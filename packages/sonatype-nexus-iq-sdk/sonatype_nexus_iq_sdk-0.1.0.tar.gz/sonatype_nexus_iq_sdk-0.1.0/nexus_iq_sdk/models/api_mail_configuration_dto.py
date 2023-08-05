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


class ApiMailConfigurationDTO(object):
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
        "hostname": "str",
        "port": "int",
        "username": "str",
        "password": "list[str]",
        "password_is_included": "bool",
        "ssl_enabled": "bool",
        "start_tls_enabled": "bool",
        "system_email": "str",
    }

    attribute_map = {
        "hostname": "hostname",
        "port": "port",
        "username": "username",
        "password": "password",
        "password_is_included": "passwordIsIncluded",
        "ssl_enabled": "sslEnabled",
        "start_tls_enabled": "startTlsEnabled",
        "system_email": "systemEmail",
    }

    def __init__(
        self,
        hostname=None,
        port=None,
        username=None,
        password=None,
        password_is_included=None,
        ssl_enabled=None,
        start_tls_enabled=None,
        system_email=None,
    ):  # noqa: E501
        """ApiMailConfigurationDTO - a model defined in Swagger"""  # noqa: E501
        self._hostname = None
        self._port = None
        self._username = None
        self._password = None
        self._password_is_included = None
        self._ssl_enabled = None
        self._start_tls_enabled = None
        self._system_email = None
        self.discriminator = None
        if hostname is not None:
            self.hostname = hostname
        if port is not None:
            self.port = port
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password
        if password_is_included is not None:
            self.password_is_included = password_is_included
        if ssl_enabled is not None:
            self.ssl_enabled = ssl_enabled
        if start_tls_enabled is not None:
            self.start_tls_enabled = start_tls_enabled
        if system_email is not None:
            self.system_email = system_email

    @property
    def hostname(self):
        """Gets the hostname of this ApiMailConfigurationDTO.  # noqa: E501


        :return: The hostname of this ApiMailConfigurationDTO.  # noqa: E501
        :rtype: str
        """
        return self._hostname

    @hostname.setter
    def hostname(self, hostname):
        """Sets the hostname of this ApiMailConfigurationDTO.


        :param hostname: The hostname of this ApiMailConfigurationDTO.  # noqa: E501
        :type: str
        """

        self._hostname = hostname

    @property
    def port(self):
        """Gets the port of this ApiMailConfigurationDTO.  # noqa: E501


        :return: The port of this ApiMailConfigurationDTO.  # noqa: E501
        :rtype: int
        """
        return self._port

    @port.setter
    def port(self, port):
        """Sets the port of this ApiMailConfigurationDTO.


        :param port: The port of this ApiMailConfigurationDTO.  # noqa: E501
        :type: int
        """

        self._port = port

    @property
    def username(self):
        """Gets the username of this ApiMailConfigurationDTO.  # noqa: E501


        :return: The username of this ApiMailConfigurationDTO.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this ApiMailConfigurationDTO.


        :param username: The username of this ApiMailConfigurationDTO.  # noqa: E501
        :type: str
        """

        self._username = username

    @property
    def password(self):
        """Gets the password of this ApiMailConfigurationDTO.  # noqa: E501


        :return: The password of this ApiMailConfigurationDTO.  # noqa: E501
        :rtype: list[str]
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this ApiMailConfigurationDTO.


        :param password: The password of this ApiMailConfigurationDTO.  # noqa: E501
        :type: list[str]
        """

        self._password = password

    @property
    def password_is_included(self):
        """Gets the password_is_included of this ApiMailConfigurationDTO.  # noqa: E501


        :return: The password_is_included of this ApiMailConfigurationDTO.  # noqa: E501
        :rtype: bool
        """
        return self._password_is_included

    @password_is_included.setter
    def password_is_included(self, password_is_included):
        """Sets the password_is_included of this ApiMailConfigurationDTO.


        :param password_is_included: The password_is_included of this ApiMailConfigurationDTO.  # noqa: E501
        :type: bool
        """

        self._password_is_included = password_is_included

    @property
    def ssl_enabled(self):
        """Gets the ssl_enabled of this ApiMailConfigurationDTO.  # noqa: E501


        :return: The ssl_enabled of this ApiMailConfigurationDTO.  # noqa: E501
        :rtype: bool
        """
        return self._ssl_enabled

    @ssl_enabled.setter
    def ssl_enabled(self, ssl_enabled):
        """Sets the ssl_enabled of this ApiMailConfigurationDTO.


        :param ssl_enabled: The ssl_enabled of this ApiMailConfigurationDTO.  # noqa: E501
        :type: bool
        """

        self._ssl_enabled = ssl_enabled

    @property
    def start_tls_enabled(self):
        """Gets the start_tls_enabled of this ApiMailConfigurationDTO.  # noqa: E501


        :return: The start_tls_enabled of this ApiMailConfigurationDTO.  # noqa: E501
        :rtype: bool
        """
        return self._start_tls_enabled

    @start_tls_enabled.setter
    def start_tls_enabled(self, start_tls_enabled):
        """Sets the start_tls_enabled of this ApiMailConfigurationDTO.


        :param start_tls_enabled: The start_tls_enabled of this ApiMailConfigurationDTO.  # noqa: E501
        :type: bool
        """

        self._start_tls_enabled = start_tls_enabled

    @property
    def system_email(self):
        """Gets the system_email of this ApiMailConfigurationDTO.  # noqa: E501


        :return: The system_email of this ApiMailConfigurationDTO.  # noqa: E501
        :rtype: str
        """
        return self._system_email

    @system_email.setter
    def system_email(self, system_email):
        """Sets the system_email of this ApiMailConfigurationDTO.


        :param system_email: The system_email of this ApiMailConfigurationDTO.  # noqa: E501
        :type: str
        """

        self._system_email = system_email

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
        if issubclass(ApiMailConfigurationDTO, dict):
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
        if not isinstance(other, ApiMailConfigurationDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
