run:
	gcc -O3 -fopenmp -mcmodel=medium -DSTREAM_ARRAY_SIZE=335000000 -DNTIMES=1000 stream.c -lm
	./a.out



# -------------------------------------------------------------
# STREAM version $Revision: 5.10 $
# -------------------------------------------------------------
# This system uses 8 bytes per array element.
# -------------------------------------------------------------
# Array size = 335000000 (elements), Offset = 0 (elements)
# Memory per array = 2555.8 MiB (= 2.5 GiB).
# Total memory required = 7667.5 MiB (= 7.5 GiB).
# Each kernel will be executed 1000 times.
#  The *best* time for each kernel (excluding the first iteration)
#  will be used to compute the reported bandwidth.
# -------------------------------------------------------------
# Number of Threads requested = 64
# Number of Threads counted = 64
# -------------------------------------------------------------
# Your clock granularity/precision appears to be 1 microseconds.
# Each test below will take on the order of 18599 microseconds.
#    (= 18599 clock ticks)
# Increase the size of the arrays if this shows that
# you are not getting at least 20 clock ticks per test.
# -------------------------------------------------------------
# WARNING -- The above is only a rough guideline.
# For best results, please be sure you know the
# precision of your system timer.
# -------------------------------------------------------------
# Function    Best Rate MB/s  Avg time     Min time     Max time
# Copy:          289664.9     0.021180     0.018504     0.027151
# Scale:         189453.2     0.029745     0.028292     0.034929
# Add:           203822.4     0.041391     0.039446     0.046995
# Triad:         204972.0     0.040721     0.039225     0.046999
# -------------------------------------------------------------
# Solution Validates: avg error less than 1.000000e-13 on all three arrays
# -------------------------------------------------------------