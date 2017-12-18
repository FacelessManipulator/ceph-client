source cephenv
../src/stop.sh
MON=1 OSD=2 MDS=1 ../src/vstart.sh  -d -n -l
ceph -s

