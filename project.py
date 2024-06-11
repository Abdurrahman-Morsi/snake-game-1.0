import pygame.mixer
from turtle import Screen
from background import BackGround
from snake import Snake
from food import Food
from scoreboard import Scoreboard
from time import sleep

ALIGNMENT = "left"
FONT = ("Courier", 15, "normal")
HEIGHT = 700
WIDTH = 700
SNAKE_SIZE = 20


# Initialize pygame mixer for sound effects
pygame.mixer.init()

# Load sound effects
bgsound = pygame.mixer.Sound("8-bit-background-music-for-arcade-game-come-on-mario-164702.wav")
game_over_sound = pygame.mixer.Sound("523174__sami_kullstrom__crash-lofi.wav")
eat_sound = pygame.mixer.Sound("eat.wav")

def main():
    """Initialize and start the Snake game."""
    # playing the background sound infinitely
    bgsound.play(-1)
    game_on, name = play()
    while game_on:
        game_on, _ = play(name)

def generate_screen():
    """Instantiate the screen and customize it for the game.
    
    Returns:
        Screen: The customized screen object.
    """
    screen = Screen()
    screen.setup(width=WIDTH, height=HEIGHT)
    screen.bgcolor("#777777")
    background = BackGround(screen)
    screen.title("SNAKE")
    background.draw()
    screen.tracer(0)
    return screen

def config_game(screen, name):
    """Setup the game configuration and difficulty level.
    
    Args:
        screen (Screen): The screen object.
        name (None)|(int): The player's name

    Returns:
        tuple: A tuple containing the difficulty level and player name.
    """
    if name is None:
        name = screen.textinput(title="Welcome To Snake", prompt="What's your name?").title()
    difficulty_level = screen.numinput(title="level", prompt="Difficulty (1-3):\n1-> slowest\n2 -> moderate speed\n3 -> fastest ", default=1, minval=1, maxval=3)
    screen._write(
        pos=(50, 315),
        txt=f"Difficulty level: {int(difficulty_level)}",
        align=ALIGNMENT,
        font=FONT,
        pencolor="white"
    )
    difficulty = 1 / (difficulty_level * 10)
    return difficulty, name

def key_setup(snake, screen):
    """Setup the keys for controlling the snake.
    
    Args:
        snake (Snake): The snake object.
        screen (Screen): The screen object.
    """
    screen.onkey(snake.up, "Up")
    screen.onkey(snake.down, "Down")
    screen.onkey(snake.right, "Right")
    screen.onkey(snake.left, "Left")
    screen.onkey(snake.up, "w")
    screen.onkey(snake.down, "s")
    screen.onkey(snake.right, "d")
    screen.onkey(snake.left, "a")

def play_again(screen, state, current_score, name, scores):
    """Prompt the player to play again or exit.
    
    Args:
        screen (Screen): The screen object.
        state (str): The current state of the game (e.g., "Game Over").
        current_score (int): The player's current score.
        name (str): The player's name.
        scores (dict): A dictionary containing player scores.

    Returns:
        bool: True if the player wants to play again, False otherwise.
    """
    if current_score > scores[name]:
        scores[name] = current_score
        with open("score_record.csv", "w") as new_record:
            for player, score in scores.items():
                new_record.write(f"{player},{score}\n")
    
    play_again = screen.textinput(state, f"Your Highest Score is {scores[name]}\nDo You want to play again(y,n):")
    if play_again is None:
        pass
    elif play_again.lower() in ("y", "yes"):
        screen.clearscreen()
        return True
    
    return False

def get_highest_score(name, screen):
    """Retrieve the highest score for the current player.
    
    Args:
        name (str): The player's name.
        screen (Screen): The screen object.

    Returns:
        tuple: A tuple containing the player score and highest score.
    """
    try:
        with open("score_record.csv", "r+") as file:
            scores = {player: int(score) for player, score in [line.strip().split(",") for line in file if line]}
            if name not in scores:
                scores[name] = 0
            high_score = scores[name]
                
    except FileNotFoundError:
        with open("score_record.csv", "w") as file:
            scores = {name:0}
            high_score = 0
    finally:
        screen._write(
            pos=(50, 300),
            txt=f"Highest Score: {max(scores.values())}",
            align=ALIGNMENT,
            font=FONT,
            pencolor="white"
        )
    return scores, high_score

def play(name=None):
    """Main game loop.
    
    Args:
        name (None)|(str): The current round number.
    """
    # create customized screen
    screen = generate_screen()
    # create snake object
    snake = Snake()
    # setup the game and define difficulty
    difficulty, name = config_game(screen, name)
    scores, highest_score = get_highest_score(name, screen)
    # create food object
    food = Food(snake.positions)
    # create scoreboard
    scoreboard = Scoreboard(name)
    # update screen to show all changes and turtles that have been created
    screen.update()
    # sets up the keys for navigation
    key_setup(snake, screen)
    # make screen response to the chosen keys
    screen.listen()
    
    # stop screen to control animation
    screen.tracer(n= snake.size + 2, delay=0)
    while snake.alive:
        # make snake move in the direction of its head 
        snake.move()
        if food.pos() == snake.segments[0].pos():
            # play the eating sound
            eat_sound.play()
            # increment the score by one and increase the snake's segments by one
            scoreboard.change_score()
            snake.add_segment(food.my_color)
            # check if the game comes to an end by occupying all the playing screen by the snake
            snake.size += 1
            if snake.size == 841:
                screen.clearscreen()
                return play_again(screen, "Congratulations You won", scoreboard.score, name, scores)
            # change the food's location on the board
            food.change_place(snake.positions)
        # update the screen to the happening move    
        screen.update()
        # stop the program to make the animation so the snake will appear to be move by the rate of that amount delaying
        sleep(difficulty)
    # play the game over sound
    game_over_sound.play()
    snake.segments[0].color("red")
    screen.update()
    return play_again(screen, "Game Over", scoreboard.score, name, scores), name

if __name__ == "__main__":
    main()
