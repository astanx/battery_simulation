import pygame
from constants import *
import math

class Cell:
  def __init__(self, pos=(400, 300), size=100, color=(0, 255, 0), capacity=400.0, speed=1.0):
    self.capacity = capacity
    self.energy = self.capacity
    self.pos = pos
    self.size = size
    self.color = color
    self.speed = speed
    
    self.elapsed_time = 0.0
    
    self.ring_width = int(size * 0.1)
    
    self.chart_data = [(self.energy, 0.0)]
  def draw(self, surface):
    pygame.draw.circle(surface, self.color,
                   [self.pos[0], self.pos[1]], self.size/2, 0)
    
    if self.energy > 0:
      angle = (self.energy / self.capacity) * 360
      pygame.draw.arc(surface, WHITE,
        (self.pos[0] - self.size/2 - self.ring_width//2, self.pos[1] - self.size/2 - self.ring_width//2, self.size + self.ring_width, self.size + self.ring_width),
        math.radians(-90), math.radians(-90 + angle), self.ring_width)

  def move(self, dt):
    if self.energy > 0:
      self.pos = (self.pos[0], self.pos[1] + self.speed * dt)
  
  def set_position(self, x, y):
    self.pos = (x, y)
  def resize(self, new_size):
    self.size = new_size
    self.ring_width = int(new_size * 0.1)
    
  def get_percentage(self):
    return self.energy / self.capacity * 100
  
  def update_energy(self, squares, dt):
    for square in squares:
      if (abs(self.pos[0] - square.pos[0]) < (self.size + square.size) / 2 and
          abs(self.pos[1] - square.pos[1]) < (self.size + square.size) / 2):
        self.energy -= dt * 5 * (square.feels_like - 60) / 50 
        if self.energy < 0:
          self.energy = 0
    
  def update(self, squares, dt):
    self.elapsed_time += dt
    self.update_energy(squares, dt)
          
    self.chart_data.append((self.energy, self.elapsed_time))