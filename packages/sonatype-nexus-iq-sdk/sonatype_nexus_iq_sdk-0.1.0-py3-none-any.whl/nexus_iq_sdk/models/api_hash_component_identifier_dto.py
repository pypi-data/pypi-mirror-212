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


class ApiHashComponentIdentifierDTO(object):
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
        "hash": "str",
        "comment": "str",
        "create_time": "datetime",
        "component_identifier": "ApiComponentIdentifierDTOV2",
        "package_url": "str",
    }

    attribute_map = {
        "hash": "hash",
        "comment": "comment",
        "create_time": "createTime",
        "component_identifier": "componentIdentifier",
        "package_url": "packageUrl",
    }

    def __init__(
        self,
        hash=None,
        comment=None,
        create_time=None,
        component_identifier=None,
        package_url=None,
    ):  # noqa: E501
        """ApiHashComponentIdentifierDTO - a model defined in Swagger"""  # noqa: E501
        self._hash = None
        self._comment = None
        self._create_time = None
        self._component_identifier = None
        self._package_url = None
        self.discriminator = None
        if hash is not None:
            self.hash = hash
        if comment is not None:
            self.comment = comment
        if create_time is not None:
            self.create_time = create_time
        if component_identifier is not None:
            self.component_identifier = component_identifier
        if package_url is not None:
            self.package_url = package_url

    @property
    def hash(self):
        """Gets the hash of this ApiHashComponentIdentifierDTO.  # noqa: E501


        :return: The hash of this ApiHashComponentIdentifierDTO.  # noqa: E501
        :rtype: str
        """
        return self._hash

    @hash.setter
    def hash(self, hash):
        """Sets the hash of this ApiHashComponentIdentifierDTO.


        :param hash: The hash of this ApiHashComponentIdentifierDTO.  # noqa: E501
        :type: str
        """

        self._hash = hash

    @property
    def comment(self):
        """Gets the comment of this ApiHashComponentIdentifierDTO.  # noqa: E501


        :return: The comment of this ApiHashComponentIdentifierDTO.  # noqa: E501
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """Sets the comment of this ApiHashComponentIdentifierDTO.


        :param comment: The comment of this ApiHashComponentIdentifierDTO.  # noqa: E501
        :type: str
        """

        self._comment = comment

    @property
    def create_time(self):
        """Gets the create_time of this ApiHashComponentIdentifierDTO.  # noqa: E501


        :return: The create_time of this ApiHashComponentIdentifierDTO.  # noqa: E501
        :rtype: datetime
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this ApiHashComponentIdentifierDTO.


        :param create_time: The create_time of this ApiHashComponentIdentifierDTO.  # noqa: E501
        :type: datetime
        """

        self._create_time = create_time

    @property
    def component_identifier(self):
        """Gets the component_identifier of this ApiHashComponentIdentifierDTO.  # noqa: E501


        :return: The component_identifier of this ApiHashComponentIdentifierDTO.  # noqa: E501
        :rtype: ApiComponentIdentifierDTOV2
        """
        return self._component_identifier

    @component_identifier.setter
    def component_identifier(self, component_identifier):
        """Sets the component_identifier of this ApiHashComponentIdentifierDTO.


        :param component_identifier: The component_identifier of this ApiHashComponentIdentifierDTO.  # noqa: E501
        :type: ApiComponentIdentifierDTOV2
        """

        self._component_identifier = component_identifier

    @property
    def package_url(self):
        """Gets the package_url of this ApiHashComponentIdentifierDTO.  # noqa: E501


        :return: The package_url of this ApiHashComponentIdentifierDTO.  # noqa: E501
        :rtype: str
        """
        return self._package_url

    @package_url.setter
    def package_url(self, package_url):
        """Sets the package_url of this ApiHashComponentIdentifierDTO.


        :param package_url: The package_url of this ApiHashComponentIdentifierDTO.  # noqa: E501
        :type: str
        """

        self._package_url = package_url

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
        if issubclass(ApiHashComponentIdentifierDTO, dict):
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
        if not isinstance(other, ApiHashComponentIdentifierDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
