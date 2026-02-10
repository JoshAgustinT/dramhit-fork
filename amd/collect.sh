#  rm build/CMakeCache.txt
#     cmake -S . -B build
#     cmake --build build/ --clean-first
#  sudo apt-get install cmake-curses-gui
#  nix develop --extra-experimental-features nix-command --extra-experimental-features flakes
# 'Constants' hash table types


# ./collect.sh large single-local 32

DRAMHIT=3
GROWT=6
DRAMHIT23=8


# Ensure correct usage
if [ "$#" -ne 3 ]; then
     echo "Usage: $0 <small|large> <numa_policy> <num_threads> ʕ•ᴥ•ʔ"
     exit 1
fi
#if [ "$#" -ne 2 ]; then
#    echo "Usage: $0 <small|large> <num_threads> ʕ•ᴥ•ʔ"
#    exit 1
#fi
test=$1
numa_policy=$2
numThreads=$3

if [ "$numa_policy" = "single-local" ]; then
    numa_policy=6  
elif [ "$numa_policy" = "single-remote" ]; then
    numa_policy=6
elif [ "$numa_policy" = "dual" ]; then
    numa_policy=6
fi

#TEST 256 KB
if [ "$test" = "small" ]; then
    size=524288 
    insertFactor=10000
    readFactor=10000
#TEST 2GB HT
elif [ "$test" = "large" ]; then
    # size=4294967296
    # size=268435456
    size=536870912 
    # size=4096

    # size=1073741824
    # size=268435456
    # size=524288
    insertFactor=1000
    readFactor=1000
fi

# size=134217728
# insertFactor=10
# size=2048
# insertFactor=1000000
# numThreads=1

fill=70

HASHJOIN=13
rsize=375809638
ZIPFIAN=11
UNIFORM=14

OUTPUT_FILE=output.txt
HOME_DIR=/opt/dramhit-fork
# This is for in-order batching tests
cmake -S $HOME_DIR -B $HOME_DIR/build -DIN_ORDER_BATCHING=OFF -DDRAMHiT_VARIANT=2025_INLINE -DBUCKETIZATION=ON -DBRANCH=simd -DUNIFORM_PROBING=ON -DPREFETCH=DOUBLE
cmake --build $HOME_DIR/build

# Let's test this with MLC, Folklore, DRAMHit, dramblast regular double prefetch?
# collect... performance 10-90, bw at 70%?, probably it...lfb might as well.

echo "" > $OUTPUT_FILE

# DRAMBLAST
    echo "START dramblast {" >> $OUTPUT_FILE
    cmd="--perf_cnt_path ./perf_cnt.txt --perf_def_path ./perf-cpp/perf_list.csv \
    --find_queue 64 --ht-fill $fill --ht-type $DRAMHIT --insert-factor $insertFactor --read-factor $readFactor\
    --num-threads $numThreads --numa-split $numa_policy --no-prefetch 0 --mode $ZIPFIAN --ht-size $size --skew 0.01\
    --hw-pref 0 --batch-len 16 --relation_r_size $rsize"

    EVENTS="unc_m_cas_count.all,unc_m_cas_count.rd,unc_m_cas_count.wr"
    # Get bw info
    # sudo perf stat -I 1000 -e $EVENTS -- $HOME_DIR/build/dramhit $cmd > /dev/null 2>> $OUTPUT_FILE
    # sudo /usr/bin/perf stat -a -M umc_mem_bandwidth -I 1000 -- $HOME_DIR/build/dramhit $cmd > /dev/null 2>> $OUTPUT_FILE

    echo "START uniform test {" >> $OUTPUT_FILE
    # 10-90 fill performance
    for fill_loop in $(seq 10 10 90);
    do  
        cmd="--perf_cnt_path ./perf_cnt.txt --perf_def_path ./perf-cpp/perf_list.csv \
        --find_queue 64 --ht-fill $fill_loop --ht-type $DRAMHIT --insert-factor $insertFactor --read-factor $readFactor\
        --num-threads $numThreads --numa-split $numa_policy --no-prefetch 0 --mode $ZIPFIAN --ht-size $size --skew 0.01\
        --hw-pref 0 --batch-len 16 --relation_r_size $rsize"
        sudo $HOME_DIR/build/dramhit $cmd | grep "get_mops" >> $OUTPUT_FILE
         echo $HOME_DIR/build/dramhit $cmd >> $OUTPUT_FILE
    done  
    

    echo "} END uniform test" >> $OUTPUT_FILE
    echo "} END dramblast" >> $OUTPUT_FILE


# #DRAMHIT23
   
#     echo "START dramhit23 {" >> $OUTPUT_FILE
#     cmd="--perf_cnt_path ./perf_cnt.txt --perf_def_path ./perf-cpp/perf_list.csv \
#     --find_queue 64 --ht-fill $fill --ht-type $DRAMHIT23 --insert-factor $insertFactor --read-factor $readFactor\
#     --num-threads $numThreads --numa-split $numa_policy --no-prefetch 0 --mode $ZIPFIAN --ht-size $size --skew 0.01\
#     --hw-pref 0 --batch-len 16 --relation_r_size $rsize"

#     EVENTS="unc_m_cas_count.all,unc_m_cas_count.rd,unc_m_cas_count.wr"
#     # Get bw info
#     # sudo perf stat -I 1000 -e $EVENTS -- $HOME_DIR/build/dramhit $cmd > /dev/null 2>> $OUTPUT_FILE
#     sudo /usr/bin/perf stat -a -M umc_mem_bandwidth -I 1000 -- $HOME_DIR/build/dramhit $cmd > /dev/null 2>> $OUTPUT_FILE


#     echo "START uniform test {" >> $OUTPUT_FILE
#     # 10-90 fill performance
#     for fill_loop in $(seq 10 10 90);
#     do  
#         cmd="--perf_cnt_path ./perf_cnt.txt --perf_def_path ./perf-cpp/perf_list.csv \
#         --find_queue 64 --ht-fill $fill_loop --ht-type $DRAMHIT23 --insert-factor $insertFactor --read-factor $readFactor\
#         --num-threads $numThreads --numa-split $numa_policy --no-prefetch 0 --mode $ZIPFIAN --ht-size $size --skew 0.01\
#         --hw-pref 0 --batch-len 16 --relation_r_size $rsize"
#         sudo $HOME_DIR/build/dramhit $cmd | grep "get_mops" >> $OUTPUT_FILE
#          echo $HOME_DIR/build/dramhit $cmd >> $OUTPUT_FILE
#     done  
    

#     echo "} END uniform test" >> $OUTPUT_FILE
#     echo "} END dramhit23" >> $OUTPUT_FILE

# #FOLKLORE
#    echo "START folklore {" >> $OUTPUT_FILE
#     cmd="--perf_cnt_path ./perf_cnt.txt --perf_def_path ./perf-cpp/perf_list.csv \
#     --find_queue 64 --ht-fill $fill --ht-type $DRAMHIT23 --insert-factor $insertFactor --read-factor $readFactor\
#     --num-threads $numThreads --numa-split $numa_policy --no-prefetch 1 --mode $ZIPFIAN --ht-size $size --skew 0.01\
#     --hw-pref 0 --batch-len 16 --relation_r_size $rsize"

#     EVENTS="unc_m_cas_count.all,unc_m_cas_count.rd,unc_m_cas_count.wr"
#     # Get bw info
#     # sudo perf stat -I 1000 -e $EVENTS -- $HOME_DIR/build/dramhit $cmd > /dev/null 2>> $OUTPUT_FILE
#     sudo /usr/bin/perf stat -a -M umc_mem_bandwidth -I 1000 -- $HOME_DIR/build/dramhit $cmd > /dev/null 2>> $OUTPUT_FILE


#     echo "START uniform test {" >> $OUTPUT_FILE
#     # 10-90 fill performance
#     for fill_loop in $(seq 10 10 90);
#     do  
#         cmd="--perf_cnt_path ./perf_cnt.txt --perf_def_path ./perf-cpp/perf_list.csv \
#         --find_queue 64 --ht-fill $fill_loop --ht-type $DRAMHIT23 --insert-factor $insertFactor --read-factor $readFactor\
#         --num-threads $numThreads --numa-split $numa_policy --no-prefetch 1 --mode $ZIPFIAN --ht-size $size --skew 0.01\
#         --hw-pref 0 --batch-len 16 --relation_r_size $rsize"
#         sudo $HOME_DIR/build/dramhit $cmd | grep "get_mops" >> $OUTPUT_FILE
#          echo $HOME_DIR/build/dramhit $cmd >> $OUTPUT_FILE
#     done  
    

#     echo "} END uniform test" >> $OUTPUT_FILE
#     echo "} END folklore" >> $OUTPUT_FILE




#     echo "MLC {" >> $OUTPUT_FILE

#     sudo $HOME_DIR/tools/mlc/mlc --bandwidth_matrix -U -h>> $OUTPUT_FILE

#     echo "} MLC" >> $OUTPUT_FILE


