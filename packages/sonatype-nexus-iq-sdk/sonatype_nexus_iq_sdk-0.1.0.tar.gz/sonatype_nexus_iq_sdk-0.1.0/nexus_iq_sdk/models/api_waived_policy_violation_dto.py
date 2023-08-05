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


class ApiWaivedPolicyViolationDTO(object):
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
        "policy_id": "str",
        "policy_name": "str",
        "policy_violation_id": "str",
        "threat_level": "int",
        "constraint_violations": "list[ApiConstraintViolationDTO]",
        "policy_waiver": "ApiPolicyWaiverDTO",
    }

    attribute_map = {
        "policy_id": "policyId",
        "policy_name": "policyName",
        "policy_violation_id": "policyViolationId",
        "threat_level": "threatLevel",
        "constraint_violations": "constraintViolations",
        "policy_waiver": "policyWaiver",
    }

    def __init__(
        self,
        policy_id=None,
        policy_name=None,
        policy_violation_id=None,
        threat_level=None,
        constraint_violations=None,
        policy_waiver=None,
    ):  # noqa: E501
        """ApiWaivedPolicyViolationDTO - a model defined in Swagger"""  # noqa: E501
        self._policy_id = None
        self._policy_name = None
        self._policy_violation_id = None
        self._threat_level = None
        self._constraint_violations = None
        self._policy_waiver = None
        self.discriminator = None
        if policy_id is not None:
            self.policy_id = policy_id
        if policy_name is not None:
            self.policy_name = policy_name
        if policy_violation_id is not None:
            self.policy_violation_id = policy_violation_id
        if threat_level is not None:
            self.threat_level = threat_level
        if constraint_violations is not None:
            self.constraint_violations = constraint_violations
        if policy_waiver is not None:
            self.policy_waiver = policy_waiver

    @property
    def policy_id(self):
        """Gets the policy_id of this ApiWaivedPolicyViolationDTO.  # noqa: E501


        :return: The policy_id of this ApiWaivedPolicyViolationDTO.  # noqa: E501
        :rtype: str
        """
        return self._policy_id

    @policy_id.setter
    def policy_id(self, policy_id):
        """Sets the policy_id of this ApiWaivedPolicyViolationDTO.


        :param policy_id: The policy_id of this ApiWaivedPolicyViolationDTO.  # noqa: E501
        :type: str
        """

        self._policy_id = policy_id

    @property
    def policy_name(self):
        """Gets the policy_name of this ApiWaivedPolicyViolationDTO.  # noqa: E501


        :return: The policy_name of this ApiWaivedPolicyViolationDTO.  # noqa: E501
        :rtype: str
        """
        return self._policy_name

    @policy_name.setter
    def policy_name(self, policy_name):
        """Sets the policy_name of this ApiWaivedPolicyViolationDTO.


        :param policy_name: The policy_name of this ApiWaivedPolicyViolationDTO.  # noqa: E501
        :type: str
        """

        self._policy_name = policy_name

    @property
    def policy_violation_id(self):
        """Gets the policy_violation_id of this ApiWaivedPolicyViolationDTO.  # noqa: E501


        :return: The policy_violation_id of this ApiWaivedPolicyViolationDTO.  # noqa: E501
        :rtype: str
        """
        return self._policy_violation_id

    @policy_violation_id.setter
    def policy_violation_id(self, policy_violation_id):
        """Sets the policy_violation_id of this ApiWaivedPolicyViolationDTO.


        :param policy_violation_id: The policy_violation_id of this ApiWaivedPolicyViolationDTO.  # noqa: E501
        :type: str
        """

        self._policy_violation_id = policy_violation_id

    @property
    def threat_level(self):
        """Gets the threat_level of this ApiWaivedPolicyViolationDTO.  # noqa: E501


        :return: The threat_level of this ApiWaivedPolicyViolationDTO.  # noqa: E501
        :rtype: int
        """
        return self._threat_level

    @threat_level.setter
    def threat_level(self, threat_level):
        """Sets the threat_level of this ApiWaivedPolicyViolationDTO.


        :param threat_level: The threat_level of this ApiWaivedPolicyViolationDTO.  # noqa: E501
        :type: int
        """

        self._threat_level = threat_level

    @property
    def constraint_violations(self):
        """Gets the constraint_violations of this ApiWaivedPolicyViolationDTO.  # noqa: E501


        :return: The constraint_violations of this ApiWaivedPolicyViolationDTO.  # noqa: E501
        :rtype: list[ApiConstraintViolationDTO]
        """
        return self._constraint_violations

    @constraint_violations.setter
    def constraint_violations(self, constraint_violations):
        """Sets the constraint_violations of this ApiWaivedPolicyViolationDTO.


        :param constraint_violations: The constraint_violations of this ApiWaivedPolicyViolationDTO.  # noqa: E501
        :type: list[ApiConstraintViolationDTO]
        """

        self._constraint_violations = constraint_violations

    @property
    def policy_waiver(self):
        """Gets the policy_waiver of this ApiWaivedPolicyViolationDTO.  # noqa: E501


        :return: The policy_waiver of this ApiWaivedPolicyViolationDTO.  # noqa: E501
        :rtype: ApiPolicyWaiverDTO
        """
        return self._policy_waiver

    @policy_waiver.setter
    def policy_waiver(self, policy_waiver):
        """Sets the policy_waiver of this ApiWaivedPolicyViolationDTO.


        :param policy_waiver: The policy_waiver of this ApiWaivedPolicyViolationDTO.  # noqa: E501
        :type: ApiPolicyWaiverDTO
        """

        self._policy_waiver = policy_waiver

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
        if issubclass(ApiWaivedPolicyViolationDTO, dict):
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
        if not isinstance(other, ApiWaivedPolicyViolationDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
