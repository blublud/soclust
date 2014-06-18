
class Parent:
	def outer(self):
		print 'Parent outer'
		self.inner()
	def inner(self):
		print 'Parent inner'

