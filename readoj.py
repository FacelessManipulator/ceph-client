#!/usr/bin/env python
import rados, sys

if len(sys.argv) < 3:
    print "should followed with poolname objname"
    exit()
poolname = sys.argv[1]
objname = sys.argv[2]

cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
cluster.connect()
print "\n Reading from Cluster ID: " + cluster.get_fsid()
#cluster.create_pool('test')
#pool =  cluster.list_pools()[0]
#cluster.delete_pool(pool)
ioctx = cluster.open_ioctx(poolname)
#ioctx.write_full(objname, content)
print objname,": ",ioctx.read(objname)
ioctx.close()
