#!usr/bin/env

# Author: Igor Santos
# License: MIT

"""
Possible formations are V, Moose, M, Arrow, U, Line for a even number of followers (8 boids)
and their degenerations with a odd number of followers (9 boids): V-odd, Moose-odd, M-odd, Arrow-odd, U-odd,
Line-odd
"""

# Python modules
from __future__ import division
import random
import sys
from optparse import OptionParser
from time import time
import math

# third-party modules
import pygame

# parse commandline arguments
op = OptionParser()

op.add_option("--formation", type=str, default="V",
              help="Formation of the boids following the leader. The default is 'V' formation.")
op.add_option("--time", type=int, default=20,
              help="Time of execution. The default is 20 seconds.")

(opts, args) = op.parse_args()
if len(args) > 0:
    op.error("this script takes no arguments.")
    sys.exit(1)

t0 = time()

print(__doc__)

class Leader(object):

	def __init__(self):
		self.x = random.uniform(30,1000)
		self.y = random.uniform(30,600)
		self.velX = random.uniform(0,1)
		self.velY = random.uniform(0,1)

	# Calculate the distance between the leader and point on the plane.
	def Distance(self, x, y):
		d = ((self.x - x)**2 + (self.y - y)**2)**0.5
		return d

	# Refresh the position and velocity of the leader.
	def Move(self):

		self.velX = random.uniform(0,0.2)
		self.velY = random.uniform(0,0.2)
		self.x = self.x + self.velX
		self.y = self.y + self.velY

# Class Follower inherits Leader
class Follower(Leader):
	def __init__(self, formation):
		Leader.__init__(self)
		self.formation = formation

	# Find the barycenter of the group of followers.
	def Baricenter(self, followers):
		bx = 0
		by = 0
		for follower in followers:
			bx = bx + follower.x
			by = by + follower.y
		n = len(followers)
		return bx/n , by/n

	# Define the positions of the followers relative to the line which goes from the leader to the barycenter.
	def Party(self,followers, leader, Xb, Yb):
		S0 = [] 			# Followers on the line between the leader and the baricenter
		S1 = [] 			# Followers on the left
		S2 = []				# Followers on the right

		for follower in followers:
			s = 0
			s =  (leader.x - Xb) * (follower.y - Yb) - (leader.y - Yb) * (follower.x - Xb)
			if s == 0:
				S0.append(follower)
			elif s > 0:
				S1.append(follower)
			else:
				S2.append(follower)

		return S0, S1, S2

	# Define the possible positions of the followers according to the formation chosen.
	def FinalPositions(self, leader, Xb, Yb, formation):
		s = 0
		slotsGlobal = []
		fakeFollowers = []
		xsb = 0
		ysb = 0

		# The local reference system of coordinates is on the leader and the inertial one is at the top left side
		# The coordinates of the formation are taken relatively to the local system.
		if formation == 'V':
			slots = [[40,-40],[80,-80],[120,-120],[160, -160],[-40,-40],[-80,-80],[-120,-120],[-160,-160]]
		if formation == 'Moose':
			slots = [[40,-40],[80,-80],[80,-120],[80, -160],[-40,-40],[-80,-80],[-80,-120], [-80, -160]]
		if formation == 'M':
			slots = [[40,-40],[80,-80],[120,-120],[120, -40],[-40,-40],[-80,-80],[-120,-120],[-120, -40]]
		if formation == 'Arrow':
			slots = [[40,-40],[80,-80],[120,-120],[40, -250],[-40,-40],[-80,-80],[-120,-120],[-40, -250]]
		if formation == 'U':
			slots = [[40, 0],[40,-40],[40,-80],[40, -120],[-40, 0],[-40,-40],[-40,-80], [-40, -120]]
		if formation == 'Line':
			slots = [[40,-40],[80,-40],[120,-40],[160, -40],[-40,-40],[-80, -40],[-120,-40],[-160, -40]]

		"""
		 According to the paper of Vicenzo Gervasi and Giuseppe Prencipe is possible to put a boid in the line
		 of symmetry of the formation. However, I couldn't make it and didn't find where is the problem. So as solution
		 I shifted a little bit the position X which was supposed to be in the symmetry line. X = 0.0001 instead of
		 being 0.
		"""
		if formation == 'V-odd':
			slots = [[40,-40],[80,-80],[120,-120],[160, -160],[-40,-40],[-80,-80],[-120,-120],[-160,-160],[0.0001,-160]]
		if formation == 'Moose-odd':
			slots = [[40,-40],[80,-80],[80,-120],[80, -160],[-40,-40],[-80,-80],[-80,-120], [-80, -160],[0.00001,-160]]
		if formation == 'M-odd':
			slots = [[40,-40],[80,-80],[120,-120],[120, -40],[-40,-40],[-80,-80],[-120,-120],[-120, -40],[0.00001,-200]]
		if formation == 'Arrow-odd':
			slots = [[40,-40],[80,-80],[120,-120],[40, -250],[-40,-40],[-80,-80],[-120,-120],[-40, -250],[0.00001,-120]]
		if formation == 'U-odd':
			slots = [[40, 0],[40,-40],[40,-80],[40, -120],[-40, 0],[-40,-40],[-40,-80], [-40, -120],[0.00001,-200]]
		if formation == 'Line-odd':
			slots = [[40,-40],[80,-40],[120,-40],[160, -40],[-40,-40],[-80, -40],[-120,-40],[-160, -40],[0.00001,-260]]

		##########################
		# Translation and rotation
		#
		# The positions of the followers and the leader are taken relatively to the inertial (Global) system.
		# So translation and rotation are needed.
		# This part of the code takes the positions in the formations which are written in the local system and
		# writes then in the Global system.
		#
		# The goal of this part is to find the angle gama.
		vfx = leader.x - Xb
		vfy = leader.y - Yb
		norm_vf = leader.Distance(Xb, Yb)
		norm_leaderVel = (leader.velX**2 + leader.velY**2)**0.5
		cos_theta = (leader.velX*vfx + leader.velY*vfy)/(norm_vf * norm_leaderVel)
		theta = math.acos(cos_theta)

		halfx = leader.x/2
		if leader.velX != 0:
			halfy = leader.y - (leader.velY/leader.velX)*halfx
		else:
			halfy = leader.y

		s =  (leader.x - halfx) * (Yb - halfy) - (leader.y - halfy) * (Xb - halfx)

		if s > 0 :
			theta = -theta

		cos_alpha_y = leader.velY/norm_leaderVel
		cos_alpha_x = leader.velX/norm_leaderVel
		alpha = math.acos(cos_alpha_y)
		if (cos_alpha_y < 0 and cos_alpha_x > 0) or (cos_alpha_y > 0 and cos_alpha_x > 0):
			alpha = - alpha

		gama = alpha + theta

		for slot in slots:
			xs = slot[0]
			ys = slot[1]

			xs0 = xs*math.cos(gama) - ys*math.sin(gama)
			ys0 = xs*math.sin(gama) + ys*math.cos(gama)

			xsf = xs0 + leader.x
			ysf = ys0 + leader.y

			xsb = xsb + xsf
			ysb = ysb + ysf
			slotsGlobal.append([xsf, ysf])

		# Position of the barycenter of the formation
		Xbf = xsb/len(slots)
		Ybf = ysb/len(slots)

		for i in xrange(len(slots)):
			fake = Follower(formation)
			fake.x = slotsGlobal[i][0]
			fake.y = slotsGlobal[i][1]
			fakeFollowers.append(fake)

		F0, F1, F2 = self.Party(fakeFollowers, leader,Xbf, Ybf)

		return F0, F1, F2, Xbf, Ybf

	# Sort the parties according to the descending order to the barycenter.
	def Sort(self, leader, X, Y, C0, C1, C2):
		D0 = []
		D1 = []
		D2 = []
		E0 = []
		E1 = []
		E2 = []

		for element in C0:
			D0.append([element, element.Distance(leader.x, leader.y), element.Distance(X,Y)])

		for element in C1:
			D1.append([element, element.Distance(leader.x, leader.y), element.Distance(X,Y)])

		for element in C2:
			D2.append([element, element.Distance(leader.x, leader.y), element.Distance(X,Y)])

		D0.sort(key = lambda x: x[2], reverse = True)
		D0.sort(key = lambda x: x[1], reverse = True)
		for d in D0:
			E0.append(d[0])

		D1.sort(key = lambda x: x[2], reverse = True)
		D1.sort(key = lambda x: x[1], reverse = True)
		for d in D1:
			E1.append(d[0])

		D2.sort(key = lambda x: x[2], reverse = True)
		D2.sort(key = lambda x: x[1], reverse = True)
		for d in D2:
			E2.append(d[0])


		return E0, E1, E2

	# Refresh the follower position
	def Move(self, F, k):
		x = F[k - 1].x
		y = F[k - 1].y
		if self.Distance(x,y) <= 10:
			self.x = x
			self.y = y
		else:
			self.velX = x - self.x
			self.velY = y - self.y
			self.x = self.x + 0.2 * random.uniform(0.1,0.8)*self.velX
			self.y = self.y + 0.2 * random.uniform(0.1,0.8)*self.velY

	# This method applies the algorithm of the paper. Check the paper for clarification.
	def Formation(self, followers, leader):
		Xb, Yb = self.Baricenter(followers)
		S0, S1, S2 = self.Party(followers, leader, Xb, Yb)
		F0, F1, F2, Xbf, Ybf = self.FinalPositions(leader, Xb, Yb, self.formation)
		F0, F1, F2 = self.Sort(leader, Xbf, Ybf, F0, F1, F2)
		S0, S1, S2 = self.Sort(leader, Xb, Yb, S0, S1, S2)
		H = []

		for boid in S1:
			if (S1.index(boid) + 1) > len(F1):
				H.append(boid)
		for boid in S2:
			if (S2.index(boid) + 1 > len(F2)):
				H.append(boid)

		if self in S1:
			k = S1.index(self) + 1
			if k <= len(F1):
				self.Move(F1, k)
			elif k <= (len(F1) + len(F0) - len(S0)):
				H, [], [] = self.Sort(leader, Xb, Yb, H, [], [])
				k_prime = H.index(self) + 1
				p = k_prime + len(S0)
				self.Move(H, p)
			else:
				p = len(F2) - (k - len(F1) - len(F0) + len(S0)) + 1
				self.Move(F2, p)

		if self in S2:
			k = S2.index(self) + 1
			if k <= len(F2):
				self.Move(F2, k)
			elif k <= (len(F2) + len(F0) - len(S0)):
				H, [], [] = self.Sort(leader, Xb, Yb, H, [], [])
				k_prime = H.index(self) + 1
				p = k_prime + len(S0)
				self.Move(H, p)
			else:
				p = len(F1) - (k - len(F2) - len(F0) + len(S0)) + 1
				self.Move(F1, p)

		if self in S0:
			k = S0.index(self) + 1
			if k <= len(F0):
				self.Move(F0, k)
			elif len(S1) <= len(S2):
				p = len(F1) - len(S1) + (k - len(F0))
				self.Move(F1, p)
			else:
				p = len(F2) - len(S2) + (k - len(F0))
				self.Move(F2, p)


# Main Routine

pygame.init()

size = width, height = 1250, 700  	# Size of the screen
black = 0, 0, 0 						# Color

screen = pygame.display.set_mode(size) # Screen

pygame.display.set_caption('Formation')	# Title

ballLeader = pygame.image.load('../images/redBall.jpg')
leaderBall = ballLeader.get_rect()

leader = Leader()

followers = []

if opts.formation in ['V', 'Moose', 'M', 'Arrow', 'U', 'Line']:
	nBoids = 8 # number of boids in an even formation
else:
	nBoids = 9 # number of boids in an odd formation

numFollowers = nBoids

for i in xrange(numFollowers):
	followers.append(Follower(opts.formation))

ballFollower = pygame.image.load('../images/smallBall.jpg')
followerBall = ballFollower.get_rect()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

#### Leader ##########

	leader.Move()

	border = 20
	# Keep the leader inside the screen.
	if leader.x < border and leader.velX < 0:
		leader.x = width - border
	if leader.x > width - border and leader.velX > 0:
		leader.x = border
	if leader.y < border and leader.velY < 0:
		leader.y = height - border
	if leader.y > height - border and leader.velY > 0:
		leader.y = border

	screen.fill(black)

	leaderAvatar = pygame.Rect(leaderBall)

	leaderAvatar.x = leader.x
	leaderAvatar.y = leader.y
	screen.blit(ballLeader,leaderAvatar)
#### Leader ####

#### Follower ####
	randomFollower = random.choice(followers)
	randomFollower.Formation(followers, leader)

	for follower in followers:
		followerAvatar = pygame.Rect(followerBall)

		followerAvatar.x = follower.x
		followerAvatar.y = follower.y
		screen.blit(ballFollower, followerAvatar) # Image of a boid and its object
#### Follower ####

	pygame.display.flip() # Refresh screen

	if time() - t0 >= opts.time:
		break

# End ;-)
