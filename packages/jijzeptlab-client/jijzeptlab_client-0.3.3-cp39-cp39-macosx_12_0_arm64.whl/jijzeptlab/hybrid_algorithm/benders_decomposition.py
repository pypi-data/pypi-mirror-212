from __future__ import annotations

from enum import Enum
from typing import Any, Callable, List, Tuple

import jijmodeling as jm
import jijzeptlab as jzl

from jijzeptlab.utils.baseclass import (
    Option as Option,
    Result as Result,
    ResultWithDualVariables as ResultWithDualVariables,
    StateModel as StateModel
)


class InitializeOption(Option):
    slack_M_value: float


class UpdateCallback(Option):
    masterproblem_callback: Callable[[jzl.CompiledInstance], Result]
    subproblem_callback: Callable[[jzl.CompiledInstance], ResultWithDualVariables]


class BendersDecompositionResultStatus(Enum):
    SUCCESS: str
    MASTERPROBLEM_INFEASIBLE: str
    SUBPROBLEM_INFEASIBLE: str


class BendersDecompositionResult(Result):
    masterproblem_sampleset: jm.SampleSet | None
    subproblem_sampleset: jm.SampleSet | None
    original_compiled_model: jzl.CompiledInstance
    lower_bound: float
    upper_bound: float
    status: BendersDecompositionResultStatus

    def is_feasible(self) -> bool:
        """Check feasibility"""
        raise NotImplementedError("BendersDecompositionResult is not implemented yet.")

    def is_converge(self, tol: float = ...) -> bool:
        """Check convergence"""
        raise NotImplementedError("BendersDecompositionResult is not implemented yet.")

    def to_sample_set(self) -> jm.SampleSet | None:
        """Convert to SampleSet"""
        raise NotImplementedError("BendersDecompositionResult is not implemented yet.")

    def __init__(
        self,
        masterproblem_sampleset,
        subproblem_sampleset,
        original_compiled_model,
        lower_bound,
        upper_bound,
        _is_feasible,
        status,
    ) -> None:
        raise NotImplementedError("BendersDecompositionResult is not implemented yet.")


class BendersDecompositionModel(StateModel):
    """
    Model of Benders Decomposition
    """

    compiled_model: jzl.CompiledInstance
    master_decision_variables: List[jm.DecisionVariable]
    LARGE_CONSTANT: int = 100000000
    LOGENC_RANGE: int = 100000
    FIXED_PREFIX: str = "__fixed"
    RANDOMIZER_PREFIX: str = "__randomizer"
    BENDERS_COST_PLACEHOLDER: str = "__benders_cost_placeholder"
    DUAL_PREFIX: str = "__dual"
    FIXED_MASTER_PREFIX: str = "__fixed_master"
    alpha_variable: jm.DecisionVariable = jm.Integer(
        "__alpha", lower=-LOGENC_RANGE, upper=LOGENC_RANGE
    )
    option: InitializeOption | None = None

    def __post_init__(self) -> None:
        raise NotImplementedError("BendersDecompositionModel is not implemented yet.")

    def reset(self, option: InitializeOption | None = ...):
        """Reset model"""
        raise NotImplementedError("BendersDecompositionModel is not implemented yet.")

    def update(
        self, callback: UpdateCallback, *args: Tuple[Any, ...], **kwargs: Any
    ) -> BendersDecompositionResult:
        """Update model"""
        raise NotImplementedError("BendersDecompositionModel is not implemented yet.")

    def __init__(
        self,
        compiled_model,
        master_decision_variables,
        LARGE_CONSTANT,
        LOGENC_RANGE,
        FIXED_PREFIX,
        RANDOMIZER_PREFIX,
        BENDERS_COST_PLACEHOLDER,
        DUAL_PREFIX,
        FIXED_MASTER_PREFIX,
        alpha_variable,
        option,
    ) -> None:
        raise NotImplementedError("BendersDecompositionModel is not implemented yet.")


def create_model(
    compiled_model: jzl.CompiledInstance,
    master_decision_variables: List[jm.DecisionVariable],
    alpha_variable: jm.DecisionVariable | None = None,
    LARGE_CONSTANT: int | None = None,
) -> BendersDecompositionModel:
    """Create BendersDecompositionModel"""
    raise NotImplementedError("create_model is not implemented yet.")
