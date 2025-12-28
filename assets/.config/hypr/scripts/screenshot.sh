#!/bin/bash

# Checking and installing dependencies
dependencies=("slurp" "grim" "convert" "swappy")
for dep in "${dependencies[@]}"; do
    command -v "$dep" &> /dev/null || { echo "$dep not found, please install it."; exit 1; }
done

screenshot="$(slurp)"

# Process the screenshot and copy to clipboard
grim -g "$screenshot" - | convert - -shave 2x2 PNG:- | wl-copy

notify-send -t 3000 -u low "Screenshot" "Screenshot copied to clipboard"

# Paste to clipboard and use swappy for further processing
wl-paste | swappy -f -

