ceph osd crush add-bucket maxwell host
ceph osd crush move maxwell root=default
ceph osd crush set osd.1 1.0 root=default host=maxwell
ceph osd setcrushmap -i crushmap.1
ceph osd pool create base 8 8 replicated rule_base
ceph osd pool set base size 1
ceph osd pool set cache size 1
ceph osd pool create cache 8 8 replicated rule_cache
ceph osd tier add base cache
ceph osd tier cache-mode cache writeback
ceph osd tier set-overlay base cache
ceph osd pool set cache hit_set_type bloom
ceph osd pool set cache hit_set_count 12
ceph osd pool set cache hit_set_period 60
ceph osd pool set cache min_read_recency_for_promote 2
ceph osd pool set cache min_write_recency_for_promote 2

