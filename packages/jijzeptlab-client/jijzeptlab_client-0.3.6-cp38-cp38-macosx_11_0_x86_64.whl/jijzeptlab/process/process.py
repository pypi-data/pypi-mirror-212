from __future__ import annotations

import enum

import jijmodeling as jm
import jijmodeling.transpiler as jmt
import jijzeptlab as jzl


class ProcessLabel:
    compile_model = enum.auto()
    transpile_to_mip = enum.auto()
    solve_mip = enum.auto()


class Process:
    def compile_model(
        self,
        problem: jm.Problem,
        instance_data: jzl.InstanceData,
        fixed_variables: jzl.FixedVariables,
        option: jzl.CompileOption,
    ) -> jzl.CompiledInstance:
        jmt_compiled_instance = jmt.core.compile_model(
            problem, instance_data.to_dict(), fixed_variables.to_dict()
        )
        compiled_instance = jzl.CompiledInstance(
            jmt_compiled_instance, option, problem, instance_data, fixed_variables
        )

        return compiled_instance


BackendProcess = Process()
