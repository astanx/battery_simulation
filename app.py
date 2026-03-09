import pygame
from pygame.locals import *

pygame.init()

from road import Road
from settings import lithiumSpeed, hydrogenSpeed, timeScale
from constants import *
from cell.lithium_cell import *
from cell.hydrogen_cell import *

class Application:
  def __init__(self):
    self.clock = pygame.time.Clock()
    self.window = pygame.display.set_mode((INIT_WIDTH, INIT_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Cell charge simulator")

    self.width = INIT_WIDTH
    self.height = INIT_HEIGHT
    self.running = True
    
    self.is_paused = False
    self.is_stopped = False
        
    # You can modify batteries here
    lithium_cell = LithiumCell(color=(0,0,255), capacity=40000, current=1, speed=lithiumSpeed, voltage=3.7)
    hydrogen_cell = HydrogenCell(color=(255,0,0), capacity=120000, current=10, current_density=7000, 
                                 speed=hydrogenSpeed, RH_initial=0.8, k_exchange=0.005, membrane_capacity=0.0002)
    
    lithium_road = Road(cell=lithium_cell, x=self.width * 3 // 4, name="Lithium")
    hydrogen_road = Road(cell=hydrogen_cell, x=self.width // 4, name="Hydrogen")

    self.roads = [
      lithium_road,
      hydrogen_road
    ]
    
    self.controller_road_index = len(self.roads) - 1
    self.controlled_road = self.roads[self.controller_road_index]
    
    # Example of adding a square with specific humidity and temperature
    # lithium_road.add_square(humidity=50, temperature=80)
    # hydrogen_road.add_square(humidity=30, temperature=90)
    
  def fill_window(self):
    self.window.fill(BG_DARK)

    for x in range(0, self.width, 40):
      pygame.draw.line(self.window, GRID_COLOR, (x, 0), (x, self.height), 1)
    for y in range(0, self.height, 40):
      pygame.draw.line(self.window, GRID_COLOR, (0, y), (self.width, y), 1)
      
  def handle_event(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      if event.type == KEYDOWN:
        self.handle_keyboard(event)
      if event.type == VIDEORESIZE:
        self.width, self.height = event.size
        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        for road in self.roads:
          road.handle_resize(self.width, self.height)
  
  def handle_keyboard(self, event):
    if event.key == K_ESCAPE:
      self.running = False
    if event.key == K_SPACE:
      self.is_stopped = not self.is_stopped
    if event.key == K_RETURN:
      self.is_paused = not self.is_paused
    
    if event.key == K_UP:
      self.controlled_road.move_battery_up()
    if event.key == K_DOWN:
      self.controlled_road.move_battery_down()
      
    if event.key == K_RIGHT:
      if self.controller_road_index > 0:
        self.controller_road_index -= 1
        self.controlled_road = self.roads[self.controller_road_index]
        
    if event.key == K_LEFT:
      if self.controller_road_index < len(self.roads) - 1:
        self.controller_road_index += 1
        self.controlled_road = self.roads[self.controller_road_index]
  
  def run(self):
    while self.running:
      dt = self.clock.tick(60) / 1000
      
      self.handle_event()
      self.fill_window()

      for road in self.roads:
        if not self.is_paused:
          road.update(is_stopped=self.is_stopped, dt=dt, energy_time_scale=timeScale)
        road.draw(self.window)
        
      pygame.display.update()
    self.quit()
    
  def quit(self):
    pygame.quit()