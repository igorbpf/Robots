# Robots
A couple of collective intelligence algorithms implemented.

# Flocking

The flocking folder contains code for the flocking problem (swarm problem). 

There is a nice description of the problem in this wikipedia article:

https://en.wikipedia.org/wiki/Flocking_(behavior)

# Dependencies

pygame 1.9.1

# Usage

On the command line:
python flocking.py

The result will be:

![alt tag](https://github.com/igorbpf/Robots/blob/master/images/flocking_demo.png)

It is also possible add some flags in order to change some variables. The command:

python flocking.py --n_boids=50 --n_time=20  

will execute the program for 20 seconds and with 50 boids. Type python flocking.py -h
to get more details about the flags available.





