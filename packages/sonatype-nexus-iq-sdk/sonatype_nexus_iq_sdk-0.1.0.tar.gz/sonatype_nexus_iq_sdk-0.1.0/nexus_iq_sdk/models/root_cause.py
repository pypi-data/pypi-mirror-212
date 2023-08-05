# coding: utf-8

"""
    Sonatype Nexus IQ Server

    This documents the available APIs into [Sonatype Nexus IQ Server](https://www.sonatype.com/products/open-source-security-dependency-management) (also knwon as Nexus Lifecycle).   # noqa: E501

    OpenAPI spec version: 156
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class RootCause(object):
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
    swagger_types = {"list_of_paths": "list[str]", "version_range": "str"}

    attribute_map = {"list_of_paths": "listOfPaths", "version_range": "versionRange"}

    def __init__(self, list_of_paths=None, version_range=None):  # noqa: E501
        """RootCause - a model defined in Swagger"""  # noqa: E501
        self._list_of_paths = None
        self._version_range = None
        self.discriminator = None
        if list_of_paths is not None:
            self.list_of_paths = list_of_paths
        if version_range is not None:
            self.version_range = version_range

    @property
    def list_of_paths(self):
        """Gets the list_of_paths of this RootCause.  # noqa: E501


        :return: The list_of_paths of this RootCause.  # noqa: E501
        :rtype: list[str]
        """
        return self._list_of_paths

    @list_of_paths.setter
    def list_of_paths(self, list_of_paths):
        """Sets the list_of_paths of this RootCause.


        :param list_of_paths: The list_of_paths of this RootCause.  # noqa: E501
        :type: list[str]
        """

        self._list_of_paths = list_of_paths

    @property
    def version_range(self):
        """Gets the version_range of this RootCause.  # noqa: E501


        :return: The version_range of this RootCause.  # noqa: E501
        :rtype: str
        """
        return self._version_range

    @version_range.setter
    def version_range(self, version_range):
        """Sets the version_range of this RootCause.


        :param version_range: The version_range of this RootCause.  # noqa: E501
        :type: str
        """

        self._version_range = version_range

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
        if issubclass(RootCause, dict):
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
        if not isinstance(other, RootCause):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
