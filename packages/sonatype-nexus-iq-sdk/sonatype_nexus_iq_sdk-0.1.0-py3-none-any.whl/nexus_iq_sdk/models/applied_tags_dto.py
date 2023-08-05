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


class AppliedTagsDTO(object):
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
    swagger_types = {"application_tags_by_owner": "list[ApplicationTagsByOwnerDTO]"}

    attribute_map = {"application_tags_by_owner": "applicationTagsByOwner"}

    def __init__(self, application_tags_by_owner=None):  # noqa: E501
        """AppliedTagsDTO - a model defined in Swagger"""  # noqa: E501
        self._application_tags_by_owner = None
        self.discriminator = None
        if application_tags_by_owner is not None:
            self.application_tags_by_owner = application_tags_by_owner

    @property
    def application_tags_by_owner(self):
        """Gets the application_tags_by_owner of this AppliedTagsDTO.  # noqa: E501


        :return: The application_tags_by_owner of this AppliedTagsDTO.  # noqa: E501
        :rtype: list[ApplicationTagsByOwnerDTO]
        """
        return self._application_tags_by_owner

    @application_tags_by_owner.setter
    def application_tags_by_owner(self, application_tags_by_owner):
        """Sets the application_tags_by_owner of this AppliedTagsDTO.


        :param application_tags_by_owner: The application_tags_by_owner of this AppliedTagsDTO.  # noqa: E501
        :type: list[ApplicationTagsByOwnerDTO]
        """

        self._application_tags_by_owner = application_tags_by_owner

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
        if issubclass(AppliedTagsDTO, dict):
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
        if not isinstance(other, AppliedTagsDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
