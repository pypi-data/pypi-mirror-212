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


class ApiLicenseLegalMetadataDTO(object):
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
        "license_id": "str",
        "license_name": "str",
        "license_text": "str",
        "obligations": "list[LicenseObligationDTO]",
        "threat_group": "LicenseThreatGroupDTO",
        "is_multi": "bool",
        "single_license_ids": "list[str]",
    }

    attribute_map = {
        "license_id": "licenseId",
        "license_name": "licenseName",
        "license_text": "licenseText",
        "obligations": "obligations",
        "threat_group": "threatGroup",
        "is_multi": "isMulti",
        "single_license_ids": "singleLicenseIds",
    }

    def __init__(
        self,
        license_id=None,
        license_name=None,
        license_text=None,
        obligations=None,
        threat_group=None,
        is_multi=None,
        single_license_ids=None,
    ):  # noqa: E501
        """ApiLicenseLegalMetadataDTO - a model defined in Swagger"""  # noqa: E501
        self._license_id = None
        self._license_name = None
        self._license_text = None
        self._obligations = None
        self._threat_group = None
        self._is_multi = None
        self._single_license_ids = None
        self.discriminator = None
        if license_id is not None:
            self.license_id = license_id
        if license_name is not None:
            self.license_name = license_name
        if license_text is not None:
            self.license_text = license_text
        if obligations is not None:
            self.obligations = obligations
        if threat_group is not None:
            self.threat_group = threat_group
        if is_multi is not None:
            self.is_multi = is_multi
        if single_license_ids is not None:
            self.single_license_ids = single_license_ids

    @property
    def license_id(self):
        """Gets the license_id of this ApiLicenseLegalMetadataDTO.  # noqa: E501


        :return: The license_id of this ApiLicenseLegalMetadataDTO.  # noqa: E501
        :rtype: str
        """
        return self._license_id

    @license_id.setter
    def license_id(self, license_id):
        """Sets the license_id of this ApiLicenseLegalMetadataDTO.


        :param license_id: The license_id of this ApiLicenseLegalMetadataDTO.  # noqa: E501
        :type: str
        """

        self._license_id = license_id

    @property
    def license_name(self):
        """Gets the license_name of this ApiLicenseLegalMetadataDTO.  # noqa: E501


        :return: The license_name of this ApiLicenseLegalMetadataDTO.  # noqa: E501
        :rtype: str
        """
        return self._license_name

    @license_name.setter
    def license_name(self, license_name):
        """Sets the license_name of this ApiLicenseLegalMetadataDTO.


        :param license_name: The license_name of this ApiLicenseLegalMetadataDTO.  # noqa: E501
        :type: str
        """

        self._license_name = license_name

    @property
    def license_text(self):
        """Gets the license_text of this ApiLicenseLegalMetadataDTO.  # noqa: E501


        :return: The license_text of this ApiLicenseLegalMetadataDTO.  # noqa: E501
        :rtype: str
        """
        return self._license_text

    @license_text.setter
    def license_text(self, license_text):
        """Sets the license_text of this ApiLicenseLegalMetadataDTO.


        :param license_text: The license_text of this ApiLicenseLegalMetadataDTO.  # noqa: E501
        :type: str
        """

        self._license_text = license_text

    @property
    def obligations(self):
        """Gets the obligations of this ApiLicenseLegalMetadataDTO.  # noqa: E501


        :return: The obligations of this ApiLicenseLegalMetadataDTO.  # noqa: E501
        :rtype: list[LicenseObligationDTO]
        """
        return self._obligations

    @obligations.setter
    def obligations(self, obligations):
        """Sets the obligations of this ApiLicenseLegalMetadataDTO.


        :param obligations: The obligations of this ApiLicenseLegalMetadataDTO.  # noqa: E501
        :type: list[LicenseObligationDTO]
        """

        self._obligations = obligations

    @property
    def threat_group(self):
        """Gets the threat_group of this ApiLicenseLegalMetadataDTO.  # noqa: E501


        :return: The threat_group of this ApiLicenseLegalMetadataDTO.  # noqa: E501
        :rtype: LicenseThreatGroupDTO
        """
        return self._threat_group

    @threat_group.setter
    def threat_group(self, threat_group):
        """Sets the threat_group of this ApiLicenseLegalMetadataDTO.


        :param threat_group: The threat_group of this ApiLicenseLegalMetadataDTO.  # noqa: E501
        :type: LicenseThreatGroupDTO
        """

        self._threat_group = threat_group

    @property
    def is_multi(self):
        """Gets the is_multi of this ApiLicenseLegalMetadataDTO.  # noqa: E501


        :return: The is_multi of this ApiLicenseLegalMetadataDTO.  # noqa: E501
        :rtype: bool
        """
        return self._is_multi

    @is_multi.setter
    def is_multi(self, is_multi):
        """Sets the is_multi of this ApiLicenseLegalMetadataDTO.


        :param is_multi: The is_multi of this ApiLicenseLegalMetadataDTO.  # noqa: E501
        :type: bool
        """

        self._is_multi = is_multi

    @property
    def single_license_ids(self):
        """Gets the single_license_ids of this ApiLicenseLegalMetadataDTO.  # noqa: E501


        :return: The single_license_ids of this ApiLicenseLegalMetadataDTO.  # noqa: E501
        :rtype: list[str]
        """
        return self._single_license_ids

    @single_license_ids.setter
    def single_license_ids(self, single_license_ids):
        """Sets the single_license_ids of this ApiLicenseLegalMetadataDTO.


        :param single_license_ids: The single_license_ids of this ApiLicenseLegalMetadataDTO.  # noqa: E501
        :type: list[str]
        """

        self._single_license_ids = single_license_ids

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
        if issubclass(ApiLicenseLegalMetadataDTO, dict):
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
        if not isinstance(other, ApiLicenseLegalMetadataDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
