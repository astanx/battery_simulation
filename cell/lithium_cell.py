from .cell import Cell
from math import exp
from .lithium_cell_constants import *
from .cell_constants import *
from settings import temperatureBaseUnit
from helper import *

class LithiumCell(Cell):
    def __init__(self, pos=(400, 300), size=100, color=(0, 255, 0), capacity=400.0, current=0.0, speed=1.0, voltage=3.7):      
      super().__init__(pos, size, color, capacity, speed)
      self.current = current
      self.nominal_voltage = voltage
      self.SOC = 1.0
      
    def arrhenius_equation(self, temperature): # expects temperature in Kelvin
      RT = R_ref * exp(E_a / R * (1/temperature - 1/T_ref))
      return RT
    
    def open_circuit_voltage(self, temperature):
      OCV = OCV_ref + alpha * (self.SOC - 0.5) + g * (temperature - T_ref)
      return OCV 
    
    def effective_resistance(self, temperature, humidity = 0.0):
      return self.arrhenius_equation(temperature) #* (1 + k * max(0, humidity - 50)) # Ignores SOC and humidity dependence
    
    def polarization_voltage(self, temperature):
      R_pol = R_ref * exp(E_pol / R * (1/temperature - 1/T_ref))
      return self.current * R_pol
    
    def soc_update(self, dt, efficiency = 0.995):
      d_SOC = (self.current * efficiency * dt) / (self.capacity * 3600)
      self.SOC -= d_SOC
      return self.SOC
    
    def terminal_voltage(self, temperature, humidity):
      OCV = self.open_circuit_voltage(temperature)
      R_eff = self.effective_resistance(temperature, humidity)
      V_pol = self.polarization_voltage(temperature)
      return OCV - self.current * R_eff - V_pol
    
    def energy_change(self, temperature, humidity, dt):
      V = self.terminal_voltage(temperature, humidity)
      return V * self.current * dt
    
    def capacity_degradation(self, temperature):
      T_C = temperature - 273.15
      fade = a * pow(max(0, 25 - T_C), 1.5)
      return Q_nom * (1 - fade)
    
    def update_charge(self, squares, dt):
      self.soc_update(dt=dt)
      for square in squares:
        if (abs(self.pos[0] - square.pos[0]) < (self.size + square.size) / 2 and
            abs(self.pos[1] - square.pos[1]) < (self.size + square.size) / 2):
          
          if temperatureBaseUnit == "C":
            T = celsius_to_kelvin(square.temperature)
          elif temperatureBaseUnit == "F":        
            T = fahrenheit_to_kelvin(square.temperature)
          elif temperatureBaseUnit == "K":
            T = square.temperature
          
          self.energy -= self.energy_change(T, square.humidity, dt)
          
          if self.energy < 0:
            self.energy = 0