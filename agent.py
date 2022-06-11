import numpy as np
import pygame as pg



Vector = pg.math.Vector2


class Vehicle:
    def __init__(self, x, y):
        self.acceleration = Vector(0,0)
        self.velocity = Vector(0,-2)
        self.position = Vector(x,y)
        self.r = 5
        self.maxspeed = 5
        self.maxforce = 0.2
        self.rect = pg.Rect(x,y,1,1)
        self.health = 1000

    def update(self):
        self.velocity += self.acceleration
        if self.velocity.magnitude() > self.maxspeed:
            self.velocity.scale_to_length(self.maxspeed)
        self.position += self.velocity
        self.acceleration.update(0,0)

    def applyForce(self, force):
        self.acceleration += force
        if self.acceleration.magnitude() > self.maxforce:
            self.acceleration.scale_to_length(self.maxforce)

    def seek(self, target):
        desired = target - self.position
        # desired.normalize_ip()
        steer = desired - self.velocity
        self.applyForce(steer)

    def display(self, surf):
        phi = self.velocity.as_polar()[1] + 90
        vector1 = Vector(0, -self.r*2).rotate(phi)
        vector2 = Vector(-self.r, self.r*2).rotate(phi)
        vector3 = Vector(self.r, self.r*2).rotate(phi)
        self.rect = pg.draw.polygon(surf, pg.Color(0,255,0),[self.position+vector1,self.position+vector2,self.position+vector3])
        # pg.draw.circle(surf,pg.Color(0,255,0),self.position, self.r)

class Food:
    def __init__(self,x,y):
        self.rect = pg.Rect(x,y,1,1)
        self.position = Vector(x, y)
        self.r = 2

    def display(self, surf):
        self.rect = pg.draw.circle(surf, pg.Color(255,255,255), self.position, self.r)