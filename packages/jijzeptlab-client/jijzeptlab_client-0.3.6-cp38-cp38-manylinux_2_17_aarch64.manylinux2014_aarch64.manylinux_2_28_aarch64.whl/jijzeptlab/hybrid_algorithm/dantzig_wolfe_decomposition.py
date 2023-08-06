from typing import Any, Callable, Dict, List, Optional, Tuple

import jijmodeling as jm
import jijzeptlab as jzl


class DantzigWolfeDecomposition:
    LARGE_CONSTANT: int
    BASIS_PREFIX: str
    U_PREFIX: str
    SIGMA_PREFIX: str
    LAMBDA_PREFIX: str
    DualVariableType = Dict[str, Dict[Tuple[int, ...], float]]
    problem: jm.Problem

    def __init__(
        self,
        compiled_instance: jzl.CompiledInstance,
        separated_constraints_label: List[List[str]],
        overlapped_constraints_label: List[str],
        masterproblem_callback: Callable[
            [jm.Problem, dict, Tuple[Any, ...], Any],
            Optional[Tuple[jm.SampleSet, DualVariableType]],
        ],
        subproblem_callback: Callable[
            [jm.Problem, dict, Tuple[Any, ...], Any],
            Optional[Tuple[jm.SampleSet, DualVariableType]],
        ],
        separated_objectives: Optional[List[jm.Expression]] = ...,
        overlapped_constraint_elements: Optional[Dict[str, List[jm.Expression]]] = ...,
        slack_M_value: float = 20.0,
    ) -> None:
        raise NotImplementedError("DantzigWolfeDecomposition is not implemented yet.")

    def initialize(self, slack_M_value: float = 20.0):
        raise NotImplementedError("DantzigWolfeDecomposition is not implemented yet.")

    @property
    def separated_subproblems(self) -> List[jm.Problem]:
        raise NotImplementedError("DantzigWolfeDecomposition is not implemented yet.")

    @property
    def shifted_separated_subproblems(self) -> List[jm.Problem]:
        raise NotImplementedError("DantzigWolfeDecomposition is not implemented yet.")

    @property
    def masterproblem(self) -> jm.Problem:
        raise NotImplementedError("DantzigWolfeDecomposition is not implemented yet.")

    @property
    def always_feasible_masterproblem(self) -> jm.Problem:
        raise NotImplementedError("DantzigWolfeDecomposition is not implemented yet.")

    @property
    def convergence_parameter(self) -> float:
        raise NotImplementedError("DantzigWolfeDecomposition is not implemented yet.")

    @property
    def current_solution(self) -> jm.SampleSet:
        raise NotImplementedError("DantzigWolfeDecomposition is not implemented yet.")

    @property
    def current_dual_variables(self) -> DualVariableType:
        raise NotImplementedError("DantzigWolfeDecomposition is not implemented yet.")

    def is_feasible(self) -> bool:
        raise NotImplementedError("DantzigWolfeDecomposition is not implemented yet.")

    def is_converge(self, tol: float = ...) -> bool:
        raise NotImplementedError("DantzigWolfeDecomposition is not implemented yet.")

    def update(
        self, *args: Tuple[Any, ...], **kwargs: Any
    ) -> Tuple[Optional[jm.SampleSet], Optional[List[jm.SampleSet]]]:
        raise NotImplementedError("DantzigWolfeDecomposition is not implemented yet.")
