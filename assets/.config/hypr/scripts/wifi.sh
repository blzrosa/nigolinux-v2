#!/bin/bash

SSID=$(nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d: -f2)
STRENGTH=$(nmcli -f IN-USE,SIGNAL dev wifi | grep '\*' | awk '{print $2}')

if [[ -z "$SSID" || -z "$STRENGTH" ]]; then
    echo "󰤮 Disconnected"
    exit
fi

if (( STRENGTH >= 80 )); then
    ICON="󰤨"
elif (( STRENGTH >= 60 )); then
    ICON="󰤥"
elif (( STRENGTH >= 40 )); then
    ICON="󰤢"
elif (( STRENGTH >= 20 )); then
    ICON="󰤟"
else
    ICON="󰤯"
fi

echo "$ICON $SSID"

