# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetProjectVariableResult',
    'AwaitableGetProjectVariableResult',
    'get_project_variable',
    'get_project_variable_output',
]

@pulumi.output_type
class GetProjectVariableResult:
    """
    A collection of values returned by getProjectVariable.
    """
    def __init__(__self__, environment_scope=None, id=None, key=None, masked=None, project=None, protected=None, raw=None, value=None, variable_type=None):
        if environment_scope and not isinstance(environment_scope, str):
            raise TypeError("Expected argument 'environment_scope' to be a str")
        pulumi.set(__self__, "environment_scope", environment_scope)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if key and not isinstance(key, str):
            raise TypeError("Expected argument 'key' to be a str")
        pulumi.set(__self__, "key", key)
        if masked and not isinstance(masked, bool):
            raise TypeError("Expected argument 'masked' to be a bool")
        pulumi.set(__self__, "masked", masked)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if protected and not isinstance(protected, bool):
            raise TypeError("Expected argument 'protected' to be a bool")
        pulumi.set(__self__, "protected", protected)
        if raw and not isinstance(raw, bool):
            raise TypeError("Expected argument 'raw' to be a bool")
        pulumi.set(__self__, "raw", raw)
        if value and not isinstance(value, str):
            raise TypeError("Expected argument 'value' to be a str")
        pulumi.set(__self__, "value", value)
        if variable_type and not isinstance(variable_type, str):
            raise TypeError("Expected argument 'variable_type' to be a str")
        pulumi.set(__self__, "variable_type", variable_type)

    @property
    @pulumi.getter(name="environmentScope")
    def environment_scope(self) -> str:
        """
        The environment scope of the variable. Defaults to all environment (`*`). Note that in Community Editions of Gitlab, values other than `*` will cause inconsistent plans.
        """
        return pulumi.get(self, "environment_scope")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The name of the variable.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def masked(self) -> bool:
        """
        If set to `true`, the value of the variable will be hidden in job logs. The value must meet the [masking requirements](https://docs.gitlab.com/ee/ci/variables/#masked-variables). Defaults to `false`.
        """
        return pulumi.get(self, "masked")

    @property
    @pulumi.getter
    def project(self) -> str:
        """
        The name or id of the project.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def protected(self) -> bool:
        """
        If set to `true`, the variable will be passed only to pipelines running on protected branches and tags. Defaults to `false`.
        """
        return pulumi.get(self, "protected")

    @property
    @pulumi.getter
    def raw(self) -> bool:
        """
        Whether the variable is treated as a raw string. Default: false. When true, variables in the value are not expanded.
        """
        return pulumi.get(self, "raw")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value of the variable.
        """
        return pulumi.get(self, "value")

    @property
    @pulumi.getter(name="variableType")
    def variable_type(self) -> str:
        """
        The type of a variable. Valid values are: `env_var`, `file`. Default is `env_var`.
        """
        return pulumi.get(self, "variable_type")


class AwaitableGetProjectVariableResult(GetProjectVariableResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProjectVariableResult(
            environment_scope=self.environment_scope,
            id=self.id,
            key=self.key,
            masked=self.masked,
            project=self.project,
            protected=self.protected,
            raw=self.raw,
            value=self.value,
            variable_type=self.variable_type)


def get_project_variable(environment_scope: Optional[str] = None,
                         key: Optional[str] = None,
                         project: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProjectVariableResult:
    """
    The `ProjectVariable` data source allows to retrieve details about a project-level CI/CD variable.

    **Upstream API**: [GitLab REST API docs](https://docs.gitlab.com/ee/api/project_level_variables.html)

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gitlab as gitlab

    foo = gitlab.get_project_variable(key="foo",
        project="my/example/project")
    bar = gitlab.get_project_variable(environment_scope="staging/*",
        key="bar",
        project="my/example/project")
    ```


    :param str environment_scope: The environment scope of the variable. Defaults to all environment (`*`). Note that in Community Editions of Gitlab, values other than `*` will cause inconsistent plans.
    :param str key: The name of the variable.
    :param str project: The name or id of the project.
    """
    __args__ = dict()
    __args__['environmentScope'] = environment_scope
    __args__['key'] = key
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gitlab:index/getProjectVariable:getProjectVariable', __args__, opts=opts, typ=GetProjectVariableResult).value

    return AwaitableGetProjectVariableResult(
        environment_scope=__ret__.environment_scope,
        id=__ret__.id,
        key=__ret__.key,
        masked=__ret__.masked,
        project=__ret__.project,
        protected=__ret__.protected,
        raw=__ret__.raw,
        value=__ret__.value,
        variable_type=__ret__.variable_type)


@_utilities.lift_output_func(get_project_variable)
def get_project_variable_output(environment_scope: Optional[pulumi.Input[Optional[str]]] = None,
                                key: Optional[pulumi.Input[str]] = None,
                                project: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetProjectVariableResult]:
    """
    The `ProjectVariable` data source allows to retrieve details about a project-level CI/CD variable.

    **Upstream API**: [GitLab REST API docs](https://docs.gitlab.com/ee/api/project_level_variables.html)

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gitlab as gitlab

    foo = gitlab.get_project_variable(key="foo",
        project="my/example/project")
    bar = gitlab.get_project_variable(environment_scope="staging/*",
        key="bar",
        project="my/example/project")
    ```


    :param str environment_scope: The environment scope of the variable. Defaults to all environment (`*`). Note that in Community Editions of Gitlab, values other than `*` will cause inconsistent plans.
    :param str key: The name of the variable.
    :param str project: The name or id of the project.
    """
    ...
