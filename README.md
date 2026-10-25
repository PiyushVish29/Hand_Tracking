# Hand Tracking

A collection of Python experiments for webcam-based hand tracking with OpenCV and MediaPipe. The scripts detect hand landmarks and explore using finger gestures to control system volume, screen brightness, and images.

## Features

- Detect and draw hand landmarks from a webcam feed.
- Recognize basic finger gestures.
- Adjust Windows system volume or screen brightness using the distance between the thumb and index finger.
- Experiment with zooming, moving, and navigating images using hand gestures.

## Requirements

- Python 3
- A webcam
- Windows for the system volume and brightness controls

Python packages used by the scripts:

```text
opencv-python
mediapipe
numpy
pycaw
comtypes
screen-brightness-control
```

Install the packages with:

```powershell
python -m pip install opencv-python mediapipe numpy pycaw comtypes screen-brightness-control
```

## Run

From the project directory, start a script with Python. For example, to see hand tracking:

```powershell
python testing.py
```

Other scripts are separate experiments:

| File | Purpose |
| --- | --- |
| `hand_tracker.py` | Reusable hand landmark and finger gesture detection |
| `testing.py` | Basic webcam hand tracking demo |
| `main.py`, `main2.py`, `main3.py` | Experiments combining gesture detection with system or image controls |
| `volume_control.py` | Windows system volume control |
| `brightness_control.py` | Screen brightness control demo |
| `image_control.py`, `image_control2.py` | Image display and gesture-control experiments |

## Configuration and notes

- Allow webcam access when prompted. Press **Esc** to exit the webcam demos.
- Update image folder paths in the image-control scripts to point to a folder on your computer before using those experiments.
- The volume and brightness controls depend on Windows APIs and may not work on other operating systems.
- These scripts are prototypes; individual experiments may require configuration or fixes for your machine and installed package versions.
