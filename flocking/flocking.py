#!usr/bin/env

# Python modules
from __future__ import division
import random
import sys
from optparse import OptionParser
from time import time

# third-party modules
import pygame

__author__ = 'igorbpf'

# parse commandline arguments
op = OptionParser()

op.add_option("--n_boids", type=int, default=100,
              help="Number of boids in the swarm. The default is 100 boids.")
op.add_option("--neighborhood", type=int, default=500,
              help="Neighborhood radius of a boid. The default is 500 unit of measurement.")
op.add_option("--mindistance", type=int, default=20,
              help="Minimum distance between two boids. The default is 20 unit of measurement.")
op.add_option("--time", type=int, default=10,
              help="Time of execution. The default is 10 seconds.")

print(__author__)

(opts, args) = op.parse_args()
if len(args) > 0:
    op.error("this script takes no arguments.")
    sys.exit(1)

t0 = time()

class Boid(object):
    """This class defines a boid unit and apply its rules."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocityX = random.uniform(1, 20) # Random initial velocity in X
        self.velocityY = random.uniform(1, 20) # Random initial velocity in y

    # Calculate the distance between two boids.
    def get_distance(self, boid):
        X = self.x - boid.x
        Y = self.y - boid.y
        return (X ** 2 + Y ** 2)**0.5

    # Separation rule
    def apply_rule_1(self, boids, mindistance):
        if len(boids) < 1:
            return

        near_boids = 0

        pcX = 0
        pcY = 0

        for boid in boids:
            distance = self.get_distance(boid)
            if distance < mindistance:
                near_boids = near_boids + 1

                pcX = pcX - (boid.x - self.x)
                pcY = pcY - (boid.y - self.y)

        if near_boids == 0:
            return

        self.velocityX = self.velocityX + pcX
        self.velocityY = self.velocityY + pcY

    # Alignment rule
    def apply_rule_2(self, boids):
        if len(boids) < 2:
            return

        pvX = 0
        pvY = 0

        for boid in boids:

            pvX = pvX + boid.velocityX
            pvY = pvY + boid.velocityY

        pvX = pvX/(len(boids) - 1)
        pvY = pvY/(len(boids) - 1)

        pvX = (pvX - self.velocityX)/10
        pvY = (pvY - self.velocityY)/10

        self.velocityX = self.velocityX + pvX
        self.velocityY = self.velocityY + pvY

    # Cohesion rule
    def apply_rule_3(self, boids):
        if len(boids) < 2:
            return

        pcX = 0
        pcY = 0
        for boid in boids:
            if boid.x != self.x and boid.y != self.y:

                pcX = pcX + boid.x
                pcY = pcY + boid.y

        pcX = pcX/(len(boids) - 1)
        pcY = pcY/(len(boids) - 1)


        pcX = (pcX - self.x)/100
        pcY = (pcY - self.y)/100

        self.velocityX = self.velocityX + pcX
        self.velocityY = self.velocityY + pcY

    # New position
    def get_position(self, k_boids):
        self.x = self.x + 0.3 * k_boids/100 * self.velocityX
        self.y = self.y + 0.3 * k_boids/100 * self.velocityY
# End of the Boid class


# Main routine
pygame.init()  # Initialize Pygame

numBoids = opts.n_boids  # Number of Boids
boids = []

size = width, height = 1250, 700  # Size of the screen
black = 0, 0, 0

screen = pygame.display.set_mode(size) # Open the screen

pygame.display.set_caption('Flocking')  # Title


ball = pygame.image.load("../images/smallBall.jpg") # Ball image
ballrect = ball.get_rect()              # Get the template

# Initialize boids in random positions
for i in range(numBoids):
    boids.append(Boid(x=random.uniform(0, width), y=random.uniform(0, height)))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Boid checks its neighborhood
    for boid in boids:
        neighbors_boids = []
        for boids_around in boids:
            if boids_around != boid:
                distance = boid.get_distance(boids_around)
                if distance < opts.neighborhood:
                    neighbors_boids.append(boids_around)


        boid.apply_rule_1(neighbors_boids, opts.mindistance)
        boid.apply_rule_3(neighbors_boids)
        boid.apply_rule_2(neighbors_boids)

        boid.get_position(opts.n_boids)

        # Keep the boids inside the screen space
        border = 20

        if boid.x < border and boid.velocityX < 0:
            boid.velocityX = -boid.velocityX
        if boid.x > width - border and boid.velocityX > 0:
            boid.velocityX = -boid.velocityX
        if boid.y < border and boid.velocityY < 0:
            boid.velocityY = -boid.velocityY
        if boid.y > height - border and boid.velocityY > 0:
            boid.velocityY = -boid.velocityY


    # Pygame routine
    screen.fill(black)
    for boid in boids:
        kind_boid = pygame.Rect(ballrect) # Rectangular kind_boid object

        # Coordinates transferring
        kind_boid.x = boid.x
        kind_boid.y = boid.y
        screen.blit(ball, kind_boid) # Image of a boid and its object
    pygame.display.flip()    # Refresh screen

    if time() - t0 >= opts.time:
        break
# End! ;-)