from __future__ import annotations

import inspect
import textwrap
import typing as typ

from dataclasses import dataclass, field

import jijmodeling as jm
import numpy as np

from jijzept.client import JijZeptClient
from jijzept.config.path_type import PATH_TYPE
from jijzept.exception.exception import (
    JijZeptSolvingFailedError,
    JijZeptSolvingUnknownError,
    JijZeptSolvingValidationError
)
from jijzept.instance_translator.instance_translator import InstanceTranslator
from jijzept.post_api import post_instance_and_query
from jijzept.response.base import APIStatus
from jijzeptlab.response import JijZeptLabResponse


@dataclass
class InputData:
    """input data for specifing problem, instance_data, and fixed_variables
    This class is used for submit informations of problem, instance_data, and fixed_variables.

    Attributes:
        problem (jm.Problem): Problem.
        instance_data (dict[str, list | np.ndarray]): Instance data.
        fixed_variables (dict[str, dict[tuple[int, ...], int]]): Fixed variables.

    Examples:
        ```python
        import jijmodeling as jm
        d = jm.Placeholder("d", dim=1)
        x = jm.Integer("x", shape=d.shape, lower=0, upper=100)
        i = jm.Element("i", d.shape[0])
        problem = jm.Problem("test")
        problem += jm.Sum(i, d[i]*x[i])
        problem += jm.Constraint("one-hot", jm.Sum(i, x[i]) == 1)

        instance_data = {"d": [1, 2, 3]}

        # define problem and instance_data as an `InputData`
        input_data = jzl.client.InputData(problem, instance_data)
        ```
    """

    problem: jm.Problem
    instance_data: dict[str, list | np.ndarray] = field(default_factory=dict)
    fixed_variables: dict[str, dict[tuple[int, ...], int]] = field(default_factory=dict)


class JijZeptLabClient:
    """JijZeptLab client class."""

    def __init__(
        self,
        token: str | None = None,
        url: str | None = None,
        proxy: str | None = None,
        config: PATH_TYPE | None = None,
        config_env: str = "default",
    ):
        """Sets token and url.
        If you do not set any arguments, JijZept configuration file is used.
        If you set the url or token here, that will be used as the priority setting for connecting to the API.
        See JijZeptClient for details.
        Args:
            token (str | None, optional): Token string. Defaults to None.
            url (str | None, optional): API URL. Defaults to None.
            proxy (str | None, optional): Proxy URL. Defaults to None.
            config (str | None, optional): Config file path. Defaults to None.
            config_env (str, optional): configure environment name. Defaults to 'default'.
        Raises:
            TypeError: `token`, `url`, or `config` is not str.
        """
        self.client = JijZeptClient(
            url=url, token=token, proxy=proxy, config=config, config_env=config_env
        )

    def submit(
        self,
        code_string: str,
        result_variables: list[str],
        input_data: typ.Optional[InputData] = None,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str = "jijzeptlabsolver",
    ) -> JijZeptLabResponse:
        """submit job to the server
        this method submits the script specified by `code_string` to the server with `InputData` object.

        Args:
            code_string (str): Code string.
            result_variables (list[str]): Result variables. This variables are returned as a result.
            input_data (Optional[InputData], optional): Input data for specifing problem, instance_data, and fixed_variables. Defaults to None.
            max_wait_time (int | float | None, optional): Max wait time. Defaults to None.
            sync (bool, optional): Sync. Defaults to True.
            queue_name (str, optional): Queue name. Defaults to "jijzeptlabsolver".

        Returns:
            JijZeptLabResponse: JijZeptLabResponse
        """
        instance: dict[str, typ.Any] = {
            "python_source": code_string,
        }

        if input_data is not None:
            problem = input_data.problem
            instance_data = input_data.instance_data
            fixed_variables = input_data.fixed_variables

            instance["problem"] = jm.to_serializable(problem)

            instance["instance_data"] = InstanceTranslator.instance_translate(
                instance_data
            )

            instance["fixed_variables"] = jm.utils.serialize_fixed_var(fixed_variables)

        response = post_instance_and_query(
            JijZeptLabResponse,
            client=self.client,
            instance_type="PythonCode",
            instance=instance,
            queue_name=queue_name,
            solver="JijZeptLabSolver",
            parameters={"result": result_variables},
            timeout=max_wait_time,
            sync=sync,
        )

        # Raise error if the problem is not solved.
        if response.status == APIStatus.FAILED:
            raise JijZeptSolvingFailedError(
                response.error_message.get("message", "The problem is not solved.")
            )
        elif response.status == APIStatus.UNKNOWNERROR:
            raise JijZeptSolvingUnknownError(
                response.error_message.get("message", "The problem is not solved.")
            )
        elif response.status == APIStatus.VALIDATIONERROR:
            raise JijZeptSolvingValidationError(
                response.error_message.get("message", "The problem is not solved.")
            )

        return response

    def submit_func(
        self,
        func: typ.Callable,
        result_variables: list[str],
        input_data: typ.Optional[InputData] = None,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str = "jijzeptlabsolver",
    ) -> JijZeptLabResponse:
        """submit job to the server (with function)
        This method submits the script specified by the function `func` to the server with `InputData` object.

        Args:
            func (typ.Callable): Function.
            result_variables (list[str]): Result variables. This variables are returned as a result.
            input_data (Optional[InputData], optional): Input data for specifing problem, instance_data, and fixed_variables. Defaults to None.
            max_wait_time (int | float | None, optional): Max wait time. Defaults to None.
            sync (bool, optional): Sync. Defaults to True.
            queue_name (str, optional): Queue name. Defaults to "jijzeptlabsolver".

        Returns:
            JijZeptLabResponse: JijZeptLabResponse

        Examples:
            ```python
            # This function is executed on the server side.
            def script_on_server_side():
                import jijzeptlab as jzl
                import jijmodeling as jm
                # we are going to solve knapsack problem using MIP solver in this tutorial
                # of course we can switch to quantum Ising sampler
                import jijzeptlab.solver.mip as mip
                # problem, instance_data are pre-defined
                problem: jm.Problem
                instance_data: dict
                # compile the problem to generate intermediate representation
                # note that we have to pass `instance_data` via `jzl.InstanceData` object

                compiled_model = jzl.compile_model(problem, jzl.InstanceData.from_dict(instance_data))
                # initialize MIP instance
                mip_model = mip.create_model(compiled_model)
                # solve
                mip_result = mip.solve(mip_model, )
                # convert the solution to `jm.SampleSet`。
                final_solution = mip_result.to_sample_set()


            import jijmodeling as jm
            d = jm.Placeholder("d", dim=1)
            x = jm.Integer("x", shape=d.shape, lower=0, upper=100)
            i = jm.Element("i", d.shape[0])
            problem = jm.Problem("test")
            problem += jm.Sum(i, d[i]*x[i])
            problem += jm.Constraint("one-hot", jm.Sum(i, x[i]) == 1)

            instance_data = {"d": [1, 2, 3]}

            import jijzeptlab as jzl
            client = jzl.client.JijZeptLabClient(config="./config.toml")
            input_data = jzl.client.InputData(problem, instance_data)
            # submit job
            result = client.submit_func(script_on_server_side, ["final_solution"], input_data)
            print(result.variables)
            ```

        """

        source_code = inspect.getsource(func)

        # Split the source code into lines
        lines = source_code.splitlines()

        # Remove the first line (function definition)
        lines = lines[1:]

        # Join the lines back together
        inside_function_code = "\n".join(lines)

        # Use textwrap.dedent to remove any common leading whitespace from every line
        code_string = textwrap.dedent(inside_function_code)

        return self.submit(
            code_string, result_variables, input_data, max_wait_time, sync, queue_name
        )

    def submit_file(
        self,
        filepath: str,
        result_variables: list[str],
        input_data: typ.Optional[InputData] = None,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str = "jijzeptlabsolver",
    ):
        """submit job to the server (with source code file)
        This method submits the script specified by the file `filepath` to the server with `InputData` object.

        Args:
            filepath (str): _description_
            result_variables (list[str]): _description_
            input_data (typ.Optional[InputData], optional): _description_. Defaults to None.
            max_wait_time (int | float | None, optional): _description_. Defaults to None.
            sync (bool, optional): _description_. Defaults to True.
            queue_name (str, optional): _description_. Defaults to "jijzeptlabsolver".

        Returns:
            JijZeptLabResponse: JijZeptLabResponse

        Examples:
            ```python
            import jijmodeling as jm
            d = jm.Placeholder("d", dim=1)
            x = jm.Integer("x", shape=d.shape, lower=0, upper=100)
            i = jm.Element("i", d.shape[0])
            problem = jm.Problem("test")
            problem += jm.Sum(i, d[i]*x[i])
            problem += jm.Constraint("one-hot", jm.Sum(i, x[i]) == 1)

            instance_data = {"d": [1, 2, 3]}
            import jijzeptlab as jzl
            client = jzl.client.JijZeptLabClient(config="./config.toml")
            input_data = jzl.client.InputData(problem, instance_data)
            # submit job (script.py is the file name of the job script)
            result = client.submit_file("./script.py", ["final_solution"], input_data)
            print(result.variables)
            ```
        """
        code_string: str = ""
        with open(filepath, "r") as f:
            code_string = f.read()

        return self.submit(
            code_string, result_variables, input_data, max_wait_time, sync, queue_name
        )
