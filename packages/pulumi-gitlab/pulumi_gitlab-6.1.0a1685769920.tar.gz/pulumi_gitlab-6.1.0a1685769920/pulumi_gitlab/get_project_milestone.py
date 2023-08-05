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
    'GetProjectMilestoneResult',
    'AwaitableGetProjectMilestoneResult',
    'get_project_milestone',
    'get_project_milestone_output',
]

@pulumi.output_type
class GetProjectMilestoneResult:
    """
    A collection of values returned by getProjectMilestone.
    """
    def __init__(__self__, created_at=None, description=None, due_date=None, expired=None, id=None, iid=None, milestone_id=None, project=None, project_id=None, start_date=None, state=None, title=None, updated_at=None, web_url=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if due_date and not isinstance(due_date, str):
            raise TypeError("Expected argument 'due_date' to be a str")
        pulumi.set(__self__, "due_date", due_date)
        if expired and not isinstance(expired, bool):
            raise TypeError("Expected argument 'expired' to be a bool")
        pulumi.set(__self__, "expired", expired)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if iid and not isinstance(iid, int):
            raise TypeError("Expected argument 'iid' to be a int")
        pulumi.set(__self__, "iid", iid)
        if milestone_id and not isinstance(milestone_id, int):
            raise TypeError("Expected argument 'milestone_id' to be a int")
        pulumi.set(__self__, "milestone_id", milestone_id)
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        pulumi.set(__self__, "project", project)
        if project_id and not isinstance(project_id, int):
            raise TypeError("Expected argument 'project_id' to be a int")
        pulumi.set(__self__, "project_id", project_id)
        if start_date and not isinstance(start_date, str):
            raise TypeError("Expected argument 'start_date' to be a str")
        pulumi.set(__self__, "start_date", start_date)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if title and not isinstance(title, str):
            raise TypeError("Expected argument 'title' to be a str")
        pulumi.set(__self__, "title", title)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)
        if web_url and not isinstance(web_url, str):
            raise TypeError("Expected argument 'web_url' to be a str")
        pulumi.set(__self__, "web_url", web_url)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        The time of creation of the milestone. Date time string, ISO 8601 formatted, for example 2016-03-11T03:45:40Z.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of the milestone.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="dueDate")
    def due_date(self) -> str:
        """
        The due date of the milestone. Date time string in the format YYYY-MM-DD, for example 2016-03-11.
        """
        return pulumi.get(self, "due_date")

    @property
    @pulumi.getter
    def expired(self) -> bool:
        """
        Bool, true if milestone expired.
        """
        return pulumi.get(self, "expired")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def iid(self) -> int:
        """
        The ID of the project's milestone.
        """
        return pulumi.get(self, "iid")

    @property
    @pulumi.getter(name="milestoneId")
    def milestone_id(self) -> int:
        """
        The instance-wide ID of the project’s milestone.
        """
        return pulumi.get(self, "milestone_id")

    @property
    @pulumi.getter
    def project(self) -> str:
        """
        The ID or URL-encoded path of the project owned by the authenticated user.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> int:
        """
        The project ID of milestone.
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter(name="startDate")
    def start_date(self) -> str:
        """
        The start date of the milestone. Date time string in the format YYYY-MM-DD, for example 2016-03-11.
        """
        return pulumi.get(self, "start_date")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The state of the milestone. Valid values are: `active`, `closed`.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def title(self) -> str:
        """
        The title of a milestone.
        """
        return pulumi.get(self, "title")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        """
        The last update time of the milestone. Date time string, ISO 8601 formatted, for example 2016-03-11T03:45:40Z.
        """
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter(name="webUrl")
    def web_url(self) -> str:
        """
        The web URL of the milestone.
        """
        return pulumi.get(self, "web_url")


class AwaitableGetProjectMilestoneResult(GetProjectMilestoneResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProjectMilestoneResult(
            created_at=self.created_at,
            description=self.description,
            due_date=self.due_date,
            expired=self.expired,
            id=self.id,
            iid=self.iid,
            milestone_id=self.milestone_id,
            project=self.project,
            project_id=self.project_id,
            start_date=self.start_date,
            state=self.state,
            title=self.title,
            updated_at=self.updated_at,
            web_url=self.web_url)


def get_project_milestone(milestone_id: Optional[int] = None,
                          project: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProjectMilestoneResult:
    """
    The `ProjectMilestone` data source allows get details of a project milestone.

    **Upstream API**: [GitLab REST API docs](https://docs.gitlab.com/ee/api/milestones.html)

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gitlab as gitlab

    example = gitlab.get_project_milestone(milestone_id=10,
        project="foo/bar")
    ```


    :param int milestone_id: The instance-wide ID of the project’s milestone.
    :param str project: The ID or URL-encoded path of the project owned by the authenticated user.
    """
    __args__ = dict()
    __args__['milestoneId'] = milestone_id
    __args__['project'] = project
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('gitlab:index/getProjectMilestone:getProjectMilestone', __args__, opts=opts, typ=GetProjectMilestoneResult).value

    return AwaitableGetProjectMilestoneResult(
        created_at=__ret__.created_at,
        description=__ret__.description,
        due_date=__ret__.due_date,
        expired=__ret__.expired,
        id=__ret__.id,
        iid=__ret__.iid,
        milestone_id=__ret__.milestone_id,
        project=__ret__.project,
        project_id=__ret__.project_id,
        start_date=__ret__.start_date,
        state=__ret__.state,
        title=__ret__.title,
        updated_at=__ret__.updated_at,
        web_url=__ret__.web_url)


@_utilities.lift_output_func(get_project_milestone)
def get_project_milestone_output(milestone_id: Optional[pulumi.Input[int]] = None,
                                 project: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetProjectMilestoneResult]:
    """
    The `ProjectMilestone` data source allows get details of a project milestone.

    **Upstream API**: [GitLab REST API docs](https://docs.gitlab.com/ee/api/milestones.html)

    ## Example Usage

    ```python
    import pulumi
    import pulumi_gitlab as gitlab

    example = gitlab.get_project_milestone(milestone_id=10,
        project="foo/bar")
    ```


    :param int milestone_id: The instance-wide ID of the project’s milestone.
    :param str project: The ID or URL-encoded path of the project owned by the authenticated user.
    """
    ...
