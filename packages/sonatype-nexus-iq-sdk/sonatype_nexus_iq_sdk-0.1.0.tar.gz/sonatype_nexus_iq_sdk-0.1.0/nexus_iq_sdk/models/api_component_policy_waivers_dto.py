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


class ApiComponentPolicyWaiversDTO(object):
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
    swagger_types = {"component_policy_waivers": "list[ApiPolicyWaiverDTO]"}

    attribute_map = {"component_policy_waivers": "componentPolicyWaivers"}

    def __init__(self, component_policy_waivers=None):  # noqa: E501
        """ApiComponentPolicyWaiversDTO - a model defined in Swagger"""  # noqa: E501
        self._component_policy_waivers = None
        self.discriminator = None
        if component_policy_waivers is not None:
            self.component_policy_waivers = component_policy_waivers

    @property
    def component_policy_waivers(self):
        """Gets the component_policy_waivers of this ApiComponentPolicyWaiversDTO.  # noqa: E501


        :return: The component_policy_waivers of this ApiComponentPolicyWaiversDTO.  # noqa: E501
        :rtype: list[ApiPolicyWaiverDTO]
        """
        return self._component_policy_waivers

    @component_policy_waivers.setter
    def component_policy_waivers(self, component_policy_waivers):
        """Sets the component_policy_waivers of this ApiComponentPolicyWaiversDTO.


        :param component_policy_waivers: The component_policy_waivers of this ApiComponentPolicyWaiversDTO.  # noqa: E501
        :type: list[ApiPolicyWaiverDTO]
        """

        self._component_policy_waivers = component_policy_waivers

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
        if issubclass(ApiComponentPolicyWaiversDTO, dict):
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
        if not isinstance(other, ApiComponentPolicyWaiversDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
