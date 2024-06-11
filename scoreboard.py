from turtle import Turtle

ALIGNMENT = "left"
FONT = ("Courier", 20, "normal")

class Scoreboard:
    """A class representing the scoreboard in the Snake game."""
    
    def __init__(self, name="Score"):
        """Initialize the Scoreboard object."""
        if len(name) > 17:
            name = name[:15] + ".."
        self.name = name
        self.scorer = Turtle(shape="blank")
        self.scorer.penup()
        self.scorer.pencolor("white")
        self.scorer.goto(-290, 300)  # Initial position of the scoreboard
        self.score = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        """Updates the scoreboard with the current score."""
        self.scorer.clear()
        self.scorer.write(f"{self.name}: {self.score}", align=ALIGNMENT, font=FONT)

    def change_score(self):
        """Increments the score by 1 and update the scoreboard."""
        self.score += 1
        self.update_scoreboard()
