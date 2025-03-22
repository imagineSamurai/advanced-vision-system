# Advanced Vision System

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.0+-green.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-no-red.svg)](https://github.com/imaginesamurai/advanced-vision-system/graphs/commit-activity)
[![Stable](https://img.shields.io/badge/Stable-yes-brightgreen.svg)](https://github.com/imaginesamurai/advanced-vision-system/releases)
[![Support](https://img.shields.io/badge/Support-yes-brightgreen.svg)](https://github.com/imaginesamurai/advanced-vision-system/issues)
[![Ko-Fi](https://img.shields.io/badge/Ko--fi-Support-ff69b4.svg)](https://ko-fi.com/imaginesamurai)

A real-time camera vision system with multiple vision modes, including night vision and thermal imaging effects.

## Features

- Multiple Vision Modes:
  - Normal Vision
  - Night Vision (High/Low/Green/Blue)
  - Thermal Vision (Hot White/Black/Rainbow/Ironbow/Plasma)
- Dynamic Battery Indicator
- Signal Strength Display
- Adjustable Frame Rate (30-240 FPS)
- Zoom Controls
- Customizable Effects:
  - Noise Filter
  - Scan Lines
  - Vignette Effect
- Interactive HUD

## Installation

1. Clone the repository:
```bash
git clone https://github.com/imaginesamurai/advanced-vision-system.git
cd advanced-vision-system
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script:
```bash
python main.py
```

### Controls

- A/D: Change Vision Mode
- W/S: Adjust Frame Rate
- +/-: Zoom In/Out
- 1: Toggle Vintage Effect
- 2: Toggle Scan Lines
- 3: Toggle HUD
- 4: Toggle Noise
- H: Toggle HUD
- Q: Quit

## Code Structure

- `main.py`: Core application loop and initialization
- `camera_handler.py`: Camera management and zoom functionality
- `vision_modes.py`: Vision effect processors
- `gui_controller.py`: User interface and controls

## Requirements

- Python 3.6+
- OpenCV
- NumPy

## Support the Project

If you find this project helpful, consider:

- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 🤝 Contributing code

You can also:
<a href='https://ko-fi.com/imagineSamurai' target="_blank"><img src='https://ko-fi.com/img/githubbutton_sm.svg' alt='Buy Me a Coffee at ko-fi.com' style='height: 25px !important;' /></a>


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenCV community
- Contributors and testers
- Everyone who has provided feedback


## Contact

- GitHub: [@imaginesamurai](https://github.com/imaginesamurai)

---
Please, if you encounter any bugs or issues, create an [issues](https://github.com/imagineSamurai/advanced-vision-system/issues) to fix it
