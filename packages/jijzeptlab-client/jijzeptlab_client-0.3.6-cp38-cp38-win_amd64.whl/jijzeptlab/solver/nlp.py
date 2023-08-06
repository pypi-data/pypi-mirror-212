from __future__ import annotations

import typing as tp

from dataclasses import dataclass
from enum import Enum

import jijmodeling as jm

from jijzeptlab.compile import CompiledInstance
from jijzeptlab.utils.baseclass import Option, ResultWithDualVariables
from pydantic import Field


class Solver(Enum):
    """Solver options.

    This class is for NlpSolveOption's solver_option argument.

    Attributes:
        ipopt: ipopt solver.
            This option is available without any additional setup from the user.
            Note that all variables are continuously relaxed on ipopt, irrespective of your settings.
        gurobi: gurobi solver.
            This option requires preparation of the gurobi solver by the user.
    """

    ipopt = "ipopt"
    gurobi = "gurobi"


class NlpModelOption(Option):
    """Options to create a NlpModel.
    Attributes:
        ignore_constraint_names (list[str]): The names of the constraints to ignore.
        relaxed_variable_names (list[str]): The names of the variables to relax.
        relax_all_variables (bool): If True, all variables are relaxed and `relaxed_variable_names` is ignored.
        ignore_constraint_indices (Dict[str, list[list[int]]]): A dictionary mapping constraint names to lists of constraint indices to ignore.
    """

    # The names of the constraints to ignore.
    ignore_constraint_names: list[str] = Field(default_factory=list)
    # The names of the variables to relax.
    relaxed_variable_names: list[str] = Field(default_factory=list)
    # If True, all variables are relaxed and `relaxed_variable_names` is ignored.
    relax_all_variables: bool = False
    # A dictionary mapping constraint names to lists of constraint indices
    # to ignore.
    ignore_constraint_indices: dict[str, list[list[int]]] = Field(default_factory=dict)


class NlpSolveOption(Option):
    """Options to solve nlp problem.
    Attributes:
        tee (bool): If True, the solver will print the progress of the solve.
    """

    tee: bool = False


class NlpSolverOption(Option):
    """Options of solver.
    Attributes:
        solver (Solver): the solver to use.
        Check the SolverOption class for a list of available solvers.
    """

    solver: Solver = Solver.ipopt
    solver_settings: dict[str, tp.Any] = Field(default_factory=dict)


class NlpModelStatus(Enum):
    """Status of NlpModel.
    Attributes:
        SUCCESS (str): The model was built successfully.
        TRIVIALLY_INFEASIBLE (str): The model is trivially infeasible.
    """

    SUCCESS = "success"
    TRIVIALLY_INFEASIBLE = "trivially_infeasible"


@dataclass(frozen=True)
class NlpModel:
    """NlpModel is a class that represents a model for non-linear problem solver.
    Attributes:
        model_status (NlpModelStatus): Status of the model.
    """

    model_status: NlpModelStatus = NlpModelStatus.SUCCESS


class NlpResultStatus(Enum):
    """Status of CbcResult.
    Attributes:
        SUCCESS (str): The problem is solved successfully. Note that the feasibility of the solution is not guaranteed.
        TRIVIALLY_INFEASIBLE (str): The problem is trivially infeasible.
    """

    SUCCESS = "success"
    TRIVIALLY_INFEASIBLE = "trivially_infeasible"


@dataclass(frozen=True)
class NlpResult(ResultWithDualVariables):
    """class that represents a result of non-linear problem solver. """
    status: NlpResultStatus = NlpResultStatus.SUCCESS

    def to_sample_set(self) -> jm.SampleSet | None:
        """Converts the result to a SampleSet.
        If the result is trivially infeasible, None is returned.

        Returns:
            SampleSet (jm.SampleSet | None): SampleSet. If the result is trivially infeasible, None is returned.
        """
        raise NotImplementedError("to_sample_set is not implemented")

    def _get_dual_variables(self) -> dict[str, dict[tuple[int], float]] | None:
        """Returns the dual variables of the constraints.
        If the result is trivially infeasible, None is returned.

        Returns:
            dict[str, dict[tuple[int], float]] | None: The dual variables of the constraints.
        """
        raise NotImplementedError("_get_dual_variables is not implemented")


def create_model(
    compiled_instance: CompiledInstance,
    model_option: NlpModelOption | None = None,
    solver_option: NlpSolverOption | None = None,
    init_solution: jm.SampleSet | None = None,
):
    """Create a NlpModel from a CompiledInstance.

    Note that all variables will be relaxed by default since the default settings of solver_option is ipopt, which is a solver for a non-linear problem with continuous variables.
    Some other solvers require explicit specification of the variable to relax continuously, e.g. gurobi.

    Args:
        compiled_instance (CompiledInstance): Compiled instance.
        model_option (NlpModelOption | None): model option. Defaults to None.
        solver_option (NlpSolverOption | None): solver option. Defaults to None.
        init_solution (jm.SampleSet | None): initial solution. Defaults to None.
    Returns:
        NlpModel: Non-linar problem model.
    
    Examples:
        ```python
        import jijzeptlab as jzl
        import jijzeptlab.solver.nlp as nlp

        compiled_model = jzl.compile_model(problem, jzl.InstanceData.from_dict(instance_data))
        # initialize MIP instance
        nlp_model = nlp.create_model(compiled_model)
        # solve
        nlp_result = nlp.solve(mip_model)
        # convert the solution to `jm.SampleSet`。
        final_solution = nlp_result.to_sample_set()
        ```

    """
    raise NotImplementedError("create_model is not implemented")


def solve(nlp_model: NlpModel, option: NlpSolveOption | None = None) -> NlpResult:
    """Solve a NlpModel.
    Args:
        nlp_model (NlpModel): Nlp model.
    Returns:
        NlpResult: Nlp result.
    """
    raise NotImplementedError("solve is not implemented")
