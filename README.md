# Robots
A couple of collective intelligence algorithms implemented.

# Dependencies

Python >= 3.4
pygame 1.9.3

# Flocking

The flocking folder contains code for the flocking problem (swarm problem).

There is a nice description of the problem in this wikipedia article:

https://en.wikipedia.org/wiki/Flocking_(behavior)

# Usage

Inside the flocking folder type on the command line:
python flocking.py

The result will be:

<a href="https://imgflip.com/gif/27cbk4"><img src="https://i.imgflip.com/27cbk4.gif" title="made at imgflip.com"/></a>

It is also possible add some flags in order to change some variables. The command:

python flocking.py --n_boids=50 --time=20  

will execute the program for 20 seconds and with 50 boids. Type python flocking.py -h
to get more details about the flags available.

# Formation

The formation folder contains code for the flocking-formation problem. Robots following a leader.

The solution was inspired in the algorithm described in the article of Vincenzo Gervasi and
Giuseppe Prencipe: Coordination without communication:the case of the flocking problem.

https://github.com/igorbpf/Robots/blob/master/formation/Coordination_without_communication.pdf

The possible formations are V, Moose, M, Arrow, U, Line for a even number of followers (8 boids)
and their degenerations with a odd number of followers (9 boids): V-odd, Moose-odd, M-odd, Arrow-odd, U-odd,
Line-odd. However, some of these odd formations are quite unstable.


# Usage

Inside the formation folder type on the command line:
python formation.py

The result will be:

for even number of boids

<a href="https://imgflip.com/gif/27cgzs"><img src="https://i.imgflip.com/27cgzs.gif" title="made at imgflip.com"/></a>

for odd number of boids

<a href="https://imgflip.com/gif/27cfom"><img src="https://i.imgflip.com/27cfom.gif" title="made at imgflip.com"/></a>

It is also possible add some flags in order to change some variables. The command:

python formation.py --formation=V --time=30  

will execute the program for 30 seconds and with the V formation. Type python flocking.py -h
to get more details about the flags available.
