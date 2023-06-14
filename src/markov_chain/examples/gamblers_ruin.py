from markov_chain.chain import MarkovChain


def gamblers_ruin(
    initial_position: int = 100, prob_up: float = 0.5, upper_limit: int = 200, lower_limit: int = 0
) -> MarkovChain:
    """
    Simulate the Gambler's Ruin problem using a Markov Chain.

    This function models the problem where a gambler will continue to place bets
    until they have either won a certain amount or lost their entire stake.
    The function takes in an initial state (stake), a probability of winning a bet,
    and an upper and lower limit for the amount of money the gambler is willing to win/lose.

    Parameters:
    initial_state (int, optional): The initial amount of money the gambler has. Default is 100.
    prob_up (float, optional): The probability of the gambler winning a bet. Default is 0.5.
    upper_limit (int, optional): The amount of money at which the gambler will stop betting if won. Default is 200.
    lower_limit (int, optional): The amount of money at which the gambler will stop betting if lost. Default is 0.

    Returns:
    MarkovChain: A MarkovChain object representing the gambler's ruin problem.
    """

    prob_down = 1.0 - prob_up
    n_states = upper_limit - lower_limit + 1
    init_state = [0.0] * n_states
    init_state[initial_position] = 1.0

    transition_matrix = []
    for _ in range(n_states):
        transition_matrix.append([0.0] * n_states)

    # Probability from transitioning once hit lower limit is 0, so probability of staying is 1
    transition_matrix[0][0] = 1.0

    # Similar reasoning for when one hits the upper limit
    transition_matrix[n_states - 1][n_states - 1] = 1.0

    for n in range(1, n_states - 1):
        transition_matrix[n + 1][n] = prob_up  # probability from going from n to n+1
        transition_matrix[n - 1][n] = prob_down

    chain = MarkovChain(transition_matrix, init_state)
    return chain
