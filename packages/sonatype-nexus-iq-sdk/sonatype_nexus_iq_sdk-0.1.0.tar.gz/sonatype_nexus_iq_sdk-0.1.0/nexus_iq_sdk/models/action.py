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


class Action(object):
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
    swagger_types = {"action_type_id": "str", "target": "str", "target_type": "str"}

    attribute_map = {
        "action_type_id": "actionTypeId",
        "target": "target",
        "target_type": "targetType",
    }

    def __init__(
        self, action_type_id=None, target=None, target_type=None
    ):  # noqa: E501
        """Action - a model defined in Swagger"""  # noqa: E501
        self._action_type_id = None
        self._target = None
        self._target_type = None
        self.discriminator = None
        if action_type_id is not None:
            self.action_type_id = action_type_id
        if target is not None:
            self.target = target
        if target_type is not None:
            self.target_type = target_type

    @property
    def action_type_id(self):
        """Gets the action_type_id of this Action.  # noqa: E501


        :return: The action_type_id of this Action.  # noqa: E501
        :rtype: str
        """
        return self._action_type_id

    @action_type_id.setter
    def action_type_id(self, action_type_id):
        """Sets the action_type_id of this Action.


        :param action_type_id: The action_type_id of this Action.  # noqa: E501
        :type: str
        """

        self._action_type_id = action_type_id

    @property
    def target(self):
        """Gets the target of this Action.  # noqa: E501


        :return: The target of this Action.  # noqa: E501
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """Sets the target of this Action.


        :param target: The target of this Action.  # noqa: E501
        :type: str
        """

        self._target = target

    @property
    def target_type(self):
        """Gets the target_type of this Action.  # noqa: E501


        :return: The target_type of this Action.  # noqa: E501
        :rtype: str
        """
        return self._target_type

    @target_type.setter
    def target_type(self, target_type):
        """Sets the target_type of this Action.


        :param target_type: The target_type of this Action.  # noqa: E501
        :type: str
        """

        self._target_type = target_type

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
        if issubclass(Action, dict):
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
        if not isinstance(other, Action):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
