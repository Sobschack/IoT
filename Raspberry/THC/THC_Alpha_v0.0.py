"""
This script reads data from an Analog-to-Digital Converter (ADC) and an OLED display
to present real-time information based on user input and sensor readings.

Components used:
- ADS1115 ADC (Analog-to-Digital Converter) for reading analog voltage signals.
- A potentiometer connected to one of the ADC channels to input a user-defined thickness in millimeters.
- SSD1306 OLED display for showing the results.

Functionality:
1. Initializes I2C communication for interfacing with the ADC and OLED display.
2. Configures the OLED display and sets up the font for text rendering.
3. Reads voltage from a specified ADC channel and applies a correction factor.
4. Reads the potentiometer value from another ADC channel to obtain a user-defined thickness in millimeters.
5. Converts the thickness measurement to a scaled value for comparison.
6. Displays the voltage, user-defined thickness in millimeters, and a comparison message on the OLED screen.
   - The comparison message indicates whether the scaled thickness is "Up", "Down", or "Level ok"
     compared to the measured voltage.
7. Continuously updates the display at a frequency of 10 Hz (every 100 milliseconds).
8. Gracefully handles user interruptions (Ctrl+C) by clearing the OLED screen and terminating the program.

Next Steps:
- Add a 28BYJ-48 stepper motor controlled by an ULN2003 driver.
  - Connect IN1 to GPIO17
  - Connect IN2 to GPIO18
  - Connect IN3 to GPIO27
  - Connect IN4 to GPIO22
  - Note: Stepper motor support is not yet implemented.

Usage:
- Run this script on a compatible microcontroller or Raspberry Pi with connected ADC, OLED, and potentiometer components.
- Ensure the correct I2C addresses, pin configurations, and connections for the stepper motor and ULN2003 are used.

Version: v0.0
"""

import time
import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# I2C Initialization
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the SSD1306 OLED display
oled = SSD1306_I2C(128, 64, i2c)

# Create a blank image for drawing
image = Image.new('1', (oled.width, oled.height))  # '1' for 1-bit color mode
draw = ImageDraw.Draw(image)

# Increase font size by 30%
font_size = 12
new_font_size = int(font_size * 1.3)  # Increase font size
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', new_font_size)
except IOError:
    font = ImageFont.load_default()

# Initialize the ADS1115
ads = ADS1115(i2c)

# Set gain for a ±1.024V range
ads.gain = 4  # ±1.024V

# Correction factor
correction_factor = 1.188679245283019

# Function to read voltage from the specified channel
def read_voltage(channel):
    # Read raw value from the specified channel
    value = ads.read(channel)
    
    # Convert raw value to voltage
    max_adc_value = 32767  # Maximum value for 16 bits
    max_voltage = 1.024  # Maximum range for gain = 4
    voltage = (value / max_adc_value) * max_voltage
    
    # Apply correction factor
    corrected_voltage = voltage * correction_factor
    return corrected_voltage

# Function to read the potentiometer value and convert it to mm
def read_potentiometer(channel):
    # Read raw value from the potentiometer (on channel A2)
    value = ads.read(channel)
    
    # Convert raw value to a range of 1 to 14 mm
    min_adc_value = 0
    max_adc_value = 32767  # Maximum value for 16 bits
    min_mm = 1
    max_mm = 14
    # Mapping to use the full range but keeping the minimum value at 1 mm
    thickness_mm = int(((value - min_adc_value) / (max_adc_value - min_adc_value)) * (max_mm - min_mm) + min_mm)
    return thickness_mm

# Function to convert thickness to a value between 0 and 1.22
def convert_thickness_to_scale(thickness_mm):
    min_mm = 1
    max_mm = 14
    min_scale = 0
    max_scale = 1.22
    scale_value = ((thickness_mm - min_mm) / (max_mm - min_mm)) * (max_scale - min_scale) + min_scale
    return scale_value

# Function to display voltage, thickness (mm), and comparison on the OLED screen
def display_voltage_and_thickness(voltage, thickness_mm):
    # Clear the image
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    
    # Display fixed text at the top
    header_text = 'OpenTHC Alpha'
    header_bbox = draw.textbbox((0, 0), header_text, font=font)
    header_width = header_bbox[2] - header_bbox[0]
    header_height = header_bbox[3] - header_bbox[1]
    
    header_x = (oled.width - header_width) // 2
    header_y = 0  # Position at the top of the screen
    draw.text((header_x, header_y), header_text, font=font, fill=255)
    
    # Display the potentiometer value (thickness in mm) on the second line
    thickness_text = f'Thick : {thickness_mm} mm'
    thickness_bbox = draw.textbbox((0, 0), thickness_text, font=font)
    thickness_width = thickness_bbox[2] - thickness_bbox[0]
    thickness_height = thickness_bbox[3] - thickness_bbox[1]
    
    thickness_x = (oled.width - thickness_width) // 2
    thickness_y = header_height + 4  # Position just below the fixed text
    draw.text((thickness_x, thickness_y), thickness_text, font=font, fill=255)
    
    # Compare the scale to the voltage and display the appropriate message
    scale_value = convert_thickness_to_scale(thickness_mm)
    tolerance = 0.05  # 5% tolerance
    if scale_value > (voltage + tolerance):
        comparison_text = 'Up'
    elif scale_value < (voltage - tolerance):
        comparison_text = 'Down'
    else:
        comparison_text = 'Level ok'
    
    comparison_bbox = draw.textbbox((0, 0), comparison_text, font=font)
    comparison_width = comparison_bbox[2] - comparison_bbox[0]
    comparison_height = comparison_bbox[3] - comparison_bbox[1]
    
    comparison_x = (oled.width - comparison_width) // 2
    comparison_y = thickness_y + thickness_height + 4  # Position below the thickness text with some space
    draw.text((comparison_x, comparison_y), comparison_text, font=font, fill=255)
    
    # Display the voltage on the fourth line
    text = f'{voltage:.2f} V'
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (oled.width - text_width) // 2
    y = comparison_y + comparison_height + 4  # Position below the comparison text with some space
    draw.text((x, y), text, font=font, fill=255)
    
    # Display the image on the OLED screen
    oled.image(image)
    oled.show()

# Main function with Ctrl+C handling
def main():
    start_time = time.time()
    try:
        while True:
            # Read the voltage value from channel 3 (A3)
            voltage = read_voltage(3)  # Channel 3 (A3)
            
            # Read the potentiometer value in mm (on channel A2)
            thickness_mm = read_potentiometer(2)  # Channel 2 (A2)
            
            # Display the voltage, thickness, and comparison
            display_voltage_and_thickness(voltage, thickness_mm)
            
            # Wait to maintain a display frequency of 10 Hz (100 ms)
            elapsed_time = time.time() - start_time
            sleep_time = max(0, (1 / 10) - elapsed_time % (1 / 10))
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        # Handle Ctrl+C to exit gracefully
        print("\nProgram interrupted by user. Exiting...")
        oled.fill(0)
        oled.show()
        print("Display cleared. Program terminated.")

if __name__ == "__main__":
    main()

#v0.0
"""
