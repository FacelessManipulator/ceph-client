#!/usr/bin/env python
import rados, sys

cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
print "\nlibrados version: " + str(cluster.version())
print "Will attempt to connect to: " + str(cluster.conf_get('mon initial members'))

cluster.connect()
print "\nCluster ID: " + cluster.get_fsid()
print "\n\nCluster Statistics"
print "=================="
cluster_stats = cluster.get_cluster_stats()

for key, value in cluster_stats.iteritems():
        print key, value
cluster.create_pool('test')
#pool =  cluster.list_pools()[0]
#cluster.delete_pool(pool)
ioctx = cluster.open_ioctx('test')
ioctx.write_full("hc", "Hello World!12")
print ioctx.read("hc")
ioctx.close()
