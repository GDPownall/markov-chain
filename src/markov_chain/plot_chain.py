from typing import Optional

import plotly.graph_objects as go

from markov_chain.chain import MarkovChain


class MarkovChainPlotter:
    """Plotting tools for the MarkovChain class"""

    @staticmethod
    def plot_stationary(chain: MarkovChain, outfile: Optional[str] = None) -> go.Figure:
        """Plot the stationary state. Provide an outfile string to save."""
        stationary = chain.stationary_state()

        fig = go.Figure(data=go.Scatter(x=list(range(len(stationary))), y=stationary, mode="lines"))
        fig.update_layout(
            title="Stationary state",
            xaxis_title="Position",
            yaxis_title="Probability",
            autosize=False,
            width=500,
            height=500,
            margin=dict(l=50, r=50, b=100, t=100, pad=4),
        )
        if outfile:
            fig.write_image(outfile)  # You need plotly-orca installed for this to work.

        return fig

    @staticmethod
    def plot_over_time(
        chain: MarkovChain,
        timesteps: int = 20,
        start_from: int = 0,
        time_between_steps: int = 200,
    ) -> go.Figure:
        """Plot the markov chain state over a number of steps as an animation"""
        x = list(range(chain.n_states))
        frames = []

        for i in range(start_from, timesteps):
            y = chain.state_at_time(i)
            frames.append(go.Frame(data=go.Scatter(x=x, y=y, mode="lines")))

        fig = go.Figure(
            data=go.Scatter(x=x, y=chain.state_at_time(start_from), mode="lines"),
            layout=go.Layout(
                xaxis=dict(range=[min(x), max(x)], autorange=False),
                yaxis=dict(range=[0, 1], autorange=False),
                updatemenus=[
                    dict(
                        type="buttons",
                        buttons=[
                            dict(
                                label="Play",
                                method="animate",
                                args=[
                                    None,
                                    {
                                        "frame": {"duration": time_between_steps, "redraw": True},
                                        "fromcurrent": True,
                                        "transition": {"duration": time_between_steps},
                                    },
                                ],
                            )
                        ],
                    )
                ],
            ),
            frames=frames,
        )

        fig.update_layout(
            title="State Over Time",
            xaxis_title="Position",
            yaxis_title="Probability",
            autosize=False,
            width=500,
            height=500,
            margin=dict(l=50, r=50, b=100, t=100, pad=4),
        )

        return fig
