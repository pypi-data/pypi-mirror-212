from __future__ import annotations

import enum

from typing import Dict, List, Optional

import jijmodeling as jm
import jijmodeling.transpiler as jmt
import mip

from jijzeptlab.compile import CompiledInstance
from jijzeptlab.utils.baseclass import Option, ResultWithDualVariables
from pydantic import Field


class MipModelOption(Option):
    """Option for MipModel

    Attributes:
        ignore_constraint_names (List[str]): constraint names to be ignored
        relaxed_variable_names (List[str]): variable names to be relaxed to continuous ones
        relax_all_variables (bool): if True, all variables are relaxed to continuous ones
        ignore_constraint_indices (Dict[str, List[List[int]]]): constraint indices to be ignored
    """

    ignore_constraint_names: List[str] = Field(default_factory=list)
    relaxed_variable_names: List[str] = Field(default_factory=list)
    relax_all_variables: bool = False
    ignore_constraint_indices: Dict[str, List[List[int]]] = Field(default_factory=dict)


class MipModelStatus(enum.Enum):
    """Status of MipModel.

    Attributes:
        SUCCESS (str): The model was built successfully.
        TRIVIALLY_INFEASIBLE (str): The model is trivially infeasible.
    """

    SUCCESS = enum.auto()
    TRIVIALLY_INFEASIBLE = enum.auto()


class MipModel:
    """MIP model class for JijZeptLab"""

    def __init__(self, mip_model, mip_decoder, model_status) -> None:
        self.mip_model = mip_model
        self._mip_decoder = mip_decoder
        self.mip_status = model_status


class MipResultStatus(enum.Enum):
    """Status of MipResult.

    Attributes:
        SUCCESS (str): The model was solved successfully.
        TRIVIALLY_INFEASIBLE (str): The model is trivially infeasible.
    """

    SUCCESS = enum.auto()
    TRIVIALLY_INFEASIBLE = enum.auto()


class MipResult(ResultWithDualVariables):
    """Result class for MIP solver"""

    def __init__(self, mip_model: mip.Model, mip_decoder, status) -> None:
        self.mip_model = mip_model
        self._mip_decoder = mip_decoder
        self._status = status

    @property
    def status(self) -> MipResultStatus:
        """Status of MipResult"""
        if self._status == mip.OptimizationStatus.OPTIMAL:
            return MipResultStatus.SUCCESS
        else:
            return MipResultStatus.TRIVIALLY_INFEASIBLE

    def to_sample_set(self) -> jm.SampleSet | None:
        """Convert to SampleSet"""
        decoded_result = self._mip_decoder.decode_from_mip(self._status, self.mip_model)
        return decoded_result


def create_model(
    compiled_instance: CompiledInstance, option: Optional[MipModelOption] = None
) -> MipModel:
    """Create MIP model from compiled instance

    Args:
        compiled_instance (CompiledInstance): compiled instance
        option (Optional[MipModelOption]): option for MIP model

    Returns:
        MipModel: MIP model

    Examples:
        ```python
        import jijzeptlab as jzl
        import jijzeptlab.solver.mip as mip

        compiled_model = jzl.compile_model(problem, jzl.InstanceData.from_dict(instance_data))
        # initialize MIP instance
        mip_model = mip.create_model(compiled_model)
        # solve
        mip_result = mip.solve(mip_model)
        # convert the solution to `jm.SampleSet`。
        final_solution = mip_result.to_sample_set()
        ```
    """

    if option is None:
        option = MipModelOption()

    jmt_instance = compiled_instance._instance
    if option.relax_all_variables:
        relax_all_vars = list(jmt_instance.var_map.var_map.keys())
    else:
        relax_all_vars = []
    mip_builder = jmt.core.mip.transpile_to_mip(
        compiled_instance._instance, relax_list=relax_all_vars
    )
    pymip_model = mip_builder.get_model()
    return MipModel(pymip_model, mip_builder, MipModelStatus.SUCCESS)


def solve(mip_model: MipModel) -> MipResult:
    status = mip_model.mip_model.optimize()
    return MipResult(mip_model.mip_model, mip_model._mip_decoder, status)
