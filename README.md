# Robots
A couple of collective intelligence algorithms implemented.

# Dependencies

pygame 1.9.1

# Flocking

The flocking folder contains code for the flocking problem (swarm problem). 

There is a nice description of the problem in this wikipedia article:

https://en.wikipedia.org/wiki/Flocking_(behavior)

# Usage

On the command line:
python flocking.py

The result will be:

![alt tag](https://github.com/igorbpf/Robots/blob/master/images/flocking_demo.png)

It is also possible add some flags in order to change some variables. The command:

python flocking.py --n_boids=50 --time=20  

will execute the program for 20 seconds and with 50 boids. Type python flocking.py -h
to get more details about the flags available.

# Formation

The formation folder contains code for the flocking-formation problem. Robots following a leader.

The solution was inspired in the algorithm described in the article of Vincenzo Gervasi and 
Giuseppe Prencipe: Coordination without communication:the case of the focking problem.

https://github.com/igorbpf/Robots/blob/master/formation/Coordination_without_communication.pdf

The possible formations are V, Moose, M, Arrow, U, Line for a even number of followers (8 boids)
and their degenerations with a odd number of followers (9 boids): V-odd, Moose-odd, M-odd, Arrow-odd, U-odd,
Line-odd. However, some of these odd formations are quite unstable.


# Usage

On the command line:
python formation.py

The result will be:

![alt tag](https://github.com/igorbpf/Robots/blob/master/images/formation_demo.png)

It is also possible add some flags in order to change some variables. The command:

python flocking.py --formation=V --time=30  

will execute the program for 30 seconds and with the V formation. Type python flocking.py -h
to get more details about the flags available.





