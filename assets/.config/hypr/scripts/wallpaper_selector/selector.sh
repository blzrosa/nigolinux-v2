#!/bin/bash

WALLPAPER_DIR="${WALLPAPER_PATH:-$HOME/.config/wallpapers/nigo}"
SCRIPT_DIR="$HOME/.config/hypr/scripts/wallpaper_selector"
CACHE_FILE="/tmp/current_wallpapers_list"

if [ ! -d "$WALLPAPER_DIR" ]; then
    notify-send "Error" "Directory not found: $WALLPAPER_DIR"
    exit 1
fi

find "$WALLPAPER_DIR" -type f \( -iname "*.jpg" -o -iname "*.png" -o -iname "*.jpeg" -o -iname "*.webp" \) | sort > "$CACHE_FILE"

SELECTED_INDEX=$(perl -e '
    use File::Basename;
    while (<>) {
        chomp;
        my $path = $_;
        my $filename = basename($path);
        my ($name, $ext) = split(/\.(?=[^.]+$)/, $filename);

        my $suffix = "";
        if ($name =~ /-trained$/) {
            $name =~ s/-trained$//;
            $suffix = " (trained)";
        }

        $name =~ s/-/: /;

        $name =~ s/_/ /g;

        $name =~ s/\b(\w)/\u$1/g;

        print "$name$suffix\0icon\x1f$path\n";
    }
' "$CACHE_FILE" | rofi -dmenu -show-icons -format i -p "Wallpaper:")

if [ -n "$SELECTED_INDEX" ]; then
    LINE_NUM=$((SELECTED_INDEX + 1))
    
    REAL_FILE_PATH=$(sed "${LINE_NUM}q;d" "$CACHE_FILE")

    if [ -n "$REAL_FILE_PATH" ]; then
        "$SCRIPT_DIR/backend.sh" "$REAL_FILE_PATH"
    fi
fi