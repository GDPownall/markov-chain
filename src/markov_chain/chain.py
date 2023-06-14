from dataclasses import dataclass
from typing import Optional

import numpy as np
import numpy.typing as npt


@dataclass
class EigenContainer:
    """Dataclass containing the result of a MarkovChain evaluation"""

    constants: Optional[np.ndarray]
    eigenvalues: np.ndarray
    eigenvectors: np.ndarray


class MarkovChain:
    """
    The MarkovChain class allows one to use Markov Chain methodology to analyse a network.

    You must define the probability matrix of a Markov chain process, and the initial state,
    to get the state at any time.
    The initial state does not necessarily need to be defined to get the steady state solution.

    The probability matrix takes the form:
        [[p00,p10,p20,...]
         [p01,p11,p21,...]
         [p02,p12,p22,...]
         ...
         ]
    where pxy is the probability to transition from state y to x
    As a result, the columns must sum to unity. The class raises an exception otherwise.

    The initial state is in the form of an array:
        [p0,p1,p2,...]
    where px is the probability of the system starting at state x. The sum of this array must therefore be 1, and the
    class raises an exception otherwise.
    """

    def __init__(
        self,
        probability_matrix: npt.ArrayLike,
        initial_state: Optional[npt.ArrayLike] = None,
    ) -> None:

        self._evaluation = None

        probability_matrix = np.array(probability_matrix)
        if len(probability_matrix.shape) != 2 or (probability_matrix.shape[0] != probability_matrix.shape[1]):
            raise ValueError("Matrix supplied to Markov Chain class not square")

        col_totals = probability_matrix.sum(axis=0)
        if not all(np.isclose(col_totals, 1)):
            raise ValueError(
                "Matrix column at position(s) "
                + str(np.argwhere(~np.isclose(col_totals, 1)).ravel())
                + " does not sum to one."
            )

        self._probability_matrix = probability_matrix
        self.n_states = probability_matrix.shape[0]

        if initial_state is not None:
            initial_state = np.array(initial_state)
            if not np.isclose(initial_state.sum(), 1):
                raise ValueError("Initial state does not sum to one")

        self._initial_state = initial_state

    def _evaluate(self) -> None:
        if self._evaluation is not None:
            return
        eig_vals, eig_vecs = np.linalg.eig(self._probability_matrix)
        # Sort eigenvalues and associate vectors
        idx = eig_vals.argsort()[::-1]
        eig_vals = eig_vals[idx]
        eig_vecs = eig_vecs[:, idx]
        eig_vecs = eig_vecs.transpose()
        eig_vecs = self._renorm_eigvectors(eig_vecs)
        consts = None
        if self._initial_state is not None:
            consts = self._initial_state.dot(np.linalg.inv(eig_vecs))
        self._evaluation = EigenContainer(constants=consts, eigenvalues=eig_vals, eigenvectors=eig_vecs)

    @staticmethod
    def _renorm_eigvectors(eig_vecs: np.ndarray) -> np.ndarray:
        # Find renorm values. Not as simple as just finding max, has to deal with negative numbers too.
        maxmin = np.array([np.max(eig_vecs, axis=1), np.min(eig_vecs, axis=1)])
        take_val = np.argmax(np.abs(maxmin), axis=0)
        renorms = maxmin[take_val, range(maxmin.shape[1])]
        # Now renormalise
        eig_vecs = (eig_vecs.T * 1.0 / renorms).T
        return eig_vecs

    def state_at_time(self, t: int) -> np.ndarray:
        """Get the state at time t"""
        consts, eig_vals, eig_vecs = self._evaluation
        if consts is None:
            raise RuntimeError("Cannot calculate state at specific time without an initial state")
        result = np.zeros(eig_vecs.shape[0])
        for i in range(len(consts)):
            result += np.real(consts[i] * (eig_vals[i] ** t) * eig_vecs[i, :])
        return result

    def stationary_state(self) -> np.ndarray:
        """Calculate the stationary state"""
        consts, eig_vals, eig_vecs = self._evaluation

        stationary_args = np.isclose(eig_vals, 1)
        if stationary_args.sum() == 1:
            e = np.where(stationary_args)[0][0]
            stationary_state = eig_vecs[e, :]
            return stationary_state / stationary_state.sum()
        if consts is None:
            raise RuntimeError(
                "Multiple stationary states found. "
                "Network must be separable. "
                "Initial state required for stationary state calculation."
            )
        stationary_state = np.zeros(len(eig_vecs[0, :]))
        for e in range(len(stationary_args)):
            if stationary_args[e]:
                stationary_state += np.real(consts[e] * np.array(eig_vecs[e]))
        return np.real(stationary_state / stationary_state.sum())
