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


class ApiEmailConfiguration(object):
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
        "enabled": "bool",
        "host": "str",
        "port": "int",
        "username": "str",
        "password": "str",
        "from_address": "str",
        "subject_prefix": "str",
        "start_tls_enabled": "bool",
        "start_tls_required": "bool",
        "ssl_on_connect_enabled": "bool",
        "ssl_server_identity_check_enabled": "bool",
        "nexus_trust_store_enabled": "bool",
    }

    attribute_map = {
        "enabled": "enabled",
        "host": "host",
        "port": "port",
        "username": "username",
        "password": "password",
        "from_address": "fromAddress",
        "subject_prefix": "subjectPrefix",
        "start_tls_enabled": "startTlsEnabled",
        "start_tls_required": "startTlsRequired",
        "ssl_on_connect_enabled": "sslOnConnectEnabled",
        "ssl_server_identity_check_enabled": "sslServerIdentityCheckEnabled",
        "nexus_trust_store_enabled": "nexusTrustStoreEnabled",
    }

    def __init__(
        self,
        enabled=None,
        host=None,
        port=None,
        username=None,
        password=None,
        from_address=None,
        subject_prefix=None,
        start_tls_enabled=None,
        start_tls_required=None,
        ssl_on_connect_enabled=None,
        ssl_server_identity_check_enabled=None,
        nexus_trust_store_enabled=None,
    ):  # noqa: E501
        """ApiEmailConfiguration - a model defined in Swagger"""  # noqa: E501
        self._enabled = None
        self._host = None
        self._port = None
        self._username = None
        self._password = None
        self._from_address = None
        self._subject_prefix = None
        self._start_tls_enabled = None
        self._start_tls_required = None
        self._ssl_on_connect_enabled = None
        self._ssl_server_identity_check_enabled = None
        self._nexus_trust_store_enabled = None
        self.discriminator = None
        if enabled is not None:
            self.enabled = enabled
        if host is not None:
            self.host = host
        self.port = port
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password
        if from_address is not None:
            self.from_address = from_address
        if subject_prefix is not None:
            self.subject_prefix = subject_prefix
        if start_tls_enabled is not None:
            self.start_tls_enabled = start_tls_enabled
        if start_tls_required is not None:
            self.start_tls_required = start_tls_required
        if ssl_on_connect_enabled is not None:
            self.ssl_on_connect_enabled = ssl_on_connect_enabled
        if ssl_server_identity_check_enabled is not None:
            self.ssl_server_identity_check_enabled = ssl_server_identity_check_enabled
        if nexus_trust_store_enabled is not None:
            self.nexus_trust_store_enabled = nexus_trust_store_enabled

    @property
    def enabled(self):
        """Gets the enabled of this ApiEmailConfiguration.  # noqa: E501


        :return: The enabled of this ApiEmailConfiguration.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this ApiEmailConfiguration.


        :param enabled: The enabled of this ApiEmailConfiguration.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def host(self):
        """Gets the host of this ApiEmailConfiguration.  # noqa: E501


        :return: The host of this ApiEmailConfiguration.  # noqa: E501
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """Sets the host of this ApiEmailConfiguration.


        :param host: The host of this ApiEmailConfiguration.  # noqa: E501
        :type: str
        """

        self._host = host

    @property
    def port(self):
        """Gets the port of this ApiEmailConfiguration.  # noqa: E501


        :return: The port of this ApiEmailConfiguration.  # noqa: E501
        :rtype: int
        """
        return self._port

    @port.setter
    def port(self, port):
        """Sets the port of this ApiEmailConfiguration.


        :param port: The port of this ApiEmailConfiguration.  # noqa: E501
        :type: int
        """
        if port is None:
            raise ValueError(
                "Invalid value for `port`, must not be `None`"
            )  # noqa: E501

        self._port = port

    @property
    def username(self):
        """Gets the username of this ApiEmailConfiguration.  # noqa: E501


        :return: The username of this ApiEmailConfiguration.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this ApiEmailConfiguration.


        :param username: The username of this ApiEmailConfiguration.  # noqa: E501
        :type: str
        """

        self._username = username

    @property
    def password(self):
        """Gets the password of this ApiEmailConfiguration.  # noqa: E501


        :return: The password of this ApiEmailConfiguration.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this ApiEmailConfiguration.


        :param password: The password of this ApiEmailConfiguration.  # noqa: E501
        :type: str
        """

        self._password = password

    @property
    def from_address(self):
        """Gets the from_address of this ApiEmailConfiguration.  # noqa: E501


        :return: The from_address of this ApiEmailConfiguration.  # noqa: E501
        :rtype: str
        """
        return self._from_address

    @from_address.setter
    def from_address(self, from_address):
        """Sets the from_address of this ApiEmailConfiguration.


        :param from_address: The from_address of this ApiEmailConfiguration.  # noqa: E501
        :type: str
        """

        self._from_address = from_address

    @property
    def subject_prefix(self):
        """Gets the subject_prefix of this ApiEmailConfiguration.  # noqa: E501

        A prefix to add to all email subjects to aid in identifying automated emails  # noqa: E501

        :return: The subject_prefix of this ApiEmailConfiguration.  # noqa: E501
        :rtype: str
        """
        return self._subject_prefix

    @subject_prefix.setter
    def subject_prefix(self, subject_prefix):
        """Sets the subject_prefix of this ApiEmailConfiguration.

        A prefix to add to all email subjects to aid in identifying automated emails  # noqa: E501

        :param subject_prefix: The subject_prefix of this ApiEmailConfiguration.  # noqa: E501
        :type: str
        """

        self._subject_prefix = subject_prefix

    @property
    def start_tls_enabled(self):
        """Gets the start_tls_enabled of this ApiEmailConfiguration.  # noqa: E501

        Enable STARTTLS Support for Insecure Connections  # noqa: E501

        :return: The start_tls_enabled of this ApiEmailConfiguration.  # noqa: E501
        :rtype: bool
        """
        return self._start_tls_enabled

    @start_tls_enabled.setter
    def start_tls_enabled(self, start_tls_enabled):
        """Sets the start_tls_enabled of this ApiEmailConfiguration.

        Enable STARTTLS Support for Insecure Connections  # noqa: E501

        :param start_tls_enabled: The start_tls_enabled of this ApiEmailConfiguration.  # noqa: E501
        :type: bool
        """

        self._start_tls_enabled = start_tls_enabled

    @property
    def start_tls_required(self):
        """Gets the start_tls_required of this ApiEmailConfiguration.  # noqa: E501

        Require STARTTLS Support  # noqa: E501

        :return: The start_tls_required of this ApiEmailConfiguration.  # noqa: E501
        :rtype: bool
        """
        return self._start_tls_required

    @start_tls_required.setter
    def start_tls_required(self, start_tls_required):
        """Sets the start_tls_required of this ApiEmailConfiguration.

        Require STARTTLS Support  # noqa: E501

        :param start_tls_required: The start_tls_required of this ApiEmailConfiguration.  # noqa: E501
        :type: bool
        """

        self._start_tls_required = start_tls_required

    @property
    def ssl_on_connect_enabled(self):
        """Gets the ssl_on_connect_enabled of this ApiEmailConfiguration.  # noqa: E501

        Enable SSL/TLS Encryption upon Connection  # noqa: E501

        :return: The ssl_on_connect_enabled of this ApiEmailConfiguration.  # noqa: E501
        :rtype: bool
        """
        return self._ssl_on_connect_enabled

    @ssl_on_connect_enabled.setter
    def ssl_on_connect_enabled(self, ssl_on_connect_enabled):
        """Sets the ssl_on_connect_enabled of this ApiEmailConfiguration.

        Enable SSL/TLS Encryption upon Connection  # noqa: E501

        :param ssl_on_connect_enabled: The ssl_on_connect_enabled of this ApiEmailConfiguration.  # noqa: E501
        :type: bool
        """

        self._ssl_on_connect_enabled = ssl_on_connect_enabled

    @property
    def ssl_server_identity_check_enabled(self):
        """Gets the ssl_server_identity_check_enabled of this ApiEmailConfiguration.  # noqa: E501

        Verify the server certificate when using TLS or SSL  # noqa: E501

        :return: The ssl_server_identity_check_enabled of this ApiEmailConfiguration.  # noqa: E501
        :rtype: bool
        """
        return self._ssl_server_identity_check_enabled

    @ssl_server_identity_check_enabled.setter
    def ssl_server_identity_check_enabled(self, ssl_server_identity_check_enabled):
        """Sets the ssl_server_identity_check_enabled of this ApiEmailConfiguration.

        Verify the server certificate when using TLS or SSL  # noqa: E501

        :param ssl_server_identity_check_enabled: The ssl_server_identity_check_enabled of this ApiEmailConfiguration.  # noqa: E501
        :type: bool
        """

        self._ssl_server_identity_check_enabled = ssl_server_identity_check_enabled

    @property
    def nexus_trust_store_enabled(self):
        """Gets the nexus_trust_store_enabled of this ApiEmailConfiguration.  # noqa: E501

        Use the Nexus Repository Manager's certificate truststore  # noqa: E501

        :return: The nexus_trust_store_enabled of this ApiEmailConfiguration.  # noqa: E501
        :rtype: bool
        """
        return self._nexus_trust_store_enabled

    @nexus_trust_store_enabled.setter
    def nexus_trust_store_enabled(self, nexus_trust_store_enabled):
        """Sets the nexus_trust_store_enabled of this ApiEmailConfiguration.

        Use the Nexus Repository Manager's certificate truststore  # noqa: E501

        :param nexus_trust_store_enabled: The nexus_trust_store_enabled of this ApiEmailConfiguration.  # noqa: E501
        :type: bool
        """

        self._nexus_trust_store_enabled = nexus_trust_store_enabled

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
        if issubclass(ApiEmailConfiguration, dict):
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
        if not isinstance(other, ApiEmailConfiguration):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
