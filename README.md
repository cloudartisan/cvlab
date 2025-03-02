# CV Lab

Collection of computer vision tools for experimentation with OpenCV.

## Requirements
- Python 3.13 or higher

## Installation

### Setup Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install numpy opencv-python pyaudio scipy pillow matplotlib
```

### Alternative Installation with Pipenv

```bash
# Install portaudio (required for macOS)
brew install portaudio

# Install dependencies using Pipenv
pipenv install
pipenv shell
```

## Usage

### RGB Color Trackbar

Simple tool to experiment with RGB color values:

```bash
python rgb_trackbar.py
```

### Object Tracking by Color

Track objects of specific colors:

```bash
# Track green objects (default)
python object_tracking/colour_tracking.py

# Track blue objects
python object_tracking/colour_tracking.py --colour blue

# Available colors: blue, green, red, orange, yellow
```

Options:
- `--colour [COLOR]`: Color to track (blue, green, red, orange, yellow)
- `--flip`: Flip video horizontally
- `--width`: Video width (default: 160)
- `--height`: Video height (default: 120)
- `-v, --verbose`: Increase output verbosity

### Pick and Track

Select a region of color to track:

```bash
python object_tracking/pick_and_track.py
```

1. Click and drag to select a region in the input window
2. The script will track objects of that color
3. Press 'r' to reset selection
4. Press 'q' to quit

## Troubleshooting

If you encounter camera access errors:

```
OpenCV: error in [AVCaptureDeviceInput initWithDevice:error:]
OpenCV: Cannot Use FaceTime HD Camera
OpenCV: camera failed to properly initialize!
```

Try the following:

```bash
sudo killall VDCAssistant
```

If you get "No module named 'cv2'" error, make sure you've activated your virtual environment:

```bash
source .venv/bin/activate
```