#!/bin/bash

echo "═══════════════════════════════════════════════════════════════"
echo "  ELI IS A FROG - THE LEGEND OF THE EMERALD GUARDIAN"
echo "  Installation & Run Script"
echo "═══════════════════════════════════════════════════════════════"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install numpy matplotlib

# Check for ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo ""
    echo "WARNING: ffmpeg not found. Attempting to install..."
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y ffmpeg
    elif command -v brew &> /dev/null; then
        brew install ffmpeg
    else
        echo "Please install ffmpeg manually for audio support."
    fi
fi

# Run the animation
echo ""
echo "Starting animation render..."
echo "This will take a LONG time (11+ minutes of animation = ~40,000 frames)"
echo ""

python3 eli_is_a_frog.py

echo ""
echo "Done! Look for eli_is_a_frog_movie.mp4"
