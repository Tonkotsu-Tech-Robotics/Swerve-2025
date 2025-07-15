# Swerve-2025

A Python implementation of a swerve drive control system for robotics applications.

## Overview

This project provides a modular swerve drive system that controls four swerve modules, each consisting of a drive motor and a steering motor. The system uses the moteus motor controller library with Pi3Hat for communication.

## Features

- Asynchronous motor control using asyncio
- Modular swerve drive architecture
- Support for moteus motor controllers
- Individual module control with speed and angle settings
- Built-in test functions for system validation

## Requirements

- Python 3.7+
- Hardware: moteus motor controllers with Pi3Hat

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Tonkotsu-Tech-Robotics/Swerve-2025.git
cd Swerve-2025
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the main program:
```bash
python main.py
```

### Hardware Configuration

The system is configured for the following motor layout:
- Bus 1: Drive motor ID 11, Steer motor ID 12
- Bus 2: Drive motor ID 13, Steer motor ID 14
- Bus 3: Drive motor ID 15, Steer motor ID 16
- Bus 4: Drive motor ID 17, Steer motor ID 18

## Dependencies

- asyncio: Asynchronous programming support
- moteus: Motor controller library
- moteus-pi3hat: Pi3Hat communication interface
- wpilib: WPILib robotics library
- wpimath: WPILib math utilities
- pygame: Game development library (for potential joystick input)

## License

This project is licensed under the terms specified in the LICENSE file.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Safety Notes

- Ensure proper hardware connections before running the program
- Use appropriate safety measures when working with motors
- Test in a controlled environment before deployment