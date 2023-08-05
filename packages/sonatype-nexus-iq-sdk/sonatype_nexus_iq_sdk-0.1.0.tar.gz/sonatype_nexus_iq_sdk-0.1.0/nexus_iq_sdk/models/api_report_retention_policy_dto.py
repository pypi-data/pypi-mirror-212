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


class ApiReportRetentionPolicyDTO(object):
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
        "inherit_policy": "bool",
        "enable_purging": "bool",
        "max_count": "int",
        "max_age": "str",
    }

    attribute_map = {
        "inherit_policy": "inheritPolicy",
        "enable_purging": "enablePurging",
        "max_count": "maxCount",
        "max_age": "maxAge",
    }

    def __init__(
        self, inherit_policy=None, enable_purging=None, max_count=None, max_age=None
    ):  # noqa: E501
        """ApiReportRetentionPolicyDTO - a model defined in Swagger"""  # noqa: E501
        self._inherit_policy = None
        self._enable_purging = None
        self._max_count = None
        self._max_age = None
        self.discriminator = None
        if inherit_policy is not None:
            self.inherit_policy = inherit_policy
        if enable_purging is not None:
            self.enable_purging = enable_purging
        if max_count is not None:
            self.max_count = max_count
        if max_age is not None:
            self.max_age = max_age

    @property
    def inherit_policy(self):
        """Gets the inherit_policy of this ApiReportRetentionPolicyDTO.  # noqa: E501


        :return: The inherit_policy of this ApiReportRetentionPolicyDTO.  # noqa: E501
        :rtype: bool
        """
        return self._inherit_policy

    @inherit_policy.setter
    def inherit_policy(self, inherit_policy):
        """Sets the inherit_policy of this ApiReportRetentionPolicyDTO.


        :param inherit_policy: The inherit_policy of this ApiReportRetentionPolicyDTO.  # noqa: E501
        :type: bool
        """

        self._inherit_policy = inherit_policy

    @property
    def enable_purging(self):
        """Gets the enable_purging of this ApiReportRetentionPolicyDTO.  # noqa: E501


        :return: The enable_purging of this ApiReportRetentionPolicyDTO.  # noqa: E501
        :rtype: bool
        """
        return self._enable_purging

    @enable_purging.setter
    def enable_purging(self, enable_purging):
        """Sets the enable_purging of this ApiReportRetentionPolicyDTO.


        :param enable_purging: The enable_purging of this ApiReportRetentionPolicyDTO.  # noqa: E501
        :type: bool
        """

        self._enable_purging = enable_purging

    @property
    def max_count(self):
        """Gets the max_count of this ApiReportRetentionPolicyDTO.  # noqa: E501


        :return: The max_count of this ApiReportRetentionPolicyDTO.  # noqa: E501
        :rtype: int
        """
        return self._max_count

    @max_count.setter
    def max_count(self, max_count):
        """Sets the max_count of this ApiReportRetentionPolicyDTO.


        :param max_count: The max_count of this ApiReportRetentionPolicyDTO.  # noqa: E501
        :type: int
        """

        self._max_count = max_count

    @property
    def max_age(self):
        """Gets the max_age of this ApiReportRetentionPolicyDTO.  # noqa: E501


        :return: The max_age of this ApiReportRetentionPolicyDTO.  # noqa: E501
        :rtype: str
        """
        return self._max_age

    @max_age.setter
    def max_age(self, max_age):
        """Sets the max_age of this ApiReportRetentionPolicyDTO.


        :param max_age: The max_age of this ApiReportRetentionPolicyDTO.  # noqa: E501
        :type: str
        """

        self._max_age = max_age

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
        if issubclass(ApiReportRetentionPolicyDTO, dict):
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
        if not isinstance(other, ApiReportRetentionPolicyDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
