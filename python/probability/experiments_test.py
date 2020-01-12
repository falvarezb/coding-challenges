from experiments import dice_roll, two_dice_roll, two_dice_roll_classical, balls_draw_classical, balls_draw

def test_dice_roll():
    assert dice_roll(1000, 1) - 1/6 < 0.1

def test_two_dice_roll_classical():
    assert two_dice_roll_classical(7) == 1/6

def test_two_dice_roll():
    assert abs(two_dice_roll(1000, 7) - two_dice_roll_classical(7)) < 0.1

def test_balls_draw_classical():
    assert balls_draw_classical(white = 6, black = 5, drawn = 3, white_wanted = 1) == 4/11

def test_balls_draw():
    assert abs(balls_draw(white = 6, black = 5, drawn = 3, white_wanted = 1)(num_trials = 1000) - balls_draw_classical(white = 6, black = 5, drawn = 3, white_wanted = 1)) < 0.1




