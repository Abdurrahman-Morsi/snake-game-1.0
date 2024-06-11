from turtle import Turtle
import random

class Food(Turtle):
    """A class representing the food in the Snake game."""
    
    SEGMENT_SIZE = 20  # Size of each snake segment
    SCREEN_BOUNDARY = 300  # Boundary of the game screen
    COLORS = {"#17023b", "#17023b", "#c40260", 
              "#c4020c", "#0215c4", "#00031a", 
              "#001a12", "#05966d", "#965a05", 
              "#f59105", "#f52105", "#7d0f00", 
              "#b6fc05"}


    def __init__(self, seg_positions):
        """Initialize the Food object."""
        super().__init__()
        range_x = range(-self.SCREEN_BOUNDARY + self.SEGMENT_SIZE//2, self.SCREEN_BOUNDARY, self.SEGMENT_SIZE)
        range_y = range(-self.SCREEN_BOUNDARY + self.SEGMENT_SIZE//2, self.SCREEN_BOUNDARY, self.SEGMENT_SIZE)
        self.available_positions = {(i, j) for i in range_x for j in range_y}
        self.my_color = ""

        self.shape("circle")
        self.change_color()
        self.speed("fastest")
        self.shapesize(0.5)
        self.penup()
        self.hideturtle()
        self.food_pos = self.get_position(seg_positions)
        self.goto(self.food_pos)
        self.showturtle()

    def change_place(self, seg_positions):
        """Change the position and the color of the food."""
        self.change_color()
        self.hideturtle() 
        self.food_pos = self.get_position(seg_positions)
        self.goto(self.food_pos)
        self.showturtle()

    def get_position(self, seg_positions):
        """Get a random position for the food."""
        available_positions = list(self.available_positions ^ set(seg_positions))
        food_pos = random.choice(available_positions)
        return food_pos
    def change_color(self):
        self.my_color = random.choice(list(self.COLORS.difference(self.my_color)))
        self.color(self.my_color)