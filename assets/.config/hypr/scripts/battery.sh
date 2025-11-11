#!/bin/bash

# Check device name
BAT=$(upower -e | grep BAT | head -n1)

PERCENT=$(upower -i $BAT | grep -E "percentage" | awk '{print $2}' | tr -d '%')
STATE=$(upower -i $BAT | grep -E "state" | awk '{print $2}')

if [[ "$STATE" == "charging" || "$STATE" == "fully-charged" ]]; then
  ICON="󰂄"
else
  if (( PERCENT == 100 )); then
    ICON="󰁹"
  elif (( PERCENT >= 90 )); then
    ICON="󰂂"
  elif (( PERCENT >= 80 )); then
    ICON="󰂁"
  elif (( PERCENT >= 70 )); then
   ICON="󰂀" 
  elif (( PERCENT >= 60 )); then
   ICON="󰁿" 
  elif (( PERCENT >= 50 )); then
   ICON="󰁾" 
  elif (( PERCENT >= 40 )); then
   ICON="󰁽"
  elif (( PERCENT >= 30 )); then
   ICON="󰁼"
  elif (( PERCENT >= 20 )); then
   ICON="󰁻"
  elif (( PERCENT >= 10 )); then
   ICON="󰁺"
  else 
   ICON="󰂎"
  fi
fi

echo "$ICON $PERCENT%"

