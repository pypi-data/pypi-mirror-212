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


class DockerHostedStorageAttributes(object):
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
        "blob_store_name": "str",
        "strict_content_type_validation": "bool",
        "write_policy": "str",
        "latest_policy": "bool",
    }

    attribute_map = {
        "blob_store_name": "blobStoreName",
        "strict_content_type_validation": "strictContentTypeValidation",
        "write_policy": "writePolicy",
        "latest_policy": "latestPolicy",
    }

    def __init__(
        self,
        blob_store_name=None,
        strict_content_type_validation=None,
        write_policy=None,
        latest_policy=None,
    ):  # noqa: E501
        """DockerHostedStorageAttributes - a model defined in Swagger"""  # noqa: E501
        self._blob_store_name = None
        self._strict_content_type_validation = None
        self._write_policy = None
        self._latest_policy = None
        self.discriminator = None
        if blob_store_name is not None:
            self.blob_store_name = blob_store_name
        self.strict_content_type_validation = strict_content_type_validation
        self.write_policy = write_policy
        if latest_policy is not None:
            self.latest_policy = latest_policy

    @property
    def blob_store_name(self):
        """Gets the blob_store_name of this DockerHostedStorageAttributes.  # noqa: E501

        Blob store used to store repository contents  # noqa: E501

        :return: The blob_store_name of this DockerHostedStorageAttributes.  # noqa: E501
        :rtype: str
        """
        return self._blob_store_name

    @blob_store_name.setter
    def blob_store_name(self, blob_store_name):
        """Sets the blob_store_name of this DockerHostedStorageAttributes.

        Blob store used to store repository contents  # noqa: E501

        :param blob_store_name: The blob_store_name of this DockerHostedStorageAttributes.  # noqa: E501
        :type: str
        """

        self._blob_store_name = blob_store_name

    @property
    def strict_content_type_validation(self):
        """Gets the strict_content_type_validation of this DockerHostedStorageAttributes.  # noqa: E501

        Whether to validate uploaded content's MIME type appropriate for the repository format  # noqa: E501

        :return: The strict_content_type_validation of this DockerHostedStorageAttributes.  # noqa: E501
        :rtype: bool
        """
        return self._strict_content_type_validation

    @strict_content_type_validation.setter
    def strict_content_type_validation(self, strict_content_type_validation):
        """Sets the strict_content_type_validation of this DockerHostedStorageAttributes.

        Whether to validate uploaded content's MIME type appropriate for the repository format  # noqa: E501

        :param strict_content_type_validation: The strict_content_type_validation of this DockerHostedStorageAttributes.  # noqa: E501
        :type: bool
        """
        if strict_content_type_validation is None:
            raise ValueError(
                "Invalid value for `strict_content_type_validation`, must not be `None`"
            )  # noqa: E501

        self._strict_content_type_validation = strict_content_type_validation

    @property
    def write_policy(self):
        """Gets the write_policy of this DockerHostedStorageAttributes.  # noqa: E501

        Controls if deployments of and updates to assets are allowed  # noqa: E501

        :return: The write_policy of this DockerHostedStorageAttributes.  # noqa: E501
        :rtype: str
        """
        return self._write_policy

    @write_policy.setter
    def write_policy(self, write_policy):
        """Sets the write_policy of this DockerHostedStorageAttributes.

        Controls if deployments of and updates to assets are allowed  # noqa: E501

        :param write_policy: The write_policy of this DockerHostedStorageAttributes.  # noqa: E501
        :type: str
        """
        if write_policy is None:
            raise ValueError(
                "Invalid value for `write_policy`, must not be `None`"
            )  # noqa: E501
        allowed_values = ["allow", "allow_once", "deny"]  # noqa: E501
        if write_policy not in allowed_values:
            raise ValueError(
                "Invalid value for `write_policy` ({0}), must be one of {1}".format(  # noqa: E501
                    write_policy, allowed_values
                )
            )

        self._write_policy = write_policy

    @property
    def latest_policy(self):
        """Gets the latest_policy of this DockerHostedStorageAttributes.  # noqa: E501

        Whether to allow redeploying the 'latest' tag but defer to the Deployment Policy for all other tags  # noqa: E501

        :return: The latest_policy of this DockerHostedStorageAttributes.  # noqa: E501
        :rtype: bool
        """
        return self._latest_policy

    @latest_policy.setter
    def latest_policy(self, latest_policy):
        """Sets the latest_policy of this DockerHostedStorageAttributes.

        Whether to allow redeploying the 'latest' tag but defer to the Deployment Policy for all other tags  # noqa: E501

        :param latest_policy: The latest_policy of this DockerHostedStorageAttributes.  # noqa: E501
        :type: bool
        """

        self._latest_policy = latest_policy

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
        if issubclass(DockerHostedStorageAttributes, dict):
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
        if not isinstance(other, DockerHostedStorageAttributes):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
