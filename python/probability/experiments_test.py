from experiments import dice_roll, two_dice_roll, two_dice_roll_classical, balls_draw_classical, balls_draw, married_couples, married_couples_theoretical


def test_dice_roll():
    assert dice_roll(1000, 1) - 1/6 < 0.1


def test_two_dice_roll_classical():
    assert two_dice_roll_classical(7) == 1/6


def test_two_dice_roll():
    assert abs(two_dice_roll(1000, 7) - two_dice_roll_classical(7)) < 0.1


def test_balls_draw_classical():
    """
    If 3 balls are “randomly drawn” from a bowl containing 6 white and 5 black balls, 
    what is the probability that one of the balls is white and the other two black?
    """
    assert balls_draw_classical(white=6, black=5, drawn=3, white_wanted=1) == 4/11


def test_balls_draw():
    assert abs(balls_draw(white=6, black=5, drawn=3, white_wanted=1)(num_trials=1000) - balls_draw_classical(white=6, black=5, drawn=3, white_wanted=1)) < 0.1


def test_married_couples_theroretical():
    """
    Probability that 10 married couples are seated at random at a round table, then no wife sits next to her husband.
    """
    assert abs(married_couples_theoretical(10) - 0.3395) < 0.001

def test_married_couples():
    assert abs(married_couples(10, 100000) - married_couples_theoretical(10)) < 0.01
