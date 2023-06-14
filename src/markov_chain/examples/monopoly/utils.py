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
