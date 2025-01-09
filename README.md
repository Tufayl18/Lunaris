# Lunar Exploration Rover

An innovative project for autonomous lunar exploration using IoT sensors, advanced imaging technology, and machine learning to detect and analyze geological features such as craters and boulders.

## Project Overview

This project aims to develop a sophisticated autonomous rover capable of exploring extra-terrestrial terrains, detecting geological features, and enhancing our understanding of the Moon's surface. The rover integrates Raspberry Pi with various sensors and a motorized system for autonomous navigation, depth sensing, and real-time data communication.

## Features

- **Autonomous Navigation**: Detect and avoid obstacles using ultrasonic sensors.
- **Crater and Boulder Detection**: Employ YOLO-based object detection for identifying geological features.
- **Depth Sensing**: Generate depth maps using MiDaS for precise terrain analysis.
- **Low-Light Image Enhancement**: Improve visibility in permanently shadowed regions (PSRs).
- **Wio Terminal Integration**: Displays real-time data and provides auditory alerts during turns and obstacle detection.
- **Wireless Data Transmission**: Real-time communication using Wi-Fi technology.

## System Design

### Hardware

- **Raspberry Pi 3B+**: Central controller
- **5MP Camera Module**: Image and video capture
- **HC-SR04 Ultrasonic Sensor**: Obstacle detection
- **L298N Motor Driver**: Motor control
- **DC Motors and Wheels**: Movement across terrains
- **Wio Terminal**: Display and interaction for real-time feedback
- **Power Supply**: 5V for Raspberry Pi, 12V for motors

### Software

- **Programming Languages**: Python
- **Libraries**:
  - OpenCV: Image processing
  - YOLO (Ultralytics): Object detection
  - MiDaS: Depth estimation
  - NumPy, Pandas, Matplotlib: Data processing and visualization
- **Development Tools**: Jupyter Notebook, Raspberry Pi OS, RealVNC Viewer

## Demonstration

### Rover Model

![Rover Model](https://github.com/Tufayl18/Lunaris/blob/main/images/Lunaris%20Model.jpg)

### Sample Output

![Sample Output](https://github.com/Tufayl18/Lunaris/blob/main/images/PSR.jpg)

### Terminal Output

![Terminal Output](https://github.com/Tufayl18/Lunaris/blob/main/images/Terminal_Output.png)

## License

This project is licensed under the [MIT License](LICENSE).
