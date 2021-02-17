# Distance Vector project for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related 
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This 
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, Jeffrey Randow, new VM fixes by Jared Scott and James Lohse.

from Node import *
from helpers import *
import copy


class DistanceVector(Node):
    
    def __init__(self, name, topolink, outgoing_links, incoming_links):
        """ Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here."""

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)
        
        # TODO: Create any necessary data structure(s) to contain the Node's internal state / distance vector data
        # create a dictionary to store the distance information
        self.vector = {self.name: 0}

    def send_initial_messages(self):
        """ This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here. 

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight """

        # TODO - Each node needs to build a message and send it to each of its neighbors
        # HINT: Take a look at the skeleton methods provided for you in Node.py

        # leverage the function send_msg in Node.py
        for neighbor in self.neighbor_names:
            #print("going to send massage from "+str(self.name)+" to "+str(neighbor))
            msg = [self.name, self.vector]
            self.send_msg(msg, neighbor)

    def process_BF(self):
        """ This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. """

        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:
        # TODO 1. Process queued messages       
        # save previous vector to determine if there are any updates needed to send
        # previously use "=" won't work as it assign to the same object
        # needs deep copy to get value
        # https://stackoverflow.com/questions/3975376/understanding-dict-copy-shallow-or-deep
        
        prev_vector = copy.deepcopy(self.vector) 
  
        for msg in self.messages:    
            # msg[0] is the origin node's name
            # msg[1] is the origin node's vector (dictionary)     

            # logic here is to get information from its downstream and update the vector

            # print("now node "+str(self.name)+" starts to process messge from "+str(msg[0]))

            for neighbor in msg[1].keys():
                # if receive info about itself, ignore and keep the value at 0
                # print("it's neighbor "+str(neighbor))
                # print("distance from node to neighbor is "+str(self.get_outgoing_neighbor_weight(msg[0])))

                if neighbor == self.name:
                    continue
                # if there was no info exist, then add 
                elif neighbor not in self.vector.keys():
                    #print(self.get_outgoing_neighbor_weight(msg[0]))
                    #print(msg[1][neighbor])
                    self.vector[neighbor] = int(self.get_outgoing_neighbor_weight(msg[0])) + msg[1][neighbor]
                # if there is negative cycle, stop at -99 
                elif self.vector[neighbor] <= -99:
                    self.vector[neighbor] = -99
                # if the updated information from neighbor suggested negative cycle, no need to do any calculation
                elif msg[1][neighbor] <= -99:
                    self.vector[neighbor] = -99
                # if the updated distance is shorter, update it
                elif int(self.get_outgoing_neighbor_weight(msg[0])) + msg[1][neighbor] < self.vector[neighbor]:
                    self.vector[neighbor] = int(self.get_outgoing_neighbor_weight(msg[0])) + msg[1][neighbor]

        # Empty queue
        self.messages = []

        # TODO 2. Send neighbors updated distances
        if prev_vector == self.vector:
            return       
        else:
            msg = [self.name, self.vector]
            for neighbor in self.neighbor_names:
                self.send_msg(msg, neighbor)
    
    def log_distances(self):
        """ This function is called immedately after process_BF each round.  It 
        prints distances to the console and the log file in the following format (no whitespace either end):
        
        A:A0,B1,C2
        
        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 """
        
        # TODO: Use the provided helper function add_entry() to accomplish this task (see helpers.py).
        # An example call that which prints the format example text above (hardcoded) is provided. 
        lst_out = []
        for neighbor in self.vector.keys():
            lst_out.append(neighbor+str(self.vector[neighbor]))
        add_entry(self.name, ','.join(lst_out))        
