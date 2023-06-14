import time

import psutil
import streamlit as st

from markov_chain.examples.monopoly.chain import MonopolyMarkovChain
from markov_chain.examples.monopoly.monte_carlo import MonopolyMonteCarlo
from markov_chain.examples.monopoly.utils import DefaultMonopolySettings
from markov_chain.examples.monopoly.utils import animate_monopoly_comparison
from markov_chain.plot_chain import MarkovChainPlotter


st.title("Simulating monopoly probability states using Eigenfactor Centrality and Monte Carlo")

st.text(
    "The monopoly game can be simulated as a network with an agent randomly hopping between states.\n"
    "This makes Eigenfactor Centrality perfect.\n"
    "In this page, it is demonstrated that the results from Eigenfactor Centrality mimic Monte Carlo."
)

three_doubles_jail = st.checkbox(
    label="Three doubles to jail?",
    value=True,
    help="Tick if you want to include the rule that three doubles in a row sends the agent to jail.",
)

number_of_monte_carlo_agents = st.number_input(label="Number of monte carlo simulations", value=100, min_value=1)

settings = DefaultMonopolySettings
settings.three_doubles_jail = three_doubles_jail

markov = MonopolyMarkovChain(settings=settings)
mc = MonopolyMonteCarlo(settings=settings, num_players=number_of_monte_carlo_agents)

st.plotly_chart(MarkovChainPlotter.plot_stationary(markov.markov))

max_animated_timesteps = 40

start_RAM = psutil.virtual_memory().used
st.text(f"RAM at start: {start_RAM/10**6}")

start_time = time.time()
markov.state_at_time(40)
st.text(f"Time to calculate state at 40 iterations with Markov Chain: {time.time()-start_time}s")
used_RAM = psutil.virtual_memory().used - start_RAM
st.text(f"RAM usage: {used_RAM*10**-6}MB")

start_time = time.time()
mc.state_at_time(40)
st.text(f"Time to calculate state at 40 iterations with Monte Carlo: {time.time()-start_time}s")
st.text(f"RAM usage:{(psutil.virtual_memory().used - used_RAM - start_RAM)*10**-6}MB")

comparison = animate_monopoly_comparison(
    simulators={"Eigenfactor centrality": markov, "Monte carlo": mc},
    timesteps=max_animated_timesteps,
    time_between_steps=200,
)
st.plotly_chart(comparison)

st.subheader("Why are there differences?")
st.text(
    "Firstly, note that monte-carlo is always imprecise.\n "
    "Even at 100,000 simulations, there are still noticeable differeces at times."
)
st.text(
    "Secondly, if the three-rolls-jail is in place, Eigenfactor Centrality cannot account for this\n"
    "as it assumes that each hop is independent. A small factor of (1/6)**3 is included to account for it,\n"
    "but in the first few turns this leads to an overestimation of the probability of going to jail.\n"
    "By the time we reach the steady state, this difference vanishes."
)
