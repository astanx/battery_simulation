import pygame
from pygame.locals import *
import random
from square import Square
from constants import *
from cell.cell import Cell
from settings import *

class Road:
  def create_squares(self, num_squares=5, windowHeight=INIT_HEIGHT):
    if useUI and len(self.squares) == 0:
      num = int(input(f"Enter number of squares to generate for {self.name}: "))
      isUI = input(f"Do you want to input values for squares? (y/n): ").lower() == 'y'
      
      for _ in range(num):
        humidity = random.randint(minimumRandomHumidity, maximumRandomHumidity)
        temperature = random.randint(minimumRandomTemperature, maximumRandomTemperature)
        if isUI:
          humidity = float(input(f"Enter humidity for square: "))
          temperature = float(input(f"Enter temperature for square: "))

        self.create_square(humidity=humidity, temperature=temperature, windowHeight=windowHeight)
    else:
      for _ in range(num_squares):
        self.create_square(humidity=random.randint(minimumRandomHumidity, maximumRandomHumidity), temperature=random.randint(minimumRandomTemperature, maximumRandomTemperature), windowHeight=windowHeight)
  
  def move_battery_up(self):
    self.cell.set_position(self.cell.pos[0], self.cell.pos[1] - self.gap)
  
  def move_battery_down(self):
    self.cell.set_position(self.cell.pos[0], self.cell.pos[1] + self.gap)
  
  def create_square(self, humidity, temperature, windowHeight=INIT_HEIGHT):
    init = self.squares[-1].pos[1] - self.gap if self.squares else windowHeight / 2 - self.cell.size / 2 - 100
    y = init
    self.squares.append(Square(pos=(self.x, y), size=self.square_size, humidity=humidity, temperature=temperature))
  
  def __init__(self, cell, x=400, name="Road", scale=None, windowHeight=INIT_HEIGHT):
    self.x = x
    self.gap = windowHeight / 5
    self.square_size = windowHeight / 6
    self.cell_size = self.square_size * 0.5
    self.name = name
    
    self.cell = cell
    self.cell.set_position(self.x, windowHeight / 2)
    self.cell.resize(self.cell_size)

    self.scale = scale if scale is not None else self.x / INIT_WIDTH
    
    self.cell_energy_font = pygame.font.SysFont(None, int(self.square_size / 6))
    
    self.squares = []
    
    if useAutoSquares:
      self.create_squares()
    
  def add_square(self, humidity, temperature):
    self.create_square(humidity=humidity, temperature=temperature)
  
  def draw(self, surface):
    for square in self.squares:
      square.draw(surface)
      
    self.cell.draw(surface)
    
    surface.blit(self.cell_energy_font.render(f"{self.name} cell energy: {self.cell.energy:.2f} ({self.cell.get_percentage():.2f}%)", True, WHITE), (self.x - self.square_size, 20))
      
  def update(self, dt, is_stopped=False, energy_time_scale=1.0):
    if not is_stopped:
      for square in self.squares:
        if (self.cell.energy > 0):
          square.move(speed=self.cell.speed, dt=dt)
    
    self.cell.update(self.squares, dt * energy_time_scale)    
    
    if self.squares and self.squares[-1].pos[1] > self.cell.pos[1] + self.cell.size and self.cell.energy > 0 and infiniteSquares:
      self.create_squares(num_squares=1)
      
  def handle_resize(self, width, height):
    new_x = width * self.scale
    new_square_size = height / 6
    new_cell_size = new_square_size * 0.5
    new_gap = height / 5

    scale_factor = new_square_size / self.square_size if self.square_size > 0 else 1.0

    self.x = new_x
    self.gap = new_gap
    self.square_size = new_square_size
    self.cell_size = new_cell_size

    self.cell.resize(new_cell_size)
    self.cell.set_position(new_x, self.cell.pos[1] * scale_factor)

    for square in self.squares:
        square.resize(new_square_size)
        square.set_position(new_x, square.pos[1] * scale_factor)

    self.cell_energy_font = pygame.font.SysFont(None, int(new_square_size / 6))
    
      