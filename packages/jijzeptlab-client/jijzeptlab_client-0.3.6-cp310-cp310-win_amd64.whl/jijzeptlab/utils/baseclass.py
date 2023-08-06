import abc

from abc import ABC, abstractmethod
from typing import Any

import jijmodeling as jm

from pydantic import BaseModel


class Option(BaseModel):
    """Base class for option"""

    class Config:
        allow_mutation: bool


class Result(ABC, metaclass=abc.ABCMeta):
    """Base class for storing result"""

    @abstractmethod
    def to_sample_set(self) -> jm.SampleSet:
        """Convert to SampleSet"""
        ...


class ResultWithDualVariables(Result, metaclass=abc.ABCMeta):
    """Base class for storing result with dual variables"""

    pass


class StateModel(metaclass=abc.ABCMeta):
    """Base class for model which has the state"""

    @abstractmethod
    def reset(self, *args, **kwargs) -> Any:
        """Reset the state"""
        ...

    @abstractmethod
    def update(self, *args, **kwargs) -> Any:
        """Update the state"""
        ...
