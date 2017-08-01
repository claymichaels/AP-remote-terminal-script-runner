#!/bin/bash

trap 'kill $(jobs -p) 2> /dev/null' SIGINT SIGTERM EXIT

task() {
    #echo -n "$apip -- "
    pingout=$(ping -i 0.5 -c 2 $apip > /dev/null 2>&1)

    if [[ $? -eq 0 ]]
    then
        sysname=$(snmpwalk -v2c -c <snipped community string> $apip sysName | cut -d' ' -f4)
        modelout=$(python ap_script_runner.py --s ap-model.script $apip)
        does_it_contain=$(echo "$modelout" | grep "AP patched for AP7131-CAV/AP7131N-CAV SKU successfully" > /dev/null 2>&1)
        if [[ $? -eq 0 ]]
        then
            model="CAV!"
        else
            model="OK"
        fi
        echo "$apip -- $sysname -- $model"
    else
        echo "$apip -- Offline"
    fi
}


for apip in $(cat ap-list.txt)
do
    task $apip &
done

wait

exit 0
