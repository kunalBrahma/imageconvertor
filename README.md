# Image to WebP Converter

A modern, macOS-native desktop application built with Python and PyQt6 to convert PNG or JPEG images to WebP format. The app optimizes images for web use, offering both lossy and lossless compression, with a user-friendly interface featuring image previews, drag-and-drop support, and a macOS-inspired design.

![App Screenshot](assets/screenshot.png)

## Features
- **Convert Multiple Images**: Select or drag-and-drop multiple PNG or JPEG images for batch conversion to WebP.
- **Format Filtering**: Choose between PNG or JPEG input formats, with file selection restricted to the chosen type.
- **Image Preview**: View thumbnails of selected images with navigation (Previous/Next buttons or list selection).
- **Lossy/Lossless Compression**: Adjust WebP quality (0–100) for lossy compression or enable lossless mode for perfect quality.
- **Persistent Output Folder**: Set an output folder once and reuse it, with an option to change it anytime.
- **Modern UI**: macOS-native design with minimalistic colors, rounded corners, and smooth hover effects.
- **Progress Feedback**: Visual progress bar and status messages for clear conversion feedback.
- **App Icon**: Professional macOS `.icns` icon for a native look.

## Requirements
- **Operating System**: macOS (tested on macOS Ventura and later)
- **Python**: 3.9 or higher
- **Dependencies**: `libwebp` (for WebP support), installed via Homebrew

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kunalBrahma/imageconvertor.git
   cd imageconvertor
