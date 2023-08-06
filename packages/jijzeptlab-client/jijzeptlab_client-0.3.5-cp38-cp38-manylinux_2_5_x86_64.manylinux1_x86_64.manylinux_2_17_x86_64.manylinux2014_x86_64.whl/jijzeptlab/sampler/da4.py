from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from jijmodeling import SampleSet
from jijzeptlab.compile import CompiledInstance
from jijzeptlab.utils.baseclass import Option, Result
from pydantic import Field


class DA4SamplerOption(Option):
    """Options to create a DA4Sampler.

    Attributes:
        time_limit (int, optional): Upper limit of execution time in seconds. Defaults to 10.
        target_energy (float, optional): Target energy to be terminated when the energy is lower
            than the target energy. Defaults to None.
        num_run (int, optional): The number of parallel trial iterations. Defaults to 16.
        num_group (int, optional): The number of groups of parallel trials. Defaults to 1.
        num_output_solution (int, optional): The number of output solutions for each parallel
            trial group. Defaults to 5.
        gs_level (int, optional): Level of global search. Defaults to 5.
        gs_cutoff (int, optional): Convergence decision level for global search. If 0 is set,
            this function is turned off. Defaults to 8000.
        one_hot_level (int, optional): Level of one-hot constraints search. Defaults to 3.
        one_hot_cutoff (int, optional): Convergence decision level for one-hot constraints
            search. If 0 is set, this function is turned off. Defaults to 100.
        internal_penalty (int, optional): Coefficient adjustment mode for constraint terms. If
            set to 0, no adjustment is made. Defaults to 0.
        penalty_auto_mode (int, optional): Coefficient adjustment mode for constraint terms. If
            set to 0, no adjustment is made. Defaults to 1.
        penalty_coefficient (int, optional): Coefficient of the constraint term. Defaults to 1.
        penalty_inc_rate (int, optional): Parameters for automatic adjustment of constraint terms.
            Defaults to 150.
        max_penalty_coefficient (int, optional): A maximum value of constraint term coefficients.
            If 0 is set, there is no maximum value. Defaults to 0.
        guidance_config (Dict[str, bool], optional): Initial value of each variable. Defaults to None.
        fixed_config (Dict[str, bool], optional): Fixed value for each variable. Defaults to None.
        one_way_one_hot_groups (List[str], optional): Specifies the number of variables in each
            group of one-way one-hot constraints. Defaults to None.
        two_way_one_hot_groups (List[str], optional): Specifies the number of variables in each
            group of two-way one-hot constraints. Defaults to None.
        inequalities_lambda (Dict[str, int], optional): Coefficient of inequality. If omitted,
            set to 1. Defaults to None.
    """

    # Upper limit of execution time in seconds.
    time_limit: int = Field(10, alias="time_limit_sec")
    # Target energy to be terminated when the energy is lower than the target energy.
    target_energy: Optional[float] = None
    # The number of parallel trial iterations.
    num_run: int = 16
    # The number of groups of parallel trials.
    num_group: int = 1
    # The number of output solutions for each parallel trial group.
    num_output_solution: int = 5
    # Level of global search.
    gs_level: int = 5
    # Convergence decision level for global search. If 0 is set, this function is turned off.
    gs_cutoff: int = 8000
    # Level of one-hot constraints search.
    one_hot_level: int = 3
    # Convergence decision level for one-hot constraints search. If 0 is set, this function is turned off.
    one_hot_cutoff: int = 100
    # Coefficient adjustment mode for constraint terms. If set to 0, no adjustment is made.
    internal_penalty: int = 0
    # Coefficient adjustment mode for constraint terms. If set to 0, no adjustment is made.
    penalty_auto_mode: int = 1
    # Coefficient of the constraint term.
    penalty_coefficient: int = Field(1, alias="penalty_coef")
    # Parameters for automatic adjustment of constraint terms.
    penalty_inc_rate: int = 150
    # A maximum value of constraint term coefficients. If 0 is set, there is no maximum value.
    max_penalty_coefficient: int = Field(0, alias="max_penalty_coef")
    # Initial value of each variable.
    guidance_config: Optional[Dict[str, bool]] = None
    # Fixed value for each variable.
    fixed_config: Optional[Dict[str, bool]] = None
    # Specifies the number of variables in each group of one-way one-hot constraints.
    one_way_one_hot_groups: Optional[List[str]] = None
    # Specifies the number of variables in each group of two-way one-hot constraints.
    two_way_one_hot_groups: Optional[List[str]] = None
    # Coefficient of inequality. If omitted, set to 1. Defaults to None.
    inequalities_lambda: Optional[Dict[str, int]] = None


@dataclass(frozen=True)
class DA4Model:
    """Model for DA4Sampler.

    Attributes:
        compiled_instance (CompiledInstance): CompiledInstance
    """

    compiled_instance: CompiledInstance


@dataclass(frozen=True)
class DA4Result(Result):
    """Result of DA4Sampler."""

    sample_set: SampleSet

    def to_sample_set(self) -> SampleSet:
        return self.sample_set


def create_model(compiled_instance: CompiledInstance) -> DA4Model:
    """Create a model for DA4Sampler.

    Args:
        compiled_instance (CompiledInstance): CompiledInstance

    Returns:
        DA4Model: DA4Model
    """
    raise NotImplementedError("DA4Sampler is not implemented yet.")


def sample(
    model: DA4Model,
    token: str,
    url: str = "https://api.aispf.global.fujitsu.com/da",
    multipliers: Optional[Dict[str, float]] = None,
    option: Optional[DA4SamplerOption] = None,
) -> DA4Result:
    """Sample by DA4Sampler.

    Args:
        model (DA4Model): DA4Model
        token (str): Token
        url (str, optional): URL. Defaults to "https://api.aispf.global.fujitsu.com/da".
        multipliers (Optional[Dict[str, float]], optional): Multipliers. Defaults to None.
        option (Optional[DA4SamplerOption], optional): Option. Defaults to None.

    Returns:
        DA4Result: DA4Result

    Examples:
        ```python
        import jijzeptlab as jzl
        import jijzeptlab.sampler.da4 as da4

        compiled_model = jzl.compile_model(problem, jzl.InstanceData.from_dict(instance_data))
        da4_option = da4.DA4SamplerOption(time_limit_sec=5)
        da4_model = da4.create_model(compiled_instance)
        da4_result = da4.sample(da4_model, token="...", option=da4_option)
        solution = da4_result.to_sample_set()
        ```
    """

    raise NotImplementedError("DA4Sampler is not implemented yet.")
