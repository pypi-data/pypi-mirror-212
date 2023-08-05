# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['TopicArgs', 'Topic']

@pulumi.input_type
class TopicArgs:
    def __init__(__self__, *,
                 avatar: Optional[pulumi.Input[str]] = None,
                 avatar_hash: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 soft_destroy: Optional[pulumi.Input[bool]] = None,
                 title: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Topic resource.
        :param pulumi.Input[str] avatar: A local path to the avatar image to upload. **Note**: not available for imported resources.
        :param pulumi.Input[str] avatar_hash: The hash of the avatar image. Use `filesha256("path/to/avatar.png")` whenever possible. **Note**: this is used to trigger an update of the avatar. If it's not given, but an avatar is given, the avatar will be updated each time.
        :param pulumi.Input[str] description: A text describing the topic.
        :param pulumi.Input[str] name: The topic's name.
        :param pulumi.Input[bool] soft_destroy: Empty the topics fields instead of deleting it.
        :param pulumi.Input[str] title: The topic's description. Requires at least GitLab 15.0 for which it's a required argument.
        """
        if avatar is not None:
            pulumi.set(__self__, "avatar", avatar)
        if avatar_hash is not None:
            pulumi.set(__self__, "avatar_hash", avatar_hash)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if soft_destroy is not None:
            warnings.warn("""GitLab 14.9 introduced the proper deletion of topics. This field is no longer needed.""", DeprecationWarning)
            pulumi.log.warn("""soft_destroy is deprecated: GitLab 14.9 introduced the proper deletion of topics. This field is no longer needed.""")
        if soft_destroy is not None:
            pulumi.set(__self__, "soft_destroy", soft_destroy)
        if title is not None:
            pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter
    def avatar(self) -> Optional[pulumi.Input[str]]:
        """
        A local path to the avatar image to upload. **Note**: not available for imported resources.
        """
        return pulumi.get(self, "avatar")

    @avatar.setter
    def avatar(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "avatar", value)

    @property
    @pulumi.getter(name="avatarHash")
    def avatar_hash(self) -> Optional[pulumi.Input[str]]:
        """
        The hash of the avatar image. Use `filesha256("path/to/avatar.png")` whenever possible. **Note**: this is used to trigger an update of the avatar. If it's not given, but an avatar is given, the avatar will be updated each time.
        """
        return pulumi.get(self, "avatar_hash")

    @avatar_hash.setter
    def avatar_hash(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "avatar_hash", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A text describing the topic.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The topic's name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="softDestroy")
    def soft_destroy(self) -> Optional[pulumi.Input[bool]]:
        """
        Empty the topics fields instead of deleting it.
        """
        return pulumi.get(self, "soft_destroy")

    @soft_destroy.setter
    def soft_destroy(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "soft_destroy", value)

    @property
    @pulumi.getter
    def title(self) -> Optional[pulumi.Input[str]]:
        """
        The topic's description. Requires at least GitLab 15.0 for which it's a required argument.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "title", value)


@pulumi.input_type
class _TopicState:
    def __init__(__self__, *,
                 avatar: Optional[pulumi.Input[str]] = None,
                 avatar_hash: Optional[pulumi.Input[str]] = None,
                 avatar_url: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 soft_destroy: Optional[pulumi.Input[bool]] = None,
                 title: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Topic resources.
        :param pulumi.Input[str] avatar: A local path to the avatar image to upload. **Note**: not available for imported resources.
        :param pulumi.Input[str] avatar_hash: The hash of the avatar image. Use `filesha256("path/to/avatar.png")` whenever possible. **Note**: this is used to trigger an update of the avatar. If it's not given, but an avatar is given, the avatar will be updated each time.
        :param pulumi.Input[str] avatar_url: The URL of the avatar image.
        :param pulumi.Input[str] description: A text describing the topic.
        :param pulumi.Input[str] name: The topic's name.
        :param pulumi.Input[bool] soft_destroy: Empty the topics fields instead of deleting it.
        :param pulumi.Input[str] title: The topic's description. Requires at least GitLab 15.0 for which it's a required argument.
        """
        if avatar is not None:
            pulumi.set(__self__, "avatar", avatar)
        if avatar_hash is not None:
            pulumi.set(__self__, "avatar_hash", avatar_hash)
        if avatar_url is not None:
            pulumi.set(__self__, "avatar_url", avatar_url)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if soft_destroy is not None:
            warnings.warn("""GitLab 14.9 introduced the proper deletion of topics. This field is no longer needed.""", DeprecationWarning)
            pulumi.log.warn("""soft_destroy is deprecated: GitLab 14.9 introduced the proper deletion of topics. This field is no longer needed.""")
        if soft_destroy is not None:
            pulumi.set(__self__, "soft_destroy", soft_destroy)
        if title is not None:
            pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter
    def avatar(self) -> Optional[pulumi.Input[str]]:
        """
        A local path to the avatar image to upload. **Note**: not available for imported resources.
        """
        return pulumi.get(self, "avatar")

    @avatar.setter
    def avatar(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "avatar", value)

    @property
    @pulumi.getter(name="avatarHash")
    def avatar_hash(self) -> Optional[pulumi.Input[str]]:
        """
        The hash of the avatar image. Use `filesha256("path/to/avatar.png")` whenever possible. **Note**: this is used to trigger an update of the avatar. If it's not given, but an avatar is given, the avatar will be updated each time.
        """
        return pulumi.get(self, "avatar_hash")

    @avatar_hash.setter
    def avatar_hash(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "avatar_hash", value)

    @property
    @pulumi.getter(name="avatarUrl")
    def avatar_url(self) -> Optional[pulumi.Input[str]]:
        """
        The URL of the avatar image.
        """
        return pulumi.get(self, "avatar_url")

    @avatar_url.setter
    def avatar_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "avatar_url", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A text describing the topic.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The topic's name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="softDestroy")
    def soft_destroy(self) -> Optional[pulumi.Input[bool]]:
        """
        Empty the topics fields instead of deleting it.
        """
        return pulumi.get(self, "soft_destroy")

    @soft_destroy.setter
    def soft_destroy(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "soft_destroy", value)

    @property
    @pulumi.getter
    def title(self) -> Optional[pulumi.Input[str]]:
        """
        The topic's description. Requires at least GitLab 15.0 for which it's a required argument.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "title", value)


class Topic(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 avatar: Optional[pulumi.Input[str]] = None,
                 avatar_hash: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 soft_destroy: Optional[pulumi.Input[bool]] = None,
                 title: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The `Topic` resource allows to manage the lifecycle of topics that are then assignable to projects.

        > Topics are the successors for project tags. Aside from avoiding terminology collisions with Git tags, they are more descriptive and better searchable.

        > Deleting a topic was implemented in GitLab 14.9. For older versions of GitLab set `soft_destroy = true` to empty out a topic instead of deleting it.

        **Upstream API**: [GitLab REST API docs for topics](https://docs.gitlab.com/ee/api/topics.html)

        ## Import

        ```sh
         $ pulumi import gitlab:index/topic:Topic You can import a topic to terraform state using `<resource> <id>`.
        ```

         The `id` must be an integer for the id of the topic you want to import, for example

        ```sh
         $ pulumi import gitlab:index/topic:Topic functional_programming 1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] avatar: A local path to the avatar image to upload. **Note**: not available for imported resources.
        :param pulumi.Input[str] avatar_hash: The hash of the avatar image. Use `filesha256("path/to/avatar.png")` whenever possible. **Note**: this is used to trigger an update of the avatar. If it's not given, but an avatar is given, the avatar will be updated each time.
        :param pulumi.Input[str] description: A text describing the topic.
        :param pulumi.Input[str] name: The topic's name.
        :param pulumi.Input[bool] soft_destroy: Empty the topics fields instead of deleting it.
        :param pulumi.Input[str] title: The topic's description. Requires at least GitLab 15.0 for which it's a required argument.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[TopicArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The `Topic` resource allows to manage the lifecycle of topics that are then assignable to projects.

        > Topics are the successors for project tags. Aside from avoiding terminology collisions with Git tags, they are more descriptive and better searchable.

        > Deleting a topic was implemented in GitLab 14.9. For older versions of GitLab set `soft_destroy = true` to empty out a topic instead of deleting it.

        **Upstream API**: [GitLab REST API docs for topics](https://docs.gitlab.com/ee/api/topics.html)

        ## Import

        ```sh
         $ pulumi import gitlab:index/topic:Topic You can import a topic to terraform state using `<resource> <id>`.
        ```

         The `id` must be an integer for the id of the topic you want to import, for example

        ```sh
         $ pulumi import gitlab:index/topic:Topic functional_programming 1
        ```

        :param str resource_name: The name of the resource.
        :param TopicArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TopicArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 avatar: Optional[pulumi.Input[str]] = None,
                 avatar_hash: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 soft_destroy: Optional[pulumi.Input[bool]] = None,
                 title: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TopicArgs.__new__(TopicArgs)

            __props__.__dict__["avatar"] = avatar
            __props__.__dict__["avatar_hash"] = avatar_hash
            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            if soft_destroy is not None and not opts.urn:
                warnings.warn("""GitLab 14.9 introduced the proper deletion of topics. This field is no longer needed.""", DeprecationWarning)
                pulumi.log.warn("""soft_destroy is deprecated: GitLab 14.9 introduced the proper deletion of topics. This field is no longer needed.""")
            __props__.__dict__["soft_destroy"] = soft_destroy
            __props__.__dict__["title"] = title
            __props__.__dict__["avatar_url"] = None
        super(Topic, __self__).__init__(
            'gitlab:index/topic:Topic',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            avatar: Optional[pulumi.Input[str]] = None,
            avatar_hash: Optional[pulumi.Input[str]] = None,
            avatar_url: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            soft_destroy: Optional[pulumi.Input[bool]] = None,
            title: Optional[pulumi.Input[str]] = None) -> 'Topic':
        """
        Get an existing Topic resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] avatar: A local path to the avatar image to upload. **Note**: not available for imported resources.
        :param pulumi.Input[str] avatar_hash: The hash of the avatar image. Use `filesha256("path/to/avatar.png")` whenever possible. **Note**: this is used to trigger an update of the avatar. If it's not given, but an avatar is given, the avatar will be updated each time.
        :param pulumi.Input[str] avatar_url: The URL of the avatar image.
        :param pulumi.Input[str] description: A text describing the topic.
        :param pulumi.Input[str] name: The topic's name.
        :param pulumi.Input[bool] soft_destroy: Empty the topics fields instead of deleting it.
        :param pulumi.Input[str] title: The topic's description. Requires at least GitLab 15.0 for which it's a required argument.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TopicState.__new__(_TopicState)

        __props__.__dict__["avatar"] = avatar
        __props__.__dict__["avatar_hash"] = avatar_hash
        __props__.__dict__["avatar_url"] = avatar_url
        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        __props__.__dict__["soft_destroy"] = soft_destroy
        __props__.__dict__["title"] = title
        return Topic(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def avatar(self) -> pulumi.Output[Optional[str]]:
        """
        A local path to the avatar image to upload. **Note**: not available for imported resources.
        """
        return pulumi.get(self, "avatar")

    @property
    @pulumi.getter(name="avatarHash")
    def avatar_hash(self) -> pulumi.Output[str]:
        """
        The hash of the avatar image. Use `filesha256("path/to/avatar.png")` whenever possible. **Note**: this is used to trigger an update of the avatar. If it's not given, but an avatar is given, the avatar will be updated each time.
        """
        return pulumi.get(self, "avatar_hash")

    @property
    @pulumi.getter(name="avatarUrl")
    def avatar_url(self) -> pulumi.Output[str]:
        """
        The URL of the avatar image.
        """
        return pulumi.get(self, "avatar_url")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A text describing the topic.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The topic's name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="softDestroy")
    def soft_destroy(self) -> pulumi.Output[Optional[bool]]:
        """
        Empty the topics fields instead of deleting it.
        """
        return pulumi.get(self, "soft_destroy")

    @property
    @pulumi.getter
    def title(self) -> pulumi.Output[Optional[str]]:
        """
        The topic's description. Requires at least GitLab 15.0 for which it's a required argument.
        """
        return pulumi.get(self, "title")

