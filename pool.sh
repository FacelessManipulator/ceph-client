#!/usr/bin/sh

# List pools
ceph osd lspools

# create block device pool
rbd pool init <pool-name>
