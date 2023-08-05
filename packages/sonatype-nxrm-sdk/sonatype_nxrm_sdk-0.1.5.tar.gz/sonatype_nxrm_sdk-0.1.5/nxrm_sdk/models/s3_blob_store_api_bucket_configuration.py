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


class S3BlobStoreApiBucketConfiguration(object):
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
        "bucket": "S3BlobStoreApiBucket",
        "encryption": "S3BlobStoreApiEncryption",
        "bucket_security": "S3BlobStoreApiBucketSecurity",
        "advanced_bucket_connection": "S3BlobStoreApiAdvancedBucketConnection",
    }

    attribute_map = {
        "bucket": "bucket",
        "encryption": "encryption",
        "bucket_security": "bucketSecurity",
        "advanced_bucket_connection": "advancedBucketConnection",
    }

    def __init__(
        self,
        bucket=None,
        encryption=None,
        bucket_security=None,
        advanced_bucket_connection=None,
    ):  # noqa: E501
        """S3BlobStoreApiBucketConfiguration - a model defined in Swagger"""  # noqa: E501
        self._bucket = None
        self._encryption = None
        self._bucket_security = None
        self._advanced_bucket_connection = None
        self.discriminator = None
        self.bucket = bucket
        if encryption is not None:
            self.encryption = encryption
        if bucket_security is not None:
            self.bucket_security = bucket_security
        if advanced_bucket_connection is not None:
            self.advanced_bucket_connection = advanced_bucket_connection

    @property
    def bucket(self):
        """Gets the bucket of this S3BlobStoreApiBucketConfiguration.  # noqa: E501


        :return: The bucket of this S3BlobStoreApiBucketConfiguration.  # noqa: E501
        :rtype: S3BlobStoreApiBucket
        """
        return self._bucket

    @bucket.setter
    def bucket(self, bucket):
        """Sets the bucket of this S3BlobStoreApiBucketConfiguration.


        :param bucket: The bucket of this S3BlobStoreApiBucketConfiguration.  # noqa: E501
        :type: S3BlobStoreApiBucket
        """
        if bucket is None:
            raise ValueError(
                "Invalid value for `bucket`, must not be `None`"
            )  # noqa: E501

        self._bucket = bucket

    @property
    def encryption(self):
        """Gets the encryption of this S3BlobStoreApiBucketConfiguration.  # noqa: E501


        :return: The encryption of this S3BlobStoreApiBucketConfiguration.  # noqa: E501
        :rtype: S3BlobStoreApiEncryption
        """
        return self._encryption

    @encryption.setter
    def encryption(self, encryption):
        """Sets the encryption of this S3BlobStoreApiBucketConfiguration.


        :param encryption: The encryption of this S3BlobStoreApiBucketConfiguration.  # noqa: E501
        :type: S3BlobStoreApiEncryption
        """

        self._encryption = encryption

    @property
    def bucket_security(self):
        """Gets the bucket_security of this S3BlobStoreApiBucketConfiguration.  # noqa: E501


        :return: The bucket_security of this S3BlobStoreApiBucketConfiguration.  # noqa: E501
        :rtype: S3BlobStoreApiBucketSecurity
        """
        return self._bucket_security

    @bucket_security.setter
    def bucket_security(self, bucket_security):
        """Sets the bucket_security of this S3BlobStoreApiBucketConfiguration.


        :param bucket_security: The bucket_security of this S3BlobStoreApiBucketConfiguration.  # noqa: E501
        :type: S3BlobStoreApiBucketSecurity
        """

        self._bucket_security = bucket_security

    @property
    def advanced_bucket_connection(self):
        """Gets the advanced_bucket_connection of this S3BlobStoreApiBucketConfiguration.  # noqa: E501


        :return: The advanced_bucket_connection of this S3BlobStoreApiBucketConfiguration.  # noqa: E501
        :rtype: S3BlobStoreApiAdvancedBucketConnection
        """
        return self._advanced_bucket_connection

    @advanced_bucket_connection.setter
    def advanced_bucket_connection(self, advanced_bucket_connection):
        """Sets the advanced_bucket_connection of this S3BlobStoreApiBucketConfiguration.


        :param advanced_bucket_connection: The advanced_bucket_connection of this S3BlobStoreApiBucketConfiguration.  # noqa: E501
        :type: S3BlobStoreApiAdvancedBucketConnection
        """

        self._advanced_bucket_connection = advanced_bucket_connection

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
        if issubclass(S3BlobStoreApiBucketConfiguration, dict):
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
        if not isinstance(other, S3BlobStoreApiBucketConfiguration):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
