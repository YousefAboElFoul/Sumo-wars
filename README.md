Sumo Wars Robot Project

Overview
Sumo Wars is a robotics project aimed at building a versatile robot capable of competing in sumo-style competitions. The robot utilizes various sensors for navigation, line following, and object detection, coupled with motor control for movement. The project incorporates Raspberry Pi as the main controller, along with additional hardware components such as the Pololu QT8-8RC sensor array and the MCP23017 GPIO expander.

Features
Line Following: Utilizes Pololu QT8-8RC sensor array for accurate line detection and following.
Object Detection: Implements ultrasonic distance measurement for detecting obstacles and avoiding collisions.
Motor Control: Controls the movement of the robot using DC motors, enabling forward, backward, and rotation maneuvers.
GPIO Expansion: Integrates the MCP23017 GPIO expander for expanding the number of available GPIO pins, allowing for more sensors and actuators to be connected.
Requirements
Hardware:
Raspberry Pi (Model 3B+ or higher recommended)
DC Motors
Pololu QT8-8RC Sensor Array
MCP23017 GPIO Expander
Ultrasonic Distance Sensor (HC-SR04)
Chassis, wheels, and other mechanical components
Software:
Python 3
RPi.GPIO library
Adafruit_GPIO library
Other libraries as specified in the code
Installation
Hardware Setup: Assemble the robot chassis, attach motors, sensors, and other components according to the provided schematics.

Software Setup:

Clone this repository to your Raspberry Pi.
Install the required Python libraries using pip install -r requirements.txt.
Update the GPIO pin configurations and sensor connections in the code as per your hardware setup.
Usage
Navigate to the project directory on your Raspberry Pi.

Run the main script using Python:

Copy code
python sumo_wars.py
Follow the on-screen instructions to control the robot and observe its behavior.

Contributing
Contributions to improve this project are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

License
This project is licensed under the MIT License.

Acknowledgements
Inspired by various robotics and DIY projects available online.
Thanks to the contributors of open-source libraries and resources used in this project.
