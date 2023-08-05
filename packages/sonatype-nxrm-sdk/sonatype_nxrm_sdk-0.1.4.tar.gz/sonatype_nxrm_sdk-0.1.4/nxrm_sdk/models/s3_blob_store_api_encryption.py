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


class S3BlobStoreApiEncryption(object):
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
    swagger_types = {"encryption_type": "str", "encryption_key": "str"}

    attribute_map = {
        "encryption_type": "encryptionType",
        "encryption_key": "encryptionKey",
    }

    def __init__(self, encryption_type=None, encryption_key=None):  # noqa: E501
        """S3BlobStoreApiEncryption - a model defined in Swagger"""  # noqa: E501
        self._encryption_type = None
        self._encryption_key = None
        self.discriminator = None
        if encryption_type is not None:
            self.encryption_type = encryption_type
        if encryption_key is not None:
            self.encryption_key = encryption_key

    @property
    def encryption_type(self):
        """Gets the encryption_type of this S3BlobStoreApiEncryption.  # noqa: E501

        The type of S3 server side encryption to use.  # noqa: E501

        :return: The encryption_type of this S3BlobStoreApiEncryption.  # noqa: E501
        :rtype: str
        """
        return self._encryption_type

    @encryption_type.setter
    def encryption_type(self, encryption_type):
        """Sets the encryption_type of this S3BlobStoreApiEncryption.

        The type of S3 server side encryption to use.  # noqa: E501

        :param encryption_type: The encryption_type of this S3BlobStoreApiEncryption.  # noqa: E501
        :type: str
        """
        allowed_values = ["s3ManagedEncryption", "kmsManagedEncryption"]  # noqa: E501
        if encryption_type not in allowed_values:
            raise ValueError(
                "Invalid value for `encryption_type` ({0}), must be one of {1}".format(  # noqa: E501
                    encryption_type, allowed_values
                )
            )

        self._encryption_type = encryption_type

    @property
    def encryption_key(self):
        """Gets the encryption_key of this S3BlobStoreApiEncryption.  # noqa: E501

        The encryption key.  # noqa: E501

        :return: The encryption_key of this S3BlobStoreApiEncryption.  # noqa: E501
        :rtype: str
        """
        return self._encryption_key

    @encryption_key.setter
    def encryption_key(self, encryption_key):
        """Sets the encryption_key of this S3BlobStoreApiEncryption.

        The encryption key.  # noqa: E501

        :param encryption_key: The encryption_key of this S3BlobStoreApiEncryption.  # noqa: E501
        :type: str
        """

        self._encryption_key = encryption_key

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
        if issubclass(S3BlobStoreApiEncryption, dict):
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
        if not isinstance(other, S3BlobStoreApiEncryption):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
