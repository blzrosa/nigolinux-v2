#!/bin/bash

H=$(date +%H)
M=$(date +%M)

# rule:
# 00:00 → 24:00
# 01:00 → 25:00
# 02:00 → 02:00 (normal from now onwards)
if [ "$H" -eq 0 ]; then
    H=24
elif [ "$H" -eq 1 ]; then
    H=25
fi

printf '{"text": " %02d:%s"}\n' "$((10#$H))" "$M"
