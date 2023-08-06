import typing as tp

from functools import singledispatch

import jijmodeling as jm


@singledispatch
def _recursive_deserialize(obj: tp.Any) -> tp.Any:
    """deserialize an object (jm.SampleSet and jm.Problem) recursively.
    This function traverses the object recursively and deserializes it if the instance type is serialized from jm.SampleSet or jm.Problem.
    """
    return obj


@_recursive_deserialize.register
def _(obj: dict) -> tp.Any:
    deserialized = None

    # attempt to deserialize with `jm.SampleSet.from_serializable`
    try:
        deserialized = jm.SampleSet.from_serializable(obj)
        return deserialized
    except (jm.exceptions.SerializeSampleSetError, AttributeError, TypeError):
        pass

    # attempt to deserialize with `jm.from_serializable (jm.Problem)`
    try:
        deserialized = jm.from_serializable(obj)
        return deserialized
    except (ValueError, NotImplementedError):
        pass

    return {k: _recursive_deserialize(v) for k, v in obj.items()}


# list
@_recursive_deserialize.register
def _(obj: list) -> tp.Any:
    return [_recursive_deserialize(elem) for elem in obj]


# tuple
@_recursive_deserialize.register
def _(obj: tuple) -> tp.Any:
    return tuple(_recursive_deserialize(elem) for elem in obj)
