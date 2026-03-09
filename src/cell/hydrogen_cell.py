from .cell import Cell
from math import exp, log
from .hydrogen_cell_constants import *
from .cell_constants import *
from config import temperatureBaseUnit
from src.helper import *


class HydrogenCell(Cell):
  def __init__(self, pos=(400, 300), size=100, color=(0, 255, 0), capacity=400.0,
              current=10.0, speed=1.0, current_density=7000,
              RH_initial=0.7, k_exchange=0.01, membrane_capacity=0.0001):
    super().__init__(pos, size, color, capacity, speed)

    self.current_density = current_density
    self.current = current
    self.RH_membrane = RH_initial  # initial membrane hydration
    self.k_exchange = k_exchange  # water exchange rate
    self.membrane_capacity = membrane_capacity  # kg water the membrane can hold

  def vapor_pressure(self, temperature):
    return exp(23.196 - 3816.44/(temperature - 46))

  def nernst_equation(self, temperature, humidity):
    H = max(humidity / 100, 1e-6)
    vapor = max(self.vapor_pressure(temperature), 1e-6)
    
    argument = (H * vapor) / (P_H2 * pow(P_O2, 0.5))
    argument = max(argument, 1e-12)
    
    return E - (R * temperature / (2 * F)) * log(argument)

  def exchange_current_desnity(self, temperature):
    return I_O_ref * exp((-E_a / R) * (1/temperature - 1/T_ref))

  def butler_volmer_equation(self, temperature):
    I_O = self.exchange_current_desnity(temperature)
    return (R * temperature / (a * n * F)) * log(self.current_density / I_O)

  def springer_membrane_conductivity(self, temperature):
    a = self.RH_membrane  # use internal membrane RH
    l = 0.043 + 17.81 * a - 39.35 * pow(a, 2) + 36 * pow(a, 3)
    sigma_mem = (0.005139 * l - 0.00326) * \
      exp(1268 * (1/303 - 1/temperature)) * 100
    n_ohmic = self.current_density * (d_mem / sigma_mem)
    return n_ohmic

  def henrys_law(self, temperature):
    return k_H_ref * exp(t_sen * (1/temperature - 1/T_ref))

  def nernstian_concentration_overpotential(self, temperature):
    C_bulk = self.bulk_oxygen_concentration(temperature)
    I_lim = n * F * D_O2 * C_bulk / d_GDL
    C_surface = C_bulk * (1 - self.current_density / I_lim)
    return (R * temperature / (n * F)) * log(C_bulk / C_surface)

  def bulk_oxygen_concentration(self, temperature):
    return (P_O2 / (R * temperature))

  def water_produced(self, dt):
    return (self.current * M_H2O / (n * F)) * dt

  def update_membrane_RH(self, RH_ambient, dt):
    delta_RH_env = self.k_exchange * (RH_ambient - self.RH_membrane) * dt
    delta_RH_prod = self.water_produced(dt) / self.membrane_capacity
    self.RH_membrane += delta_RH_env + delta_RH_prod
    self.RH_membrane = min(max(self.RH_membrane, 0.0), 1.0)

  def energy_change(self, temperature, RH_ambient, dt):
    self.update_membrane_RH(RH_ambient, dt)

    nernst = self.nernst_equation(temperature, RH_ambient*100)
    act = self.butler_volmer_equation(temperature)
    ohmic = self.springer_membrane_conductivity(temperature)
    conc = self.nernstian_concentration_overpotential(temperature)

    E_cell = nernst - act - ohmic - conc
    return E_cell * self.current * dt

  def update_energy(self, squares, dt):
    for square in squares:
      if (abs(self.pos[0] - square.pos[0]) < (self.size + square.size) / 2 and
          abs(self.pos[1] - square.pos[1]) < (self.size + square.size) / 2):
        
        if temperatureBaseUnit == "C":
          T = celsius_to_kelvin(square.temperature)
        elif temperatureBaseUnit == "F":        
          T = fahrenheit_to_kelvin(square.temperature)
        elif temperatureBaseUnit == "K":
          T = square.temperature

        self.energy -= self.energy_change(
          T, square.humidity, dt)
        
        if self.energy < 0:
          self.energy = 0
