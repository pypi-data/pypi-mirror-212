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


class ApiComponentPolicyViolationListDTOV2(object):
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
    swagger_types = {"policy_violations": "list[ApiPolicyViolationDTOV2]"}

    attribute_map = {"policy_violations": "policyViolations"}

    def __init__(self, policy_violations=None):  # noqa: E501
        """ApiComponentPolicyViolationListDTOV2 - a model defined in Swagger"""  # noqa: E501
        self._policy_violations = None
        self.discriminator = None
        if policy_violations is not None:
            self.policy_violations = policy_violations

    @property
    def policy_violations(self):
        """Gets the policy_violations of this ApiComponentPolicyViolationListDTOV2.  # noqa: E501


        :return: The policy_violations of this ApiComponentPolicyViolationListDTOV2.  # noqa: E501
        :rtype: list[ApiPolicyViolationDTOV2]
        """
        return self._policy_violations

    @policy_violations.setter
    def policy_violations(self, policy_violations):
        """Sets the policy_violations of this ApiComponentPolicyViolationListDTOV2.


        :param policy_violations: The policy_violations of this ApiComponentPolicyViolationListDTOV2.  # noqa: E501
        :type: list[ApiPolicyViolationDTOV2]
        """

        self._policy_violations = policy_violations

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
        if issubclass(ApiComponentPolicyViolationListDTOV2, dict):
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
        if not isinstance(other, ApiComponentPolicyViolationListDTOV2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
