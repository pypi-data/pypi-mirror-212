from __future__ import annotations


class FixedVariables:
    """Fixed variables class for JijZeptLab"""

    def __init__(self) -> None:
        """
        initialze FixedVariables
        """
        self._fixed_vars = {}

    def insert(self, key: str | tuple[str, list[int]], value: float):
        """insert fixed variable

        Args:
            key (str | tuple[str, list[int]]): key of fixed variable
            value (float): value of fixed variable
        """
        key_: tuple[str, list[int]]
        if isinstance(key, str):
            key_ = (key, [])
        else:
            key_ = key

        if key_[0] not in self._fixed_vars:
            self._fixed_vars[key_[0]] = {}
        self._fixed_vars[key_[0]][tuple(key_[1])] = value

    @classmethod
    def from_dict(
        cls, dict_data: dict[str, dict[tuple[int, ...], float | int]]
    ) -> "FixedVariables":
        """generate `FixedVariables` from dict object

        Args:
            dict_data (dict): fixed variables with a dict object

        Returns:
            FixedVariables: fixed variables for JijZeptLab

        Examples:
            ```python
            import jijzeptlab as jzl
            # x[8] and x[9] are fixed to 1
            fixed_variables = {'x':{(8,):1,(9,):1}
            fixed_variables = jzl.FixedVariables.from_dict(fixed_variables)
            ```
        """

        fixed_vars = cls()
        fixed_vars._fixed_vars = dict_data
        return fixed_vars

    def to_dict(self) -> dict[str, dict[tuple[int, ...], float | int]]:
        """convert to dict object

        Returns:
            dict: fixed variables with dict object

        Examples:
            ```python
            import jijzeptlab as jzl
            # x[8] and x[9] are fixed to 1
            fixed_variables = {'x':{(8,):1,(9,):1}
            fixed_variables = jzl.FixedVariables.from_dict(fixed_variables)
            print(fixed_variables.to_dict()) # {'x':{(8,):1,(9,):1}
            ```
        """
        return self._fixed_vars


class InstanceData:
    """Instance data class for JijZeptLab"""

    def __init__(self) -> None:
        """
        initialze InstanceData

        Args:
            dict_data (dict): Instance data
        """
        self._instance_data = {}

    @classmethod
    def from_dict(cls, dict_data: dict) -> InstanceData:
        """generate `InstanceData` from dict object

        Args:
            dict_data (dict): instance data with a dict object

        Returns:
            InstanceData: instance data for JijZeptLab

        Examples:
            ```python
            import jijzeptlab as jzl

            instance_data = {"d": [1, 2, 3]}
            instance_data = jzl.InstanceData.from_dict(instance_data)
            ```
        """
        instance_data = cls()
        instance_data._instance_data = dict_data
        return instance_data

    def insert(self, name: str, value):
        """insert element to instance data

        Args:
            name (str): name of element
            value (any): value of element
        """
        self._instance_data[name] = value

    def to_dict(self) -> dict:
        """convert to dict object

        Returns:
            dict: instance data with dict object

        Examples:
            ```python
            import jijzeptlab as jzl
            instance_data = {"d": [1, 2, 3]}
            instance_data = jzl.InstanceData.from_dict(instance_data)
            print(instance_data.to_dict()) # {"d": [1, 2, 3]}
            ```

        """
        return self._instance_data
