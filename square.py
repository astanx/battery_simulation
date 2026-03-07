import pygame
from pygame.locals import *
import random
from constants import *
from settings import *
from helper import *
from math import exp, sqrt

class Square:
  def rothfusz_regression(self, T, H): # Expects T in Fahrenheit, 80 <= T <= 120
    HI = (-42.379 +
          2.04901523 * T +
          10.14333127 * H -
          0.22475541 * T * H -
          0.00683783 * T * T -
          0.05481717 * H * H +
          0.00122874 * T * T * H +
          0.00085282 * T * H * H -
          0.00000199 * T * T * H * H)
    
    if H < 13 and 80 <= T <= 112:
      adjustment = ((13-H)/4)*sqrt((17-abs(T-95))/17)
      HI -= adjustment
    
    if H > 85 and 80 <= T <= 87:
      adjustment = ((H-85)/10) * ((87-T)/5)
      HI += adjustment
    
    return HI
      
  def steadman_regression(self, T, H, v = 0): # Expects T in Celsius
    e = H / 100 * 6.105 * exp(17.27 * T / (237.7 + T))
    return T + 0.33 * e - 0.7 * v - 4 
  def calculate_feels_like(self):
    if temperatureBaseUnit == "C":
      T = celsius_to_fahrenheit(self.temperature)
    elif temperatureBaseUnit == "F":        
      T = self.temperature
    elif temperatureBaseUnit == "K":
      T = kelvin_to_fahrenheit(self.temperature)
      
    if T >= 80 and T <= 120:
      HI = self.rothfusz_regression(T, self.humidity)
    else:
      T_c = fahrenheit_to_celsius(T)
      HI_c = self.steadman_regression(T_c, self.humidity)
      HI = celsius_to_fahrenheit(HI_c)
    
    if temperatureBaseUnit == "C":
      return fahrenheit_to_celsius(HI)
    elif temperatureBaseUnit == "F":
      return HI
    elif temperatureBaseUnit == "K":
      return fahrenheit_to_kelvin(HI)
    
  def __init__(self, pos=(400, 300), size=100, color=None, humidity=None, temperature=None):
    self.pos = pos
    self.size = size
        
    self.humidity = humidity if humidity is not None else random.randint(minimumRandomHumidity, maximumRandomHumidity)
    self.temperature = temperature if temperature is not None else random.randint(minimumRandomTemperature, maximumRandomTemperature)
    self.feels_like = self.calculate_feels_like()
    
    if color is None:
      r = max(0, min(255, int((self.temperature + 30) * 4)))
      g = max(0, min(255, int((self.feels_like + 30) * 4)))
      b = max(0, min(255, int(self.humidity * 2.55)))
      self.color = (r, g, b)
    else:
      self.color = color
      
    self.font = pygame.font.SysFont(None, int(self.size / 6))

  def resize(self, new_size):
    self.size = new_size
    self.font = pygame.font.SysFont(None, int(self.size / 6))
  def set_position(self, x, y):
    self.pos = (x, y)
    
  def draw(self, surface):
    pygame.draw.rect(surface, self.color,
                 [self.pos[0] - self.size/2, self.pos[1] - self.size/2, self.size, self.size], 0, 10)
    
    text_surface = self.font.render(f"H: {self.humidity:.2f}%", True, BLACK)
    surface.blit(text_surface, (self.pos[0] - self.size/4, self.pos[1] - self.size/4))
    
    text_surface = self.font.render(f"T: {self.temperature:.2f}{temperatureBaseUnit}", True, BLACK)
    surface.blit(text_surface, (self.pos[0] - self.size/4, self.pos[1] - self.size/4 + 12))
    
    text_surface = self.font.render(f"FL: {self.feels_like:.2f}{temperatureBaseUnit}", True, BLACK)
    surface.blit(text_surface, (self.pos[0] - self.size/4, self.pos[1] - self.size/4 + 24))
    
  
  def move(self, speed, dt):
    self.pos = (self.pos[0], self.pos[1] + speed * dt * self.size)
    
  