from enum import IntEnum
import questplus as qp
import numpy as np

from audio.sine import sine_tone

VOLUME = 1  # KEEP IN RANGE 0 to 1, otherwise you are summoning CTHULHU!
DURATION = 1.0  # in seconds
SAMPLE_RATE = 44100

LOWER_FREQ = 10
UPPER_FREQ = 100


class Response(IntEnum):
    YES = 1
    NO = 0


# Setting up stimulus parameters
intensity = np.logspace(
    np.log10(UPPER_FREQ), np.log10(LOWER_FREQ), 2 * int(UPPER_FREQ - LOWER_FREQ)
)  # the x values which are used to sample the psychometric function(s)

stim_domain = {
    "intensity": intensity,
}

# Psychometric function parameters
mean = np.linspace(
    UPPER_FREQ, LOWER_FREQ, 2 * int(UPPER_FREQ - LOWER_FREQ)
)  # this corresponds to the mean (i.e., frequency) of the sound
standard_deviation = 1
gamma = 0.5 # this is a 2FAC (i.e., yes-no) test
delta = 0.01 # Assume an error of 1% in user input (e.g., meaning yes but typing no)

param_domain = {
    "mean": mean,
    "sd": standard_deviation,
    "lower_asymptote": gamma,
    "lapse_rate": delta,
}

# response domain
responses = [r.name.lower() for r in Response]
outcome_domain = {"response": responses}


sampler = qp.QuestPlus(
    stim_domain=stim_domain,
    param_domain=param_domain,
    outcome_domain=outcome_domain,
    func="norm_cdf",
    stim_selection_method="min_entropy",
    param_estimation_method="mean",
    stim_scale="log10",
)

num_trials = 20
for trial in range(num_trials):
    next_stim = sampler.next_stim

    # print(f"Trial {trial}: {next_stim}")

    # play the sound
    sine_tone(
        frequency=next_stim["intensity"],
        duration=DURATION,
        volume=VOLUME,
        sample_rate=SAMPLE_RATE,
    )

    # get the response & sanitize it
    user_input = ""
    while user_input not in ["1", "0"]:
        user_input = input(f"Trial {trial + 1}: Did you hear the sound? (1 for yes, 0 for no):")

    response = Response(int(user_input))
    sampler.update(
        stim=next_stim,
        outcome={"response": response.name.lower()},
    )

print(f"Your lower bound frequency estimate is {sampler.param_estimate["mean"]} Hz.")
