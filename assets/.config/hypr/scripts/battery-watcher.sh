#!/bin/bash

# Inicializa flags
notified_15=false
notified_5=false

# Loop infinito
while true; do
    # Pega o nível da bateria
    BAT=$(upower -e | grep BAT | head -n1)
    PERCENT=$(upower -i "$BAT" | grep percentage | awk '{print $2}' | tr -d '%')
    STATE=$(upower -i "$BAT" | grep state | awk '{print $2}')

    # Se estiver carregando, reseta as flags
    if [[ "$STATE" == "charging" ]]; then
        notified_15=false
        notified_5=false
    fi

    # Checa 15%
    if (( PERCENT == 15 )) && [[ "$notified_15" == false ]]; then
        notify-send -u normal "󰂎 Low Battery" "15% left. Consider connecting the charger."
        notified_15=true
    fi

    # Checa 5%
    if (( PERCENT == 5 )) && [[ "$notified_5" == false ]]; then
        notify-send -u critical "󰂎 Very Low Battery" "5% left. Save your files!"
        notified_5=true
    fi

    # Dorme por 60 segundos
    sleep 30
done

