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


class ApiFirewallReleaseQuarantineConfigDTO(object):
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
        "id": "str",
        "name": "str",
        "auto_release_quarantine_enabled": "bool",
    }

    attribute_map = {
        "id": "id",
        "name": "name",
        "auto_release_quarantine_enabled": "autoReleaseQuarantineEnabled",
    }

    def __init__(
        self, id=None, name=None, auto_release_quarantine_enabled=None
    ):  # noqa: E501
        """ApiFirewallReleaseQuarantineConfigDTO - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._name = None
        self._auto_release_quarantine_enabled = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if auto_release_quarantine_enabled is not None:
            self.auto_release_quarantine_enabled = auto_release_quarantine_enabled

    @property
    def id(self):
        """Gets the id of this ApiFirewallReleaseQuarantineConfigDTO.  # noqa: E501


        :return: The id of this ApiFirewallReleaseQuarantineConfigDTO.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ApiFirewallReleaseQuarantineConfigDTO.


        :param id: The id of this ApiFirewallReleaseQuarantineConfigDTO.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this ApiFirewallReleaseQuarantineConfigDTO.  # noqa: E501


        :return: The name of this ApiFirewallReleaseQuarantineConfigDTO.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ApiFirewallReleaseQuarantineConfigDTO.


        :param name: The name of this ApiFirewallReleaseQuarantineConfigDTO.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def auto_release_quarantine_enabled(self):
        """Gets the auto_release_quarantine_enabled of this ApiFirewallReleaseQuarantineConfigDTO.  # noqa: E501


        :return: The auto_release_quarantine_enabled of this ApiFirewallReleaseQuarantineConfigDTO.  # noqa: E501
        :rtype: bool
        """
        return self._auto_release_quarantine_enabled

    @auto_release_quarantine_enabled.setter
    def auto_release_quarantine_enabled(self, auto_release_quarantine_enabled):
        """Sets the auto_release_quarantine_enabled of this ApiFirewallReleaseQuarantineConfigDTO.


        :param auto_release_quarantine_enabled: The auto_release_quarantine_enabled of this ApiFirewallReleaseQuarantineConfigDTO.  # noqa: E501
        :type: bool
        """

        self._auto_release_quarantine_enabled = auto_release_quarantine_enabled

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
        if issubclass(ApiFirewallReleaseQuarantineConfigDTO, dict):
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
        if not isinstance(other, ApiFirewallReleaseQuarantineConfigDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
