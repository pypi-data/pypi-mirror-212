from typing import Any

import jijzept as jz

from jijzeptlab.response.util import _recursive_deserialize


class JijZeptLabResult:
    """
    JijZeptLabResult which is used to store results
    """

    def __init__(self, variables: dict):
        """constructor

        Args:
            variables (dict): variables to be stored
        """
        # attempt to deserialize if the response includes `jm.SampleSet` or `jm.Problem`
        # if failed, return the original object
        self.variables = _recursive_deserialize(variables)


class JijZeptLabResponse(jz.response.BaseResponse, JijZeptLabResult):
    """JijZeptLabResponse which is used to get result from the server"""

    @classmethod
    def from_json_obj(cls, json_obj) -> Any:
        """Generate object from JSON object.

        Args:
            json_obj (dict): JSON object as a dictionary.
        """

        return cls(json_obj)

    @classmethod
    def empty_data(cls) -> Any:
        return cls({})

    def __repr__(self):
        return JijZeptLabResult.__repr__(self)

    def __str__(self):
        return (
            jz.response.BaseResponse.__repr__(self)
            + "\n"
            + JijZeptLabResult.__str__(self)
        )
