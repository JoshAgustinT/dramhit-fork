#  rm build/CMakeCache.txt
#     cmake -S . -B build
#     cmake --build build/ --clean-first
#  sudo apt-get install cmake-curses-gui
#  nix develop --extra-experimental-features nix-command --extra-experimental-features flakes
# 'Constants' hash table types
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
    numa_policy=4  
elif [ "$numa_policy" = "single-remote" ]; then
    numa_policy=3
elif [ "$numa_policy" = "dual" ]; then
    numa_policy=1
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

    # size=1073741824
    # size=268435456
    # size=134217728
    insertFactor=1
    readFactor=1
fi

# size=134217728
# insertFactor=10
# size=2048
# insertFactor=1000000
# numThreads=1

fill=10

HASHJOIN=13
rsize=375809638
ZIPFIAN=11
UNIFORM=14


# Let's test this with Folklore, DRAMHit, dramblast regular double prefetch?

# DRAMBLAST
    # cmd="--perf_cnt_path ./perf_cnt.txt --perf_def_path ./perf-cpp/perf_list.csv \
    # --find_queue 64 --ht-fill $fill --ht-type $DRAMHIT --insert-factor $insertFactor --read-factor $readFactor\
    # --num-threads $numThreads --numa-split $numa_policy --no-prefetch 0 --mode $ZIPFIAN --ht-size $size --skew 0.01\
    # --hw-pref 0 --batch-len 16 --relation_r_size $rsize"

    # EVENTS="unc_m_cas_count.all,unc_m_cas_count.rd,unc_m_cas_count.wr"
    # sudo perf stat -I 1000 -e $EVENTS -- $(pwd)/build/dramhit $cmd >/dev/null

#DRAMHIT23
    # cmd="--perf_cnt_path ./perf_cnt.txt --perf_def_path ./perf-cpp/perf_list.csv \
    # --find_queue 64 --ht-fill $fill --ht-type $DRAMHIT23 --insert-factor $insertFactor --read-factor $readFactor\
    # --num-threads $numThreads --numa-split $numa_policy --no-prefetch 0 --mode $ZIPFIAN --ht-size $size --skew 0.01\
    # --hw-pref 0 --batch-len 16 --relation_r_size $rsize"

    # EVENTS="unc_m_cas_count.all,unc_m_cas_count.rd,unc_m_cas_count.wr"
    # sudo perf stat -I 1000 -e $EVENTS -- $(pwd)/build/dramhit $cmd >/dev/null


#FOLKLORE
    cmd="--perf_cnt_path ./perf_cnt.txt --perf_def_path ./perf-cpp/perf_list.csv \
    --find_queue 64 --ht-fill $fill --ht-type $DRAMHIT23 --insert-factor $insertFactor --read-factor $readFactor\
    --num-threads $numThreads --numa-split $numa_policy --no-prefetch 1 --mode $ZIPFIAN --ht-size $size --skew 0.01\
    --hw-pref 0 --batch-len 16 --relation_r_size $rsize"

    EVENTS="unc_m_cas_count.all,unc_m_cas_count.rd,unc_m_cas_count.wr"
    sudo perf stat -I 1000 -e $EVENTS -- $(pwd)/build/dramhit $cmd 
    # >/dev/null






# regular test, has to be its own file
# for fill in $(seq 10 10 90);
# do  
#     # Define your events
#     cmd="--perf_cnt_path ./perf_cnt.txt --perf_def_path ./perf-cpp/perf_list.csv \
#     --find_queue 64 --ht-fill $fill --ht-type $DRAMHIT --insert-factor $insertFactor --read-factor $readFactor\
#     --num-threads $numThreads --numa-split $numa_policy --no-prefetch 0 --mode $ZIPFIAN --ht-size $size --skew 0.8\
#     --hw-pref 0 --batch-len 16 --relation_r_size $rsize"
#     echo $(pwd)/build/dramhit $cmd
#     sudo $(pwd)/build/dramhit $cmd
#     echo $(pwd)/build/dramhit $cmd
# done    

