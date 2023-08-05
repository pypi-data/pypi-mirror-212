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


class FileBlobStoreApiUpdateRequest(object):
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
    swagger_types = {"soft_quota": "BlobStoreApiSoftQuota", "path": "str"}

    attribute_map = {"soft_quota": "softQuota", "path": "path"}

    def __init__(self, soft_quota=None, path=None):  # noqa: E501
        """FileBlobStoreApiUpdateRequest - a model defined in Swagger"""  # noqa: E501
        self._soft_quota = None
        self._path = None
        self.discriminator = None
        if soft_quota is not None:
            self.soft_quota = soft_quota
        if path is not None:
            self.path = path

    @property
    def soft_quota(self):
        """Gets the soft_quota of this FileBlobStoreApiUpdateRequest.  # noqa: E501


        :return: The soft_quota of this FileBlobStoreApiUpdateRequest.  # noqa: E501
        :rtype: BlobStoreApiSoftQuota
        """
        return self._soft_quota

    @soft_quota.setter
    def soft_quota(self, soft_quota):
        """Sets the soft_quota of this FileBlobStoreApiUpdateRequest.


        :param soft_quota: The soft_quota of this FileBlobStoreApiUpdateRequest.  # noqa: E501
        :type: BlobStoreApiSoftQuota
        """

        self._soft_quota = soft_quota

    @property
    def path(self):
        """Gets the path of this FileBlobStoreApiUpdateRequest.  # noqa: E501

        The path to the blobstore contents. This can be an absolute path to anywhere on the system Nexus Repository Manager has access to or it can be a path relative to the sonatype-work directory.  # noqa: E501

        :return: The path of this FileBlobStoreApiUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this FileBlobStoreApiUpdateRequest.

        The path to the blobstore contents. This can be an absolute path to anywhere on the system Nexus Repository Manager has access to or it can be a path relative to the sonatype-work directory.  # noqa: E501

        :param path: The path of this FileBlobStoreApiUpdateRequest.  # noqa: E501
        :type: str
        """

        self._path = path

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
        if issubclass(FileBlobStoreApiUpdateRequest, dict):
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
        if not isinstance(other, FileBlobStoreApiUpdateRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
