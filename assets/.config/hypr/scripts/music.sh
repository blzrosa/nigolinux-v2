#!/bin/bash

# Pega o nome do player atual
player=$(playerctl -l 2>/dev/null | grep -m 1 .)

if [[ -z "$player" ]]; then
  echo ""
  exit
fi

# Pega título e artista
title=$(playerctl -p "$player" metadata title 2>/dev/null)
artist=$(playerctl -p "$player" metadata artist 2>/dev/null)

# Se não tiver título, vaza
if [[ -z "$title" ]]; then
  echo ""
  exit
fi

# Define o ícone com base no player
case "$player" in
  spotify)
    icon=""  # ícone do Spotify (Nerd Font)
    ;;
  firefox|chromium|brave|google-chrome)
    icon=""  # ícone do YouTube (ou genérico de vídeo)
    ;;
  *)
    icon=""  # ícone genérico de música
    ;;
esac

# Se tiver artista, exibe como "ícone artista - título"
if [[ -n "$artist" ]]; then
  echo "$icon $artist - $title"
else
  echo "$icon $title"
fi

