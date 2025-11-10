#!/bin/bash

# Usa nmcli pra pegar a rede ativa
SSID=$(nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d: -f2)
STRENGTH=$(nmcli -f IN-USE,SIGNAL dev wifi | grep '\*' | awk '{print $2}')

# Caso esteja desconectado
if [[ -z "$SSID" || -z "$STRENGTH" ]]; then
    echo "󰤮 Disconnected"
    exit
fi

# Define ícone com base na força do sinal
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

