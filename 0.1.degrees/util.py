class Node():
    # This is the constructor: self means this in java and the others are attributes
    def __init__(self, state, parent, action):
        self.state = state      # the individual person(actor) is the state
        self.parent = parent    # the previous person(actor) is the parent
        self.action = action    # the movie that joins these two actors is the action



class StackFrontier():   # First In Last Out  --OR--  Last In First Out 
    def __init__(self):
        self.frontier = []   # just has one attribute which is an empty list. 
                             # This empty list represents the initial state of the frontier.
                             # Remember that the frontier is the data structure that we use for checking
                             # each node one by one in order to determine if it has the goal state.
                               

    # As we studied, the following are the actions that we will be able to perform on the frontier.
    
    # This adds a node (an object of the class Node) to the frontier we have (list-like structure).
    def add(self, node):
        # adds a node at the end of the frontier
        self.frontier.append(node)

    # Tells us if the frontier already contains a node with the given state.
    # This will tell us whether the actor is already present in the frontier or not.
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    # This tells us whether the frontier is empty or not.
    #  This will allow us to determine if there are any actors left in the frontier or not.
    def empty(self):
        return len(self.frontier) == 0

    # This gives takes out and gives us the last node that we had put in the frontier.
    # This implements a stack. The last node that went in the frontier will come out first.
    def remove(self):
        # We can't get anything from the frontier if the it is empty that is why an exception is thrown.
        if self.empty():
            raise Exception("empty frontier")
        else:
            # access the node present at the end of the frontier
            node = self.frontier[-1]
            
            # remove that node from the frontier. Can't we use .pop()?  (?)
            self.frontier = self.frontier[:-1]  
            
            # gives us the node back
            return node


# This class implements the frontier but with a queue. 
# Now we follow the rules of a queue when we are adding and removing nodes from the frontier.
# This comes from (is a child class of the) StackFrontier class
class QueueFrontier(StackFrontier):

    # It just overrode the .remove() method to implement a queue.
    # Note that this is a classical example of polymorphism.
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        # This implements the First In First Out --OR-- Last In Last Out structure (just like at an ATM)
        else:
            # access the node present at the start of the frontier
            node = self.frontier[0]
            
            # remove the element present at the start of the frontier
            self.frontier = self.frontier[1:]
            
            # give us back the node
            return node
