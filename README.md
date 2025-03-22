# Advanced Vision System

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
pip install opencv-python numpy
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
- [Support on Ko-fi](https://ko-fi.com/imaginesamurai)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenCV community
- Contributors and testers
- Everyone who has provided feedback


## Contact

- GitHub: [@imaginesamurai](https://github.com/imaginesamurai)

---
Made with ❤️ by [Your Name] 