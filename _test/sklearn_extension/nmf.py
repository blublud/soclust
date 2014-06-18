from __future__ import division

from sklearn.decomposition import NMF
from math import sqrt
import warnings
import numbers

import numpy as np
import scipy.sparse as sp
from scipy.optimize import nnls

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils import atleast2d_or_csr, check_random_state, check_arrays
from sklearn.utils.extmath import randomized_svd, safe_sparse_dot
from sklearn.decomposition.nmf import *
from sklearn.decomposition.nmf import _sparseness
from sklearn.utils.fixes import np_version

# Newer NumPy has a ravel that needs less copying.
if np_version < (1, 7, 1):
	_ravel = np.ravel
else:
	_ravel = partial(np.ravel, order='K')


def squared_norm(x):
	"""Squared Euclidean or Frobenius norm of x.

	Returns the Euclidean norm when x is a vector, the Frobenius norm when x
	is a matrix (2-d array). Faster than norm(x) ** 2.
	"""
	x = _ravel(x)
	return np.dot(x, x)


class NMF_GetAll(NMF):
	'''WARNING: This modification is for sklearn 0.15 version. If apt-get'ed sklearn is different. Modify this accordingly
	Modification to sklearn's NMF to retrieve both W,H matrix from the 
	NMF factorization of X=WH	
	'''
	def fit_transform(self, X, y=None):
		"""Learn a NMF model for the data X and returns the transformed data.

		This is more efficient than calling fit followed by transform.

		Parameters
		----------

		X: {array-like, sparse matrix}, shape = [n_samples, n_features]
			Data matrix to be decomposed

		Returns
		-------
		data: array, [n_samples, n_components]
			Transformed data
		"""
		X = atleast2d_or_csr(X)
		check_non_negative(X, "NMF.fit")

		n_samples, n_features = X.shape

		if not self.n_components:
			self.n_components_ = n_features
		else:
			self.n_components_ = self.n_components

		W, H = self._init(X)

		gradW = (np.dot(W, np.dot(H, H.T))
				 - safe_sparse_dot(X, H.T, dense_output=True))
		gradH = (np.dot(np.dot(W.T, W), H)
				 - safe_sparse_dot(W.T, X, dense_output=True))
		init_grad = norm(np.r_[gradW, gradH.T])
		tolW = max(0.001, self.tol) * init_grad  # why max?
		tolH = tolW

		tol = self.tol * init_grad

		for n_iter in range(1, self.max_iter + 1):
			# stopping condition
			# as discussed in paper
			proj_norm = norm(np.r_[gradW[np.logical_or(gradW < 0, W > 0)],
								   gradH[np.logical_or(gradH < 0, H > 0)]])
			if proj_norm < tol:
				break

			# update W
			W, gradW, iterW = self._update_W(X, H, W, tolW)
			if iterW == 1:
				tolW = 0.1 * tolW

			# update H
			H, gradH, iterH = self._update_H(X, H, W, tolH)
			if iterH == 1:
				tolH = 0.1 * tolH

		if not sp.issparse(X):
			error = norm(X - np.dot(W, H))
		else:
			sqnorm_X = np.dot(X.data, X.data)
			norm_WHT = trace_dot(np.dot(np.dot(W.T, W), H), H)
			cross_prod = trace_dot((X * H.T), W)
			error = sqrt(sqnorm_X + norm_WHT - 2. * cross_prod)

		self.reconstruction_err_ = error

		self.comp_sparseness_ = _sparseness(H.ravel())
		self.data_sparseness_ = _sparseness(W.ravel())

		H[H == 0] = 0   # fix up negative zeros
		self.components_ = H

		if n_iter == self.max_iter:
			warnings.warn("Iteration limit reached during fit")

		return W,H

