#!/bin/bash

player=$(playerctl -l 2>/dev/null | grep -m 1 .)

if [[ -z "$player" ]]; then
  echo ""
  exit
fi

title=$(playerctl -p "$player" metadata title 2>/dev/null)
artist=$(playerctl -p "$player" metadata artist 2>/dev/null)

if [[ -z "$title" ]]; then
  echo ""
  exit
fi

# Player-based icon
case "$player" in
  spotify)
    icon=""  
    ;;
  firefox|chromium|brave|google-chrome)
    icon=""  
    ;;
  *)
    icon="" 
    ;;
esac

if [[ -n "$artist" ]]; then
  echo "$icon $artist - $title"
else
  echo "$icon $title"
fi

