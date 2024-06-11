import pytest
from unittest.mock import Mock, call
from project import play_again, generate_screen, get_highest_score
from snake import Snake
from scoreboard import Scoreboard
from food import Food
import turtle
from turtle import Turtle
import random
from background import BackGround

@pytest.fixture
def screen_mock():
    return Mock()


@pytest.fixture
def snake():
    return Snake()


@pytest.fixture
def scoreboard():
    return Scoreboard()


@pytest.fixture
def food():
    return Food([(0, 0), (20, 0), (40, 0)])  # Example list of snake positions


@pytest.fixture
def mock_screen():
    screen = Mock()
    screen.update = Mock()
    return screen

@pytest.fixture
def background(mock_screen):
    return BackGround(mock_screen)


def test_play_again(screen_mock):
    # Set up mock scores and name
    scores = {"Player1": 10, "Player2": 20}
    name = "Player1"
    current_score = 15

    # Mock the text input function to return "y" (yes)
    screen_mock.textinput.return_value = "y"

    # Call the function
    result = play_again(screen_mock, "Game Over", current_score, name, scores)

    # Assert that the screen's textinput method was called with the correct arguments
    screen_mock.textinput.assert_called_once_with("Game Over", "Your Highest Score is 15\nDo You want to play again(y,n):")

    # Assert that the function returns True (indicating the player wants to play again)
    assert result == True
    
def test_generate_screen():
    assert isinstance(generate_screen(), turtle._Screen)
    
def test_get_highest_score(mock_screen):
    with open("score_record.csv", "w") as score:
        score.write("Snake,10\n")
    assert get_highest_score("Snake", mock_screen) == ({"Snake": 10}, 10)
    with open("score_record.csv", "w") as score:
        pass
    assert get_highest_score("Snake", mock_screen) == ({"Snake": 0}, 0)

def test_initialization(snake):
    assert len(snake.segments) == 3
    assert len(snake.positions) == 3

def test_movement(snake):
    initial_position = snake.segments[0].position()
    snake.up()
    snake.move()
    new_position = snake.segments[0].position()
    assert initial_position != new_position

@pytest.mark.parametrize("directions", [
    ("up", "down"),
    ("down", "up"),
    ("left", "right"),
    ("right", "left")
])
def test_movement_directions(snake, directions):
    initial_direction, opposite_direction = directions
    getattr(snake, initial_direction)()
    snake.move()
    direction_before = snake.segments[0].heading()
    getattr(snake, opposite_direction)()
    snake.move()
    assert snake.segments[0].heading() == direction_before

def test_growth(snake):
    initial_length = len(snake.segments)
    snake.add_segment("#ffffff")
    new_length = len(snake.segments)
    assert new_length == initial_length + 1

def test_collision_boundary(snake):
    while snake.alive:
        snake.move()
    assert not snake.alive
    
    snake = Snake()
    snake.segments[0].goto((40, 0))
    snake.segments[1].goto((20, 0))
    snake.segments[2].goto((0, 0))
    snake.add_segment("#ffffff")
    snake.add_segment("#ffffff")
    
    snake.right()
    snake.move() 
    snake.down()
    snake.move()
    snake.left()
    snake.move()
    snake.up()
    snake.move()
    
    assert not snake.alive


def test_initialization_default_name(scoreboard):
    assert scoreboard.name == "Score"

def test_initialization_custom_name():
    custom_name = "Player"
    scoreboard = Scoreboard(custom_name)
    assert scoreboard.name == custom_name

def test_update_scoreboard(scoreboard):
    initial_score = scoreboard.score
    scoreboard.change_score()
    assert scoreboard.score == initial_score + 1

def test_change_score(scoreboard):
    initial_score = scoreboard.score
    scoreboard.change_score()
    assert scoreboard.score == initial_score + 1

def test_init_food_position(food):
    assert food.food_pos in food.available_positions

def test_init_food_color(food):
    c = "#"+"".join(map(lambda x: hex(int(x*255)).strip("0x").rjust(2, "0"), food.color()[0])) # store the color as hexadecimal value
    assert c in food.COLORS

def test_change_place(food):
    initial_position = food.food_pos
    initial_color = food.color()[0]

    food.change_place([(0, 0), (20, 0), (40, 0)])
    assert food.food_pos != initial_position
    assert food.color()[0] != initial_color

def test_get_position(food):
    seg_positions = [(0, 0), (20, 0), (40, 0)]
    pos = food.get_position(seg_positions)
    assert pos not in seg_positions
    assert pos in food.available_positions

def test_initialization(background, mock_screen):
    assert background.SIZE == 50
    assert background.WIDTH == 600
    assert background.HEIGHT == 600
    assert background.screen == mock_screen

def test_draw_method(background, mock_screen):
    background.goto = Mock()
    background.penup = Mock()
    background.hideturtle = Mock()
    background.pendown = Mock()
    background.pencolor = Mock()
    background.setheading = Mock()
    background.fd = Mock()
    background.draw_cell = Mock()
    background.draw()

    assert background.penup.called
    assert background.hideturtle.called
    

def test_draw_cell_method(background):
    background.color = Mock()
    background.goto = Mock()
    background.pendown = Mock()
    background.setheading = Mock()
    background.begin_fill = Mock()
    background.fd = Mock()
    background.right = Mock()
    background.penup = Mock()
    background.end_fill = Mock()
    
    x, y = 0, 0
    bg_color = "#193601"
    background.draw_cell(x, y, bg_color)

    background.color.assert_called_with(bg_color)
    background.goto.assert_called_with(x, y)
    assert background.pendown.called
    assert background.begin_fill.called
    background.fd.assert_has_calls([call(background.SIZE)] * 4)
    background.right.assert_has_calls([call(90)] * 4)
    assert background.penup.called
    assert background.end_fill.called
