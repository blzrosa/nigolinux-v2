#!/bin/bash

WALLPAPER_DIR="$HOME/.config/wallpapers/nigo"

generate_entries() {
    find "$WALLPAPER_DIR" -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.jpeg" -o -name "*.webp" \) | sort | while read -r file; do
        filename_with_ext=$(basename "$file")
        display_name=${filename_with_ext%.*}

        printf "%s\0icon\x1f%s\n" "$display_name" "$file"
    done
}

SELECTED_BASENAME=$(generate_entries | rofi -dmenu -show-icons -i -p "Select Wallpaper:")

if [ -n "$SELECTED_BASENAME" ]; then
    FULL_PATH=$(find "$WALLPAPER_DIR" -type f -name "${SELECTED_BASENAME}.*" | head -n 1)

    if [ -n "$FULL_PATH" ]; then
        swww img "$FULL_PATH" --transition-type outer --transition-fps 60
    fi
fi
