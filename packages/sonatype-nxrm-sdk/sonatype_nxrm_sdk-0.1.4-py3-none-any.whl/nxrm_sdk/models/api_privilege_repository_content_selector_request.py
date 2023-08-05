# coding: utf-8

"""
    Nexus Repository Manager REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 3.42.0-01
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class ApiPrivilegeRepositoryContentSelectorRequest(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        "name": "str",
        "description": "str",
        "actions": "list[str]",
        "format": "str",
        "repository": "str",
        "content_selector": "str",
    }

    attribute_map = {
        "name": "name",
        "description": "description",
        "actions": "actions",
        "format": "format",
        "repository": "repository",
        "content_selector": "contentSelector",
    }

    def __init__(
        self,
        name=None,
        description=None,
        actions=None,
        format=None,
        repository=None,
        content_selector=None,
    ):  # noqa: E501
        """ApiPrivilegeRepositoryContentSelectorRequest - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._description = None
        self._actions = None
        self._format = None
        self._repository = None
        self._content_selector = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if actions is not None:
            self.actions = actions
        if format is not None:
            self.format = format
        if repository is not None:
            self.repository = repository
        if content_selector is not None:
            self.content_selector = content_selector

    @property
    def name(self):
        """Gets the name of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501

        The name of the privilege.  This value cannot be changed.  # noqa: E501

        :return: The name of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ApiPrivilegeRepositoryContentSelectorRequest.

        The name of the privilege.  This value cannot be changed.  # noqa: E501

        :param name: The name of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """Gets the description of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501


        :return: The description of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ApiPrivilegeRepositoryContentSelectorRequest.


        :param description: The description of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def actions(self):
        """Gets the actions of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501

        A collection of actions to associate with the privilege, using BREAD syntax (browse,read,edit,add,delete,all) as well as 'run' for script privileges.  # noqa: E501

        :return: The actions of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """Sets the actions of this ApiPrivilegeRepositoryContentSelectorRequest.

        A collection of actions to associate with the privilege, using BREAD syntax (browse,read,edit,add,delete,all) as well as 'run' for script privileges.  # noqa: E501

        :param actions: The actions of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501
        :type: list[str]
        """
        allowed_values = [
            "READ",
            "BROWSE",
            "EDIT",
            "ADD",
            "DELETE",
            "RUN",
            "ASSOCIATE",
            "DISASSOCIATE",
            "ALL",
        ]  # noqa: E501
        if not set(actions).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `actions` [{0}], must be a subset of [{1}]".format(  # noqa: E501
                    ", ".join(
                        map(str, set(actions) - set(allowed_values))
                    ),  # noqa: E501
                    ", ".join(map(str, allowed_values)),
                )
            )

        self._actions = actions

    @property
    def format(self):
        """Gets the format of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501

        The repository format (i.e 'nuget', 'npm') this privilege will grant access to (or * for all).  # noqa: E501

        :return: The format of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501
        :rtype: str
        """
        return self._format

    @format.setter
    def format(self, format):
        """Sets the format of this ApiPrivilegeRepositoryContentSelectorRequest.

        The repository format (i.e 'nuget', 'npm') this privilege will grant access to (or * for all).  # noqa: E501

        :param format: The format of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501
        :type: str
        """

        self._format = format

    @property
    def repository(self):
        """Gets the repository of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501

        The name of the repository this privilege will grant access to (or * for all).  # noqa: E501

        :return: The repository of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501
        :rtype: str
        """
        return self._repository

    @repository.setter
    def repository(self, repository):
        """Sets the repository of this ApiPrivilegeRepositoryContentSelectorRequest.

        The name of the repository this privilege will grant access to (or * for all).  # noqa: E501

        :param repository: The repository of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501
        :type: str
        """

        self._repository = repository

    @property
    def content_selector(self):
        """Gets the content_selector of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501

        The name of a content selector that will be used to grant access to content via this privilege.  # noqa: E501

        :return: The content_selector of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501
        :rtype: str
        """
        return self._content_selector

    @content_selector.setter
    def content_selector(self, content_selector):
        """Sets the content_selector of this ApiPrivilegeRepositoryContentSelectorRequest.

        The name of a content selector that will be used to grant access to content via this privilege.  # noqa: E501

        :param content_selector: The content_selector of this ApiPrivilegeRepositoryContentSelectorRequest.  # noqa: E501
        :type: str
        """

        self._content_selector = content_selector

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(ApiPrivilegeRepositoryContentSelectorRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ApiPrivilegeRepositoryContentSelectorRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
