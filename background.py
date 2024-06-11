from turtle import Turtle

class BackGround(Turtle):
    """A class representing the background grid in the game."""
    COLOR = "#336b02"
    def __init__(self, screen):
        """Initialize the Background object."""
        super().__init__()
        self.SIZE = 50  # Size of each grid cell
        self.WIDTH = 600  # Width of the game screen
        self.HEIGHT = 600  # Height of the game screen
        self.screen = screen  # Screen to be rendered on

    def draw(self):
        """Draw the background grid."""
        self.penup()
        self.hideturtle()
        self.pen(fillcolor=self.COLOR, pencolor=self.COLOR)
        self.screen.tracer(0)
        
        self.goto(-self.WIDTH//2, self.HEIGHT//2)
        
        # Draw grid lines
        for i in range(-self.WIDTH // 2, self.WIDTH // 2, self.SIZE):
            for j in range(self.HEIGHT // 2, -self.HEIGHT // 2, -self.SIZE):
                if (i // self.SIZE + j // self.SIZE) % 2 == 0:
                    self.draw_cell(i, j)
                else:
                    self.draw_cell(i, j, "#193601")
        self.goto(-self.WIDTH//2, self.HEIGHT//2)
        self.pendown()
        self.pencolor("#000000")
        for heading in range(0,-360,-90):
            self.setheading(heading)
            self.fd(self.WIDTH)
        self.penup()
        self.setheading(0)
        
        self.screen.update()

    def draw_cell(self, x, y, bg_color=COLOR):
        """Draw a single grid cell."""
        self.color(bg_color)
        self.goto(x, y)
        self.pendown()
        self.setheading(0)
        self.begin_fill()
        for _ in range(4):
            self.fd(self.SIZE)
            self.right(90)
        self.penup()
        self.end_fill()
