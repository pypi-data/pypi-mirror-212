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


class ApiOwnerDTO(object):
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
        "owner_public_id": "str",
        "owner_id": "str",
        "owner_name": "str",
        "owner_type": "str",
    }

    attribute_map = {
        "owner_public_id": "ownerPublicId",
        "owner_id": "ownerId",
        "owner_name": "ownerName",
        "owner_type": "ownerType",
    }

    def __init__(
        self, owner_public_id=None, owner_id=None, owner_name=None, owner_type=None
    ):  # noqa: E501
        """ApiOwnerDTO - a model defined in Swagger"""  # noqa: E501
        self._owner_public_id = None
        self._owner_id = None
        self._owner_name = None
        self._owner_type = None
        self.discriminator = None
        if owner_public_id is not None:
            self.owner_public_id = owner_public_id
        if owner_id is not None:
            self.owner_id = owner_id
        if owner_name is not None:
            self.owner_name = owner_name
        if owner_type is not None:
            self.owner_type = owner_type

    @property
    def owner_public_id(self):
        """Gets the owner_public_id of this ApiOwnerDTO.  # noqa: E501


        :return: The owner_public_id of this ApiOwnerDTO.  # noqa: E501
        :rtype: str
        """
        return self._owner_public_id

    @owner_public_id.setter
    def owner_public_id(self, owner_public_id):
        """Sets the owner_public_id of this ApiOwnerDTO.


        :param owner_public_id: The owner_public_id of this ApiOwnerDTO.  # noqa: E501
        :type: str
        """

        self._owner_public_id = owner_public_id

    @property
    def owner_id(self):
        """Gets the owner_id of this ApiOwnerDTO.  # noqa: E501


        :return: The owner_id of this ApiOwnerDTO.  # noqa: E501
        :rtype: str
        """
        return self._owner_id

    @owner_id.setter
    def owner_id(self, owner_id):
        """Sets the owner_id of this ApiOwnerDTO.


        :param owner_id: The owner_id of this ApiOwnerDTO.  # noqa: E501
        :type: str
        """

        self._owner_id = owner_id

    @property
    def owner_name(self):
        """Gets the owner_name of this ApiOwnerDTO.  # noqa: E501


        :return: The owner_name of this ApiOwnerDTO.  # noqa: E501
        :rtype: str
        """
        return self._owner_name

    @owner_name.setter
    def owner_name(self, owner_name):
        """Sets the owner_name of this ApiOwnerDTO.


        :param owner_name: The owner_name of this ApiOwnerDTO.  # noqa: E501
        :type: str
        """

        self._owner_name = owner_name

    @property
    def owner_type(self):
        """Gets the owner_type of this ApiOwnerDTO.  # noqa: E501


        :return: The owner_type of this ApiOwnerDTO.  # noqa: E501
        :rtype: str
        """
        return self._owner_type

    @owner_type.setter
    def owner_type(self, owner_type):
        """Sets the owner_type of this ApiOwnerDTO.


        :param owner_type: The owner_type of this ApiOwnerDTO.  # noqa: E501
        :type: str
        """

        self._owner_type = owner_type

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
        if issubclass(ApiOwnerDTO, dict):
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
        if not isinstance(other, ApiOwnerDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
