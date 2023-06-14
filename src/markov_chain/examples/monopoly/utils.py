from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional

import numpy as np
import plotly.graph_objects as go


@dataclass
class MonopolySettings:
    """Base class for Monopoly simulators storing settings"""

    three_doubles_jail: bool
    n_chance: int
    chance_locs: List[int]
    chance_advances: List[int]


DefaultMonopolySettings = MonopolySettings(
    three_doubles_jail=True,
    n_chance=16,
    chance_locs=[2, 7, 17, 22, 36],
    chance_advances=[0, 24, 11, 10],
)


class MonopolySimulationBase(ABC):
    """Abstract base class for a monopoly simulation"""

    def __init__(self, settings: Optional[MonopolySettings] = None) -> None:
        if settings is None:
            settings = DefaultMonopolySettings
        self._settings = settings

    @abstractmethod
    def state_at_time(self, time: int) -> np.ndarray:
        """Return state at time"""


def plot_monopoly_comparison(simulators: Dict[str, MonopolySimulationBase], step: int = 20) -> go.Figure:
    """Plot a comparison between a list of simulators at a given timestep"""
    fig = go.Figure()

    for label, sim in simulators.items():
        state = sim.state_at_time(step)
        fig.add_trace(go.Scatter(x=list(range(len(state))), y=state, mode="lines", name=label))

    fig.update_layout(
        title=f"timestep {step}",
        xaxis_title="Position",
        yaxis_title="Probability",
        autosize=False,
        width=500,
        height=500,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
    )

    fig.show()
    return fig


def animate_monopoly_comparison(
    simulators: Dict[str, MonopolySimulationBase], timesteps: int = 20, time_between_steps: int = 200
) -> go.Figure:
    """Create an animation of a comparison between a list of simulators over time"""

    frames = []

    for i in range(timesteps):
        frame_data = []
        max_value = max(
            [max(sim.state_at_time(i)) for sim in simulators.values()]
        )  # find the maximum value across all simulators at this time
        for label, sim in simulators.items():
            state = sim.state_at_time(i) / max_value
            frame_data.append(go.Scatter(x=list(range(len(state))), y=state, mode="lines", name=label))
        frames.append(go.Frame(data=frame_data))

    fig = go.Figure(
        data=frames[0]["data"],
        layout=go.Layout(
            xaxis=dict(range=[0, max([len(sim.state_at_time(0)) for sim in simulators.values()])], autorange=False),
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
            title="State Over Time",
            xaxis_title="Position",
            yaxis_title="Probability/Max_probability",
            autosize=False,
            width=500,
            height=500,
            margin=dict(l=50, r=50, b=100, t=100, pad=4),
        ),
        frames=frames,
    )

    return fig
