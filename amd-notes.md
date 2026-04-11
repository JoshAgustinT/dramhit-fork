
```
u1399218@node-0:/opt/dramhit-fork$ sudo ./tools/mlc/mlc --bandwidth_matrix -U -h
Intel(R) Memory Latency Checker - v3.11b
Command line parameters: --bandwidth_matrix -U -h 

Using buffer size of 100.000MiB/thread for reads and an additional 100.000MiB/thread for writes
Measuring Memory Bandwidths between nodes within system 
Bandwidths are in MB/sec (1 MB/sec = 1,000,000 Bytes/sec)
Using all the threads from each core if Hyper-threading is enabled
Using Read-only traffic type
                Numa node
Numa node            0
       0        266998.4


```

u1399218@node-0:/opt/dramhit-fork$ sudo rdmsr -p 0 0xc0011022
8680000401500000
u1399218@node-0:/opt/dramhit-fork$ sudo wrmsr -a 0xc0011022 0x868000040153a000
u1399218@node-0:/opt/dramhit-fork$ sudo rdmsr -p 0 0xc0011022
868000040153a000
u1399218@node-0:/opt/dramhit-fork$ 



u1399218@node-0:/opt/dramhit-fork$ sudo ./tools/mlc/mlc --bandwidth_matrix -U -h
Intel(R) Memory Latency Checker - v3.11b
Command line parameters: --bandwidth_matrix -U -h 

Using buffer size of 100.000MiB/thread for reads and an additional 100.000MiB/thread for writes
Measuring Memory Bandwidths between nodes within system 
Bandwidths are in MB/sec (1 MB/sec = 1,000,000 Bytes/sec)
Using all the threads from each core if Hyper-threading is enabled
Using Read-only traffic type
                Numa node
Numa node            0
       0        267721.8




L2
START FIND TEST {
     4.006955273    173,872,738,552      ls_alloc_mab_count                                                    
     4.006955273      8,690,918,857       ls_mab_alloc.all_allocations                                         
     5.007952650    133,035,728,343      ls_alloc_mab_count                                                    
     5.007952650     10,396,920,273       ls_mab_alloc.all_allocations                                         
     6.008955849    132,498,068,699      ls_alloc_mab_count                                                    
     6.008955849     10,426,393,980       ls_mab_alloc.all_allocations                                         
     7.012947081    133,822,119,187      ls_alloc_mab_count                                                    
     7.012947081     10,428,916,179       ls_mab_alloc.all_allocations                                         
     8.013954861    133,593,190,577      ls_alloc_mab_count                                                    
     8.013954861     10,396,433,554       ls_mab_alloc.all_allocations                                         
     9.014926960    132,262,994,271      ls_alloc_mab_count                                                    
     9.014926960     10,378,557,722       ls_mab_alloc.all_allocations                                         
    10.015934749    131,123,371,817      ls_alloc_mab_count                                                    
    10.015934749     10,432,725,866       ls_mab_alloc.all_allocations                                         
    11.019938501    131,652,976,958      ls_alloc_mab_count                                                    
    11.019938501     10,473,402,597       ls_mab_alloc.all_allocations                                         
    12.020938031    131,759,086,687      ls_alloc_mab_count                                                    
    12.020938031     10,393,726,562       ls_mab_alloc.all_allocations                                         
    13.021951460    134,701,584,066      ls_alloc_mab_count                                                    
    13.021951460     10,130,650,325       ls_mab_alloc.all_allocations                                         
    14.022945960    131,704,682,454      ls_alloc_mab_count                                                    
    14.022945960     10,373,146,090       ls_mab_alloc.all_allocations                                         
    15.025953927    131,223,853,509      ls_alloc_mab_count                                                    
    15.025953927     10,470,191,030       ls_mab_alloc.all_allocations                                         
    16.029926179    133,668,783,259      ls_alloc_mab_count                                                    
    16.029926179     10,394,958,775       ls_mab_alloc.all_allocations                                         
    17.030952869    133,899,326,404      ls_alloc_mab_count                                                    
    17.030952869     10,366,151,721       ls_mab_alloc.all_allocations                                         
    18.031957288    133,407,378,173      ls_alloc_mab_count                                                    
    18.031957288     10,373,941,719       ls_mab_alloc.all_allocations   


L1:

START FIND TEST {
     4.007969391  1,388,573,331,390      ls_alloc_mab_count                                                    
     4.007969391      3,677,148,227       ls_mab_alloc.all_allocations                                         
     5.008974737  1,485,524,944,429      ls_alloc_mab_count                                                    
     5.008974737      4,020,651,640       ls_mab_alloc.all_allocations                                         
     6.009975934  1,484,754,038,287      ls_alloc_mab_count                                                    
     6.009975934      4,017,940,067       ls_mab_alloc.all_allocations                                         
     7.013963612  1,489,362,829,022      ls_alloc_mab_count                                                    
     7.013963612      4,030,654,029       ls_mab_alloc.all_allocations                                         
     8.014974148  1,485,124,674,165      ls_alloc_mab_count                                                    
     8.014974148      4,019,210,196       ls_mab_alloc.all_allocations                                         
     9.015975495  1,484,740,567,429      ls_alloc_mab_count                                                    
     9.015975495      4,018,037,827       ls_mab_alloc.all_allocations                                         
    10.016974701  1,485,299,721,292      ls_alloc_mab_count                                                    
    10.016974701      4,019,693,056       ls_mab_alloc.all_allocations                                         
    11.017975717  1,484,890,370,206      ls_alloc_mab_count                                                    
    11.017975717      4,018,221,832       ls_mab_alloc.all_allocations                                         
    12.018975144  1,485,264,607,706      ls_alloc_mab_count                                                    
    12.018975144      4,019,491,951       ls_mab_alloc.all_allocations                                         
    13.019975540  1,484,893,854,326      ls_alloc_mab_count                                                    
    13.019975540      4,018,476,836       ls_mab_alloc.all_allocations                                         
    14.020976027  1,485,310,322,219      ls_alloc_mab_count                                                    
    14.020976027      4,019,823,659       ls_mab_alloc.all_allocations                                         
    15.022968757  1,486,510,767,463      ls_alloc_mab_count                                                    
    15.022968757      4,022,689,548       ls_mab_alloc.all_allocations                                         
    16.023977173  1,484,866,296,213      ls_alloc_mab_count                                                    
    16.023977173      4,018,427,291       ls_mab_alloc.all_allocations                                         
    17.025960454  1,486,370,246,327      ls_alloc_mab_count                                                    
    17.025960454      4,022,629,370       ls_mab_alloc.all_allocations                                         
    18.026976300  1,485,091,321,419      ls_alloc_mab_count                                                    
    18.026976300      4,019,180,601       ls_mab_alloc.all_allocations                                         
    19.028982577  1,486,718,666,191      ls_alloc_mab_count                                                    
    19.028982577      4,023,512,107       ls_mab_alloc.all_allocations                                         
    20.031972258  1,487,916,722,218      ls_alloc_mab_count                                                 
