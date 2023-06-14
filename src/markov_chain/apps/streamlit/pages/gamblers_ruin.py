import streamlit as st

from markov_chain.examples.gamblers_ruin import gamblers_ruin
from markov_chain.plot_chain import MarkovChainPlotter


st.title("Simulating Gambler's Ruin through Eigenfactor Centrality")

left_edge = st.number_input(label="Smallest value", value=0)
right_edge = st.number_input(label="Largest value", min_value=left_edge, value=left_edge + 10)
start_position = st.slider(
    label="Start position",
    min_value=left_edge + 1,
    max_value=right_edge - 1,
    value=int((right_edge + left_edge) / 2),
    step=1,
)
prob_up = st.slider(label="Probability of moving up a step", min_value=0.0, max_value=1.0, value=0.5, step=0.01)

chain = gamblers_ruin(initial_position=start_position, lower_limit=left_edge, upper_limit=right_edge, prob_up=prob_up)

plotter = MarkovChainPlotter

st.plotly_chart(plotter.plot_stationary(chain=chain))

n_steps_to_animate = st.number_input(label="Number of steps to animate", min_value=1, value=10)

st.plotly_chart(
    plotter.plot_over_time(chain=chain, start_from=0, timesteps=n_steps_to_animate, time_between_steps=200)
)
