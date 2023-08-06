from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Union

from jijmodeling import SampleSet
from jijzeptlab.compile import CompiledInstance
from jijzeptlab.utils.baseclass import Option, Result


class DwaveLeapSamplerOption(Option):
    """Options to create a DwaveLeapSampler."""

    time_limit: Optional[Union[int, float]] = None
    label: Optional[str] = None


@dataclass(frozen=True)
class DwaveLeapModel:
    """Model for DwaveLeapCQMModel.

    Attributes:
        compiled_instance (CompiledInstance): CompiledInstance
    """

    compiled_instance: CompiledInstance


@dataclass(frozen=True)
class DwaveLeapResult(Result):
    """Result of DwaveLeapSampler."""

    sample_set: SampleSet

    def to_sample_set(self) -> SampleSet:
        return self.sample_set


def create_model(compiled_instance: CompiledInstance) -> DwaveLeapModel:
    """Create a model for DwaveLeapSampler.

    Args:
        compiled_instance (CompiledInstance): CompiledInstance

    Returns:
        DwaveLeapModel: DwaveLeapModel

    Examples:
        ```python
        import jijzeptlab as jzl
        import jijzeptlab.sampler.dwaveleap as dwaveleap

        compiled_model = jzl.compile_model(problem, jzl.InstanceData.from_dict(instance_data))
        leap_option = dwaveleap.DwaveLeapSamplerOption(time_limit=5)
        leap_model = dwaveleap.create_model(compiled_instance)
        leap_result = dwaveleap.sample(leap_model, token="...", option=leap_option)
        solution = leap_result.to_sample_set()
        ```

    """
    return DwaveLeapModel(compiled_instance)


def sample(
    model: DwaveLeapModel,
    token: str,
    url: Optional[str] = None,
    relax_list: Optional[List[str]] = None,
    option: Optional[DwaveLeapSamplerOption] = None,
) -> DwaveLeapResult:
    """Sample by DwaveLeap.

    Args:
        model (DA4Model): DA4Model
        token (str): Token
        url (Optional[str], optional): URL. Defaults to None.
        relax_list (Optional[List[str]], optional): Relax list. Defaults to None.
        option (Optional[DA4SamplerOption], optional): Option. Defaults to None.

    Returns:
        DwaveLeapResult: DwaveLeapResult
    """
    raise NotImplementedError("sample is not implemented yet.")
