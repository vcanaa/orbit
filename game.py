"""This example spawns (bouncing) bodies randomly on a L-shape constructed of
two segment shapes. Not interactive.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

# Python imports
import random

# Library imports
import pygame
from pygame.key import *
from pygame.locals import *
from pygame.color import *
from math import cos, sin, pi

# pymunk imports
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

import vec2dext

from agent import Agent
from planet import Planet
from rocket import Rocket
from camera import Camera


class Game(object):
  def __init__(self):
    self.space = pymunk.Space()
    self.space.gravity = (0.0, 0.0)

    self.fps = 60
    self.speedup = 10
    self.dt = 1 / self.fps
    self.physics_steps_per_frame = 8

    pygame.init()
    self.screen = pygame.display.set_mode((600, 600))
    self.clock = pygame.time.Clock()
    self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

    self.bodies = []
    self.running = True
    self.rocket_body = None

    self.objects = []
    self.create_scene()
    self.camera = Camera(self)
    self.agent = Agent(self.dt)

  def create_scene(self):
    self.planet = Planet(self, Vec2d.zero(), 300)
    self.rocket = Rocket(self, Vec2d(self.planet.shape.body.position.x + self.planet.radius + 7,
                                     self.planet.shape.body.position.y))
    self.rocket.shape.body.angle = - pi / 2
  def run(self):
    while self.running:
      for j in range(self.speedup):
        for i in range(len(self.bodies)):
          for j in range(len(self.bodies)):
            if i == j:
              continue
            b1 = self.bodies[i]
            b2 = self.bodies[j]
            d = b1.position - b2.position
            l = d.normalize_return_length()
            # print(d)
            # print(str(i) + " " + str(j) + " " + str(l))
            if l == 0:
              continue
            b2.apply_force_at_world_point(d * 1000 * b1.mass / l * b2.mass / l, b2.position)

        state = self.get_state()
        action = self.agent.update(state)
        self.apply_action(action)
        self.camera.update(
          self.rocket.shape.body.position,
          self.rocket.shape.body.velocity,
          self.planet.shape.body.position, 
          self.dt)
        dt = self.dt / self.physics_steps_per_frame
        for i in range(self.physics_steps_per_frame):
          self.space.step(dt)

      self.process_events()
      self.clear_screen()
      self.draw_objects()
      # self.space.debug_draw(self.draw_options)
      pygame.display.flip()
      self.clock.tick(self.fps)
      pygame.display.set_caption("fps: " + str(round(self.clock.get_fps(), 2)) + " fuel: " + str(round(self.rocket.fuel, 2)))

  def get_state(self):
    b1 = self.rocket.shape.body
    b2 = self.planet.shape.body
    d = b1.position - b2.position
    return [d, b1.velocity, b1.angle, b1.angular_velocity]

  def apply_action(self, action):
    angle = self.rocket.shape.body.angle
    d = Vec2d(cos(angle), sin(angle))
    throtle = action[0]
    turn = action[1]
    self.rocket.update(self.dt, throtle, turn)

  def process_events(self):
    for event in pygame.event.get():
      if event.type == QUIT:
        self.running = False
      elif event.type == KEYDOWN and event.key == K_ESCAPE:
        self.running = False
      elif event.type == KEYDOWN and event.key == K_p:
        pygame.image.save(self.screen, "bouncing_bodies.png")

  def create_circle(self, pos=Vec2d(0, 0), radius=10, mass=10):
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = pos
    shape = pymunk.Circle(body, radius, (0, 0))
    shape.elasticity = 0.1
    shape.friction = 1
    self.space.add(body, shape)
    self.bodies.append(body)
    return shape

  def create_box(self, pos=Vec2d(0, 0), size=Vec2d(1, 1), mass=10):
    inertia = pymunk.moment_for_box(mass, size)
    body = pymunk.Body(mass, inertia)
    # print(pos)
    body.position = pos
    hw = size.x / 2
    hh = size.y / 2
    shape = pymunk.Poly(
        body, [(hw, hh), (-hw, hh), (-hw, -hh), (hw, -hh)], radius=0.1)
    shape.elasticity = 0.1
    shape.friction = 1
    self.space.add(body, shape)
    self.bodies.append(body)
    return shape

  def clear_screen(self):
    self.screen.fill(THECOLORS["black"])

  def draw_objects(self):
    # print(len(self.objects))
    for o in self.objects:
      o.draw()


if __name__ == "__main__":
  game = Game()
  game.run()
