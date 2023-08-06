import typing as tp

import jijmodeling as jm
import numpy as np


def show_decivar_dependency(
    problem: jm.Problem,
) -> tp.Dict[tp.Tuple[str, ...], tp.List[str]]:
    raise NotImplementedError("show_decivar_dependency is not implemented yet.")


def convert_dual_variables_to_dense(
    input_dual_variables: tp.Dict[tp.Tuple[int, ...], float]
) -> np.ndarray:
    raise NotImplementedError("convert_dual_variables_to_dense is not implemented yet.")


def merge_sampleset(sampleset1: jm.SampleSet, sampleset2: jm.SampleSet) -> jm.SampleSet:
    raise NotImplementedError("merge_sampleset is not implemented yet.")


def merge_all_samplesets(samplesets: tp.List[jm.SampleSet]) -> jm.SampleSet:
    raise NotImplementedError("merge_all_samplesets is not implemented yet.")
