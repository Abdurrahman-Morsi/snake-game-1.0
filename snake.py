from turtle import Turtle
import random


class Snake:
    """A class representing the snake in the Snake game."""
    SEGMENT_SIZE = 20  # Size of each snake segment
    SCREEN_BOUNDARY = 300  # Boundary of the game screen
    
    def __init__(self):
        """Initialize the Snake object."""
        self.direction = "right" # Initial direction of the snake
        self.segments = [] # List to store the snake's segments
        self.positions = [] # List to store the positions of the snake's segments
        self.alive = True # Flag to indicate whether the snake is alive
        self.on_move = False # Flag to indicate if the snake is currently moving
         # Dictionary mapping directions to coordinate increments
        self.directions = {"right": {"x": self.SEGMENT_SIZE,"y":0}, 
                           "left": {"x": -self.SEGMENT_SIZE,"y": 0}, 
                           "up": {"x": 0,"y": self.SEGMENT_SIZE}, 
                           "down": {"x":0,"y": -self.SEGMENT_SIZE}
        }
        # Create initial segments of the snake
        for i in range(3):
            segment = Turtle(shape="square")
            segment.color("#612f01")
            segment.penup()
            position = (i* -self.SEGMENT_SIZE + 10),10
            segment.goto(position)
            self.positions.append(position)
            self.segments.append(segment)
        self.size = 3
        self.last_pos = self.positions[-1]
    def up(self):
        """Change the snake's direction to 'up'."""
        if self.direction != "down" and not self.on_move:
            self.on_move = True
            self.direction = "up"
    
    def down(self):
        """Change the snake's direction to 'down'."""
        if self.direction != "up" and not self.on_move:
            self.on_move = True
            self.direction = "down"
                   
    def right(self):
        """Change the snake's direction to 'right'."""
        if self.direction != "left" and not self.on_move:
            self.on_move = True
            self.direction = "right"
    
    def left(self):
        """Change the snake's direction to 'left'."""
        if self.direction != "right" and not self.on_move:
            self.on_move = True
            self.direction = "left"

    def move(self):
        """Move the snake forward one step."""
        new_step = self.next_position()
        if self.alive:
            self.last_pos = self.positions[-1]
            self.segments[-1].goto(new_step)
            self.segments.insert(0,self.segments.pop(-1))
            self.positions.pop()
            self.segments[-1].color("#612f01")
            self.positions.insert(0,new_step)
        
    
    def add_segment(self, my_color):
        """Add a new segment to the snake."""
        self.segments[0].color(my_color)
        segment = Turtle(shape="square")
        segment.color("#612f01")
        segment.penup()
        new_step = self.last_pos
        segment.goto(new_step)
        self.segments.append(segment)
        self.positions.append(new_step)
        self.move()

    
    def next_position(self):
        """Calculate the next position of the snake's head."""
        self.on_move = True
        x = self.segments[0].pos()[0] + self.directions[self.direction]["x"]
        y = self.segments[0].pos()[1] + self.directions[self.direction]["y"]
        position = x, y
        self.on_move = False
        if -300 < x < 300 and -300 < y < 300:
            if position in self.positions[1:-1]:
                self.alive = False
        else:
            self.alive = False
                
        return position

        

