"""
The set of all possible outcomes of a random experiment is called the sample space of the experiment.

An event is defined as a particular subset of the sample space to be considered.
For any given event, only one of two possibilities may hold: it occurs or it does not.

The relative frequency of occurrence of an event, observed in a number of repetitions of the experiment,
is a measure of the probability of that event.

We assume that the relative frequency converges to a value as the number of trials increases.

Therefore, according to the frequency interpretation of probability, an event's probability is the limit of the relative
frequency of the event as the number of trials approaches infinity.
"""

def freq_prob(convergence_tolerance, initial_num_trials, max_num_iter, random_experiment):

    """
    Calculates the frequentist probability by simulating trials of a random experiment until the relative frequency converges.

    The first simulation calculates the relative frequency resulting from running 'initial_num_trials' trials of the experiment.

    Each succesive simulation increases number of trials by 'initial_num_trials'.

    The function keeps on running simulations until the resulting series of relative frequencies converges or the maximum number of
    iterations, 'max_num_iter' is reached.

    'random_experiment' is a function that takes as parameters:
        - the number of trials to simulate
        - the wanted result
    and returns the relative frequency of the wanted result

    Returns
    -------
    tuple

        first element of the tuple is the probability as limit of the relative frequencies
        second element is the number of trials used to reach the limit

    """

    gen = freq_generator(initial_num_trials, random_experiment)
    last_result = next(gen)
    num_iter = 1

    while num_iter <= max_num_iter:        
        new_result = next(gen)        
        if abs(new_result[0] - last_result[0]) <= convergence_tolerance:            
            return new_result
        last_result = new_result
        num_iter += 1
    return (-1, last_result[1])


def freq_generator(initial_num_trials, random_experiment):
    num_trials = initial_num_trials

    while True:
        yield (random_experiment(num_trials), num_trials)
        num_trials = num_trials + initial_num_trials
