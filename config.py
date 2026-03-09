# Initial width and height of the window
INIT_WIDTH = 800
INIT_HEIGHT = 600

useUI = False # True - input with console, False - random values
useAutoSquares = True # True - automatically generate squares
                      # False - only use squares added with add_square(), at app.py initialization
infiniteSquares = True # True - squares will keep generating while cell has charge, 
                        # False - only initially generated squares will be used

# Percantage
minimumRandomHumidity = 0
maximumRandomHumidity = 100

timeScale = 1.0 # Simulation time scale, DOES NOT affect speed, only energy consumption
                # 1 real second = 1 simulation second
# timeScale = 2.0 1 real second = 2 simulation seconds

temperatureBaseUnit = "K" # "C" for Celsius, "F" for Fahrenheit, "K" for Kelvin

# Kelvin (if using Celsius or Fahrenheit, change these values)
minimumRandomTemperature = 240
maximumRandomTemperature = 300

# Speed of the cell (square/second)
hydrogenSpeed = 1.0 # 1 square per second
lithiumSpeed = 1.0