#!/bin/bash

python /proj/DSL/sincere/big-server/_gited/soclust/byweek_stats/byparallel.py
tar -czvf /tmp/byweek_clusts_all.tar.gz -C /tmp/ byweek_clusts
tar -czvf /tmp/byweek_stats_all.tar.gz -C /tmp/ byweek_stats

sudo /proj/DSL/sincere/big-server/scriptlib/copy-retry.sh /tmp/byweek_clusts_all.tar.gz /scratch/DSL/sincere-big-server/cnnfox/byweek/
sudo /proj/DSL/sincere/big-server/scriptlib/copy-retry.sh /tmp/byweek_stats_all.tar.gz /scratch/DSL/sincere-big-server/cnnfox/byweek/

