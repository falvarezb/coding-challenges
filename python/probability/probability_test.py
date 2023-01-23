from functools import partial
from experiments import dice_roll
from probability import freq_generator, freq_prob

def test_freq_generator():
    gen = freq_generator(1000, partial(dice_roll, wanted_result=1))
    result = [next(gen) for j in range(2)]

    assert 0 <= result[0][0] <= 1
    assert result[0][1] == 1000

    assert 0 <= result[1][0] <= 1
    assert result[1][1] == 2000


def test_freq_prob():
    result = freq_prob(0.0001, 1000, 1000, partial(dice_roll, wanted_result=1))
    assert abs(result[0] - 1/6) < 0.01
