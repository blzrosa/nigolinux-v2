#!/bin/bash

WALLPAPER_IMG="$1"

if [ -z "$WALLPAPER_IMG" ] || [ ! -f "$WALLPAPER_IMG" ]; then
    notify-send "Erro Wallpaper" "Arquivo não encontrado: $WALLPAPER_IMG"
    exit 1
fi

wal -i "$WALLPAPER_IMG" -n -s -t --backend haishoku

swww img "$WALLPAPER_IMG" --transition-type outer --transition-fps 60 --transition-step 90

if command -v pywalfox > /dev/null; then
    pywalfox update
fi

ln -sf "$HOME/.cache/wal/colors-waybar.css" "$HOME/.config/waybar/theme.css"
pkill -SIGUSR2 waybar

ln -sf "$HOME/.cache/wal/colors-kitty.conf" "$HOME/.config/kitty/current-theme.conf"
pkill -SIGUSR1 kitty

if [ -f "$HOME/.cache/wal/colors-hyprland.conf" ]; then
    ln -sf "$HOME/.cache/wal/colors-hyprland.conf" "$HOME/.config/hypr/theme.conf"
fi

mkdir -p "$HOME/.config/dunst"

gsettings set org.gnome.desktop.interface gtk-theme "Adwaita-dark"
gsettings set org.gnome.desktop.interface icon-theme "Papirus-Dark"
gsettings set org.gnome.desktop.interface cursor-theme "PJSK N25 Animated"
gsettings set org.gnome.desktop.interface cursor-size 24
gsettings set org.gnome.desktop.interface color-scheme "prefer-dark"

notify-send "Tema Atualizado" "Wallpaper e cores aplicados com sucesso!"
