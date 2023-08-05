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


class HttpClientAttributes(object):
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
        "blocked": "bool",
        "auto_block": "bool",
        "connection": "HttpClientConnectionAttributes",
        "authentication": "HttpClientConnectionAuthenticationAttributes",
    }

    attribute_map = {
        "blocked": "blocked",
        "auto_block": "autoBlock",
        "connection": "connection",
        "authentication": "authentication",
    }

    def __init__(
        self, blocked=None, auto_block=None, connection=None, authentication=None
    ):  # noqa: E501
        """HttpClientAttributes - a model defined in Swagger"""  # noqa: E501
        self._blocked = None
        self._auto_block = None
        self._connection = None
        self._authentication = None
        self.discriminator = None
        self.blocked = blocked
        self.auto_block = auto_block
        if connection is not None:
            self.connection = connection
        if authentication is not None:
            self.authentication = authentication

    @property
    def blocked(self):
        """Gets the blocked of this HttpClientAttributes.  # noqa: E501

        Whether to block outbound connections on the repository  # noqa: E501

        :return: The blocked of this HttpClientAttributes.  # noqa: E501
        :rtype: bool
        """
        return self._blocked

    @blocked.setter
    def blocked(self, blocked):
        """Sets the blocked of this HttpClientAttributes.

        Whether to block outbound connections on the repository  # noqa: E501

        :param blocked: The blocked of this HttpClientAttributes.  # noqa: E501
        :type: bool
        """
        if blocked is None:
            raise ValueError(
                "Invalid value for `blocked`, must not be `None`"
            )  # noqa: E501

        self._blocked = blocked

    @property
    def auto_block(self):
        """Gets the auto_block of this HttpClientAttributes.  # noqa: E501

        Whether to auto-block outbound connections if remote peer is detected as unreachable/unresponsive  # noqa: E501

        :return: The auto_block of this HttpClientAttributes.  # noqa: E501
        :rtype: bool
        """
        return self._auto_block

    @auto_block.setter
    def auto_block(self, auto_block):
        """Sets the auto_block of this HttpClientAttributes.

        Whether to auto-block outbound connections if remote peer is detected as unreachable/unresponsive  # noqa: E501

        :param auto_block: The auto_block of this HttpClientAttributes.  # noqa: E501
        :type: bool
        """
        if auto_block is None:
            raise ValueError(
                "Invalid value for `auto_block`, must not be `None`"
            )  # noqa: E501

        self._auto_block = auto_block

    @property
    def connection(self):
        """Gets the connection of this HttpClientAttributes.  # noqa: E501


        :return: The connection of this HttpClientAttributes.  # noqa: E501
        :rtype: HttpClientConnectionAttributes
        """
        return self._connection

    @connection.setter
    def connection(self, connection):
        """Sets the connection of this HttpClientAttributes.


        :param connection: The connection of this HttpClientAttributes.  # noqa: E501
        :type: HttpClientConnectionAttributes
        """

        self._connection = connection

    @property
    def authentication(self):
        """Gets the authentication of this HttpClientAttributes.  # noqa: E501


        :return: The authentication of this HttpClientAttributes.  # noqa: E501
        :rtype: HttpClientConnectionAuthenticationAttributes
        """
        return self._authentication

    @authentication.setter
    def authentication(self, authentication):
        """Sets the authentication of this HttpClientAttributes.


        :param authentication: The authentication of this HttpClientAttributes.  # noqa: E501
        :type: HttpClientConnectionAuthenticationAttributes
        """

        self._authentication = authentication

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
        if issubclass(HttpClientAttributes, dict):
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
        if not isinstance(other, HttpClientAttributes):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
