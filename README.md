# Medium.com writeup
[link](https://jl4730.medium.com/bellman-ford-algorithm-in-distance-vector-dv-routing-protocol-b9f36a45cd54)

# Files

## DistanceVector.py
It is a specialization (subclass) of the Node class that represents a network node (i.e., router) running the Distance Vector algorithm

## Node.py
Represents a network node, i.e., a router

## Topology.py
Represents a network topology. It's a container class for a collection of DistanceVector Nodes and the network links between them
 
## run_topo.py
A simple “driver” that loads a topology file (see *Topo.txt below), uses that data to create a Topology object containing the network Nodes, and starts the simulation

## helpers.py
This contains logging functions that implement that majority of the logging code
 
## xxxTopo.txt
These are valid topology files that will pass as input to the run.sh scrip

## BadTopo.txt
This is an invalid topology file, provided as an example of what not to do, and so you can see what the program says if you pass it a bad topology
 
## output_validator.py
This script can be run on the log output from the simulation to verify that the output file is formatted correctly. It does not verify that the contents are correct, only the format

## run.sh
Helper script that launches the simulation on a specified topology and automatically runs the output validator on the log output when the simulation finishes; basically a convenient wrapper for run_topo.py and output_validator.py

# Tesing
To run your algorithm on a specific topology, execute the run.sh bash script:
```
./run.sh *Topo
```
NOTE: Substitute the correct, desired filename for *Topo. Don’t use the .txt suffix on the command line. This will execute your implementation of the algorithm in DistanceVector.py on the topology defined in *Topo.txt and log the results (per your logging function) to *Topo.log
