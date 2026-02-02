#!/usr/bin/env bash

# EPYC 9354P specific settings
# MSR 0xC0010015: Hardware Configuration Register
# Bit 25: CPB (Core Performance Boost) Disable
MSR_HWCR="0xC0010015"
BIT_CPB=25

# MSR 0xC0010062: P-State Control
# Writing 0 forces the CPU to P-State 0 (Highest non-boost frequency)
MSR_PSTATE_CTL="0xC0010062"

echo "--- EPYC 9354P Hardware-Level Lock ---"

# 1. Install MSR tools if missing
if ! command -v wrmsr &> /dev/null; then
    echo "[!] Installing msr-tools..."
    sudo apt-get update && sudo apt-get install -y msr-tools
fi

sudo modprobe msr

# 2. Disable Core Performance Boost (Turbo)
# This prevents the clock from jumping above 3.25GHz
echo "[+] Disabling Boost via MSR..."
CURRENT_HWCR=$(sudo rdmsr -d $MSR_HWCR)
NEW_HWCR=$((CURRENT_HWCR | (1 << BIT_CPB)))
sudo wrmsr -a $MSR_HWCR $(printf '0x%x' "$NEW_HWCR")

# 3. Force P-State 0 (Highest Base Clock)
# On EPYC, P0 is typically the rated base clock (3.25GHz for 9354P)
echo "[+] Forcing P-State 0 across all cores..."
sudo wrmsr -a $MSR_PSTATE_CTL 0x0

# 4. Disable C-States (Stop the CPU from sleeping)
# Since your sysfs is empty, we use the kernel boot interface if possible
# but for now, we try the standard path:
if [ -d /sys/devices/system/cpu/cpu0/cpuidle ]; then
    echo "[+] Disabling C-States..."
    for i in /sys/devices/system/cpu/cpu*/cpuidle/state*/disable; do
        echo 1 | sudo tee $i > /dev/null
    done
fi

echo "--- Done ---"
echo "Check frequency now using: watch -n 1 \"grep MHz /proc/cpuinfo\""