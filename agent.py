import numpy as np
import pygame as pg
import neuralNetwork as nn


Vector = pg.math.Vector2
MAXENERGY = 10000
CHILDENERGY = 3000
viewDist = 100
MAXAGE = 10000


class Creature:
    def __init__(self, x, y, generation=0, brain=None):
        self.acceleration = Vector(0,0)
        self.velocity = Vector(0,-2)
        self.position = Vector(x,y)
        self.r = 5
        self.maxspeed = 5
        self.maxforce = 0.2
        self.rect = pg.Rect(x,y,1,1)
        self.energy = MAXENERGY
        self.alive = True
        self.justReproduced = 100
        self.color = [0,255,0]
        self.age = 0
        if brain is None:
            self.brain = nn.NeuralNetwork(nn.Layer(8, 10, 'sigmoid'), nn.Layer(10, 6, 'none'))
            self.generation = 0
        else:
            self.brain = brain
            self.brain.mutateNetwork(0.1)
            # self.color = 255
            self.energy = CHILDENERGY
            self.generation = generation

    def update(self):
        self.age += 1
        self.justReproduced -= 1
        self.velocity += self.acceleration
        if self.velocity.magnitude() > self.maxspeed:
            self.velocity.scale_to_length(self.maxspeed)
        self.position += self.velocity
        self.acceleration.update(0,0)
        self.energy -= self.velocity.length()
        self.applyForce(-0.1*self.velocity)
        # self.velocity.scale_to_length(self.velocity.length() * 0.9)
        if self.energy < 0 or self.age > MAXAGE:
            self.alive = False

    def boundary(self, bounds):
        if not self.rect.colliderect(bounds):
            self.acceleration += 10 * (bounds.center - self.position)
            self.energy -= 10

    def continuousBoundary(self, w, h):
        if self.position.x > w:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = w
        if self.position.y > h:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = h

    def applyForce(self, force):
        self.acceleration += force
        if self.acceleration.magnitude() > self.maxforce:
            self.acceleration.scale_to_length(self.maxforce)

    def seek(self, target):
        desired = target - self.position
        # desired.normalize_ip()
        steer = desired - self.velocity
        self.applyForce(steer)

    def vision(self, surf, foodList, bounds):
        angle = 30
        v1 = self.velocity.rotate(angle).normalize() * viewDist + self.position
        v2 = self.velocity.rotate(-angle).normalize() * viewDist + self.position
        self.triangle = pg.draw.polygon(surf, pg.Color(255,0,0), [self.position, v1, v2])
        b = self.triangle.colliderect(bounds)
        index = self.triangle.collidelist(foodList)
        if index > -1:
            v = foodList[index].position - self.position
            a = v.angle_to(self.velocity)
            return v.length()/viewDist, a/30, b
        else:
            return 0, 0, b

    def think(self, surf, foodList, bounds):
        dist, angle, bounds = self.vision(surf, foodList, bounds)
        b = 0
        if bounds:
            b = 1
        inputarray = [dist, angle, b, self.energy/MAXENERGY, self.age/MAXAGE, self.velocity.x/self.maxspeed, self.velocity.y/self.maxspeed, 1]
        return list(self.brain.feedForward(inputarray)[0])
        
    def reproduce(self):
        self.energy -= CHILDENERGY
        self.justReproduced = 200
        return Creature(self.position.x, self.position.y, generation=self.generation+1, brain=self.brain)


    def display(self, surf):
        phi = self.velocity.as_polar()[1] + 90
        vector1 = Vector(0, -self.r*2).rotate(phi)
        vector2 = Vector(-self.r, self.r*2).rotate(phi)
        vector3 = Vector(self.r, self.r*2).rotate(phi)
        self.rect = pg.draw.polygon(surf, pg.Color(*self.color),[self.position+vector1,self.position+vector2,self.position+vector3])
        # pg.draw.circle(surf,pg.Color(0,255,0),self.position, self.r)

class Food:
    def __init__(self,x,y,energy):
        self.rect = pg.Rect(x,y,1,1)
        self.position = Vector(x, y)
        self.r = 3
        self.energy = energy

    def display(self, surf):
        self.rect = pg.draw.circle(surf, pg.Color(255,255,255), self.position, self.r)











