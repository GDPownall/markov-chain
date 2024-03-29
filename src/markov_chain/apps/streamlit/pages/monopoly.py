import time

import pandas as pd
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

st.text(
    "Note in the plots below that the monopoly board has been flattened\n"
    "'GO' is at position 0, 'Jail' is at position 10, etc."
)

three_doubles_jail = st.checkbox(
    label="Three doubles to jail?",
    value=True,
    help="Tick if you want to include the rule that three doubles in a row sends the agent to jail.",
)

number_of_monte_carlo_agents = st.number_input(label="Number of monte carlo simulations", value=100000, min_value=1)

settings = DefaultMonopolySettings
settings.three_doubles_jail = three_doubles_jail


start_RAM = psutil.virtual_memory().used
start_time = time.time()

markov = MonopolyMarkovChain(settings=settings)
markov.state_at_time(40)
markov_time = time.time() - start_time
markov_used_RAM = psutil.virtual_memory().used - start_RAM

start_time = time.time()
mc = MonopolyMonteCarlo(settings=settings, num_players=number_of_monte_carlo_agents)
mc.state_at_time(40)
mc_time = time.time() - start_time
mc_used_ram = psutil.virtual_memory().used - markov_used_RAM - start_RAM


df = pd.DataFrame(
    {"Time 40 steps (s)": [markov_time, mc_time], "Memory (B)": [markov_used_RAM, mc_used_ram]},
    index=["Markov", "Monte Carlo"],
)
df["Memory (MB)"] = df["Memory (B)"] * 10**-6
st.table(df[["Time 40 steps (s)"]])

st.plotly_chart(MarkovChainPlotter.plot_stationary(markov.markov))

n_frames = st.number_input(
    label="Number of frames", value=30, min_value=1, help="Number of frames to show in the below animation"
)
time_between_steps = st.number_input(
    label="Time between frames (ms)",
    value=200,
    min_value=1,
    help="Amount of time between frames in the below animation in milliseconds",
)

comparison = animate_monopoly_comparison(
    simulators={"Eigenfactor centrality": markov, "Monte carlo": mc},
    timesteps=n_frames,
    time_between_steps=time_between_steps,
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
