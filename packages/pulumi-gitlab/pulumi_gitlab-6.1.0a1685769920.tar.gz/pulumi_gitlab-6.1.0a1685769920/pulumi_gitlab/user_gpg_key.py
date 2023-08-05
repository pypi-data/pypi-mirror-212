# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['UserGpgKeyArgs', 'UserGpgKey']

@pulumi.input_type
class UserGpgKeyArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 user_id: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a UserGpgKey resource.
        :param pulumi.Input[str] key: The armored GPG public key.
        :param pulumi.Input[int] user_id: The ID of the user to add the GPG key to. If this field is omitted, this resource manages a GPG key for the current user. Otherwise, this resource manages a GPG key for the specified user, and an admin token is required.
        """
        pulumi.set(__self__, "key", key)
        if user_id is not None:
            pulumi.set(__self__, "user_id", user_id)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        The armored GPG public key.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> Optional[pulumi.Input[int]]:
        """
        The ID of the user to add the GPG key to. If this field is omitted, this resource manages a GPG key for the current user. Otherwise, this resource manages a GPG key for the specified user, and an admin token is required.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "user_id", value)


@pulumi.input_type
class _UserGpgKeyState:
    def __init__(__self__, *,
                 created_at: Optional[pulumi.Input[str]] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 key_id: Optional[pulumi.Input[int]] = None,
                 user_id: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering UserGpgKey resources.
        :param pulumi.Input[str] created_at: The time when this key was created in GitLab.
        :param pulumi.Input[str] key: The armored GPG public key.
        :param pulumi.Input[int] key_id: The ID of the GPG key.
        :param pulumi.Input[int] user_id: The ID of the user to add the GPG key to. If this field is omitted, this resource manages a GPG key for the current user. Otherwise, this resource manages a GPG key for the specified user, and an admin token is required.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if key is not None:
            pulumi.set(__self__, "key", key)
        if key_id is not None:
            pulumi.set(__self__, "key_id", key_id)
        if user_id is not None:
            pulumi.set(__self__, "user_id", user_id)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[str]]:
        """
        The time when this key was created in GitLab.
        """
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter
    def key(self) -> Optional[pulumi.Input[str]]:
        """
        The armored GPG public key.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> Optional[pulumi.Input[int]]:
        """
        The ID of the GPG key.
        """
        return pulumi.get(self, "key_id")

    @key_id.setter
    def key_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "key_id", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> Optional[pulumi.Input[int]]:
        """
        The ID of the user to add the GPG key to. If this field is omitted, this resource manages a GPG key for the current user. Otherwise, this resource manages a GPG key for the specified user, and an admin token is required.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "user_id", value)


class UserGpgKey(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        The `UserGpgKey` resource allows to manage the lifecycle of a GPG key assigned to the current user or a specific user.

        > Managing GPG keys for arbitrary users requires admin privileges.

        **Upstream API**: [GitLab REST API docs](https://docs.gitlab.com/ee/api/users.html#get-a-specific-gpg-key)

        ## Example Usage

        ```python
        import pulumi
        import pulumi_gitlab as gitlab

        example_user = gitlab.get_user(username="example-user")
        # Manages a GPG key for the specified user. An admin token is required if `user_id` is specified.
        example_user_gpg_key = gitlab.UserGpgKey("exampleUserGpgKey",
            user_id=example_user.id,
            key=\"\"\"-----BEGIN PGP PUBLIC KEY BLOCK-----
        ...
        -----END PGP PUBLIC KEY BLOCK-----\"\"\")
        # Manages a GPG key for the current user
        example_user_user_gpg_key = gitlab.UserGpgKey("exampleUserUserGpgKey", key=\"\"\"-----BEGIN PGP PUBLIC KEY BLOCK-----
        ...
        -----END PGP PUBLIC KEY BLOCK-----\"\"\")
        ```

        ## Import

        You can import a GPG key for a specific user using an id made up of `{user-id}:{key}`, e.g.

        ```sh
         $ pulumi import gitlab:index/userGpgKey:UserGpgKey example 42:1
        ```

         Alternatively, you can import a GPG key for the current user using an id made up of `{key}`, e.g.

        ```sh
         $ pulumi import gitlab:index/userGpgKey:UserGpgKey example_user 1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] key: The armored GPG public key.
        :param pulumi.Input[int] user_id: The ID of the user to add the GPG key to. If this field is omitted, this resource manages a GPG key for the current user. Otherwise, this resource manages a GPG key for the specified user, and an admin token is required.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserGpgKeyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The `UserGpgKey` resource allows to manage the lifecycle of a GPG key assigned to the current user or a specific user.

        > Managing GPG keys for arbitrary users requires admin privileges.

        **Upstream API**: [GitLab REST API docs](https://docs.gitlab.com/ee/api/users.html#get-a-specific-gpg-key)

        ## Example Usage

        ```python
        import pulumi
        import pulumi_gitlab as gitlab

        example_user = gitlab.get_user(username="example-user")
        # Manages a GPG key for the specified user. An admin token is required if `user_id` is specified.
        example_user_gpg_key = gitlab.UserGpgKey("exampleUserGpgKey",
            user_id=example_user.id,
            key=\"\"\"-----BEGIN PGP PUBLIC KEY BLOCK-----
        ...
        -----END PGP PUBLIC KEY BLOCK-----\"\"\")
        # Manages a GPG key for the current user
        example_user_user_gpg_key = gitlab.UserGpgKey("exampleUserUserGpgKey", key=\"\"\"-----BEGIN PGP PUBLIC KEY BLOCK-----
        ...
        -----END PGP PUBLIC KEY BLOCK-----\"\"\")
        ```

        ## Import

        You can import a GPG key for a specific user using an id made up of `{user-id}:{key}`, e.g.

        ```sh
         $ pulumi import gitlab:index/userGpgKey:UserGpgKey example 42:1
        ```

         Alternatively, you can import a GPG key for the current user using an id made up of `{key}`, e.g.

        ```sh
         $ pulumi import gitlab:index/userGpgKey:UserGpgKey example_user 1
        ```

        :param str resource_name: The name of the resource.
        :param UserGpgKeyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserGpgKeyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserGpgKeyArgs.__new__(UserGpgKeyArgs)

            if key is None and not opts.urn:
                raise TypeError("Missing required property 'key'")
            __props__.__dict__["key"] = key
            __props__.__dict__["user_id"] = user_id
            __props__.__dict__["created_at"] = None
            __props__.__dict__["key_id"] = None
        super(UserGpgKey, __self__).__init__(
            'gitlab:index/userGpgKey:UserGpgKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            created_at: Optional[pulumi.Input[str]] = None,
            key: Optional[pulumi.Input[str]] = None,
            key_id: Optional[pulumi.Input[int]] = None,
            user_id: Optional[pulumi.Input[int]] = None) -> 'UserGpgKey':
        """
        Get an existing UserGpgKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] created_at: The time when this key was created in GitLab.
        :param pulumi.Input[str] key: The armored GPG public key.
        :param pulumi.Input[int] key_id: The ID of the GPG key.
        :param pulumi.Input[int] user_id: The ID of the user to add the GPG key to. If this field is omitted, this resource manages a GPG key for the current user. Otherwise, this resource manages a GPG key for the specified user, and an admin token is required.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserGpgKeyState.__new__(_UserGpgKeyState)

        __props__.__dict__["created_at"] = created_at
        __props__.__dict__["key"] = key
        __props__.__dict__["key_id"] = key_id
        __props__.__dict__["user_id"] = user_id
        return UserGpgKey(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        The time when this key was created in GitLab.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def key(self) -> pulumi.Output[str]:
        """
        The armored GPG public key.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> pulumi.Output[int]:
        """
        The ID of the GPG key.
        """
        return pulumi.get(self, "key_id")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Output[Optional[int]]:
        """
        The ID of the user to add the GPG key to. If this field is omitted, this resource manages a GPG key for the current user. Otherwise, this resource manages a GPG key for the specified user, and an admin token is required.
        """
        return pulumi.get(self, "user_id")

