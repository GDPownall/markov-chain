from typing import Optional
from typing import Tuple

import numpy as np

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from markov_chain.chain import MarkovChain


class MarkovChainPlotter:
    """Plotting tools for the MarkovChain class"""

    @staticmethod
    def plot_stationary(chain: MarkovChain, outfile: Optional[str] = None) -> plt.Figure:
        """Plot the stationary state. Provide an outfile string to save."""
        stationary = chain.stationary_state()
        fig, ax = plt.subplots()
        fig.set_tight_layout(True)
        plt.title("Stationary state")
        plt.xlabel("Position")
        plt.ylabel("Probability")
        _ = ax.plot(range(len(stationary)), stationary, linewidth=2)
        if outfile:
            fig.savefig(outfile)
        return fig

    @staticmethod
    def plot_over_time(
        chain: MarkovChain,
        timesteps: int = 20,
        start_from: int = 0,
        time_between_steps: int = 200,
        outfile: Optional[str] = None,
    ) -> FuncAnimation:
        """
        Create an animation of the state over time.

        @params
        chain (MarkovChain): The Markov chain to animate. It should contain the method "state_at_time" which returns
            the state of the chain at a specific time point.
        timesteps (int, optional): The number of time steps to animate. Defaults to 20.
        start_from (int, optional): The time step to start the animation from. Defaults to 0.
        time_between_steps (int, optional): The time in milliseconds between steps in the animation. Defaults to 200.
        outfile (str, optional): If provided, the animation will be saved to this file path.
            The file format is inferred from the filename.
            If it's not provided, the animation won't be saved to a file.

        Returns:
        FuncAnimation: The animation object.
            You can display it using IPython.display.HTML(anim.to_jshtml()) in a Jupyter notebook
            or you can save it using anim.save('filename.mp4').

        Note:
        You need to have imagemagick installed and properly configured for saving the animation.
        """
        fig, ax = plt.subplots()
        x = range(len(chain.n_states))
        y = chain.state_at_time(start_from)
        (line,) = ax.plot(x, y, linewidth=2)
        ax.set_xlabel("Position")
        ax.set_ylabel("Probability")

        def update(i: int) -> Tuple:
            label = "timestep {0}".format(i)
            line.set_ydata(chain.state_at_time(i))
            ax.set_title(label)
            return line, ax

        anim = FuncAnimation(
            fig,
            update,
            frames=np.arange(start_from, timesteps),
            interval=time_between_steps,
        )
        # plt.show()
        if outfile:
            anim.save(outfile, dpi=100, writer="imagemagick")
        return anim
