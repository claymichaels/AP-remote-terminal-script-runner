#!/bin/bash

task() {
    result=$(python ap_script_runner.py --s reboot_wing4.script $1)
    echo "$1 -- $result"
}

ccu=$1
aps=$(ssh $1 "cat /var/local/consist2.txt | grep -i device | grep 10. | cut -d' ' -f1")

for apip in $aps
do
    task $apip &
done

wait
