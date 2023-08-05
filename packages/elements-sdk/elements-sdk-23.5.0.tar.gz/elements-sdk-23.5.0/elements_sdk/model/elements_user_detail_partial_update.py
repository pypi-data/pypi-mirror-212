"""
    ELEMENTS API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 2
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from elements_sdk.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
    OpenApiModel
)
from elements_sdk.exceptions import ApiAttributeError



class ElementsUserDetailPartialUpdate(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
        ('language',): {
            'None': None,
            'EN': "en",
            'FR': "fr",
            'DE': "de",
            'RU': "ru",
        },
    }

    validations = {
        ('default_page',): {
            'max_length': 63,
            'min_length': 1,
        },
        ('email',): {
            'max_length': 255,
        },
        ('full_name',): {
            'max_length': 255,
        },
        ('gid',): {
            'inclusive_maximum': 2147483647,
            'inclusive_minimum': -2147483648,
        },
        ('ldap_dn',): {
            'max_length': 255,
        },
        ('shaper_ceiling',): {
            'inclusive_maximum': 4611686018427388000,
            'inclusive_minimum': 0,
        },
        ('shaper_rate',): {
            'inclusive_maximum': 4611686018427388000,
            'inclusive_minimum': 0,
        },
        ('uid',): {
            'inclusive_maximum': 2147483647,
            'inclusive_minimum': -2147483648,
        },
        ('unix_username',): {
            'max_length': 255,
        },
        ('username',): {
            'max_length': 255,
            'min_length': 1,
        },
    }

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        return {
            'allow_changing_password': (bool,),  # noqa: E501
            'allow_wan_login': (bool,),  # noqa: E501
            'avatar': (str, none_type,),  # noqa: E501
            'default_page': (str,),  # noqa: E501
            'email': (str, none_type,),  # noqa: E501
            'expiry': (datetime, none_type,),  # noqa: E501
            'fm_bookmarks': ([str, none_type],),  # noqa: E501
            'full_name': (str, none_type,),  # noqa: E501
            'gid': (int, none_type,),  # noqa: E501
            'home': (int, none_type,),  # noqa: E501
            'is_external': (bool,),  # noqa: E501
            'is_cloud': (bool,),  # noqa: E501
            'is_cloud_default': (bool,),  # noqa: E501
            'is_enabled': (bool,),  # noqa: E501
            'language': (str, none_type,),  # noqa: E501
            'last_seen': (datetime, none_type,),  # noqa: E501
            'ldap': (bool, date, datetime, dict, float, int, list, str, none_type,),  # noqa: E501
            'ldap_dn': (str, none_type,),  # noqa: E501
            'password_change_required': (bool,),  # noqa: E501
            'permissions': ([str, none_type],),  # noqa: E501
            'shaper_ceiling': (int, none_type,),  # noqa: E501
            'shaper_rate': (int, none_type,),  # noqa: E501
            'totp_enabled': (bool,),  # noqa: E501
            'uid': (int, none_type,),  # noqa: E501
            'unix_username': (str, none_type,),  # noqa: E501
            'username': (str,),  # noqa: E501
            'groups': ([int],),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'allow_changing_password': 'allow_changing_password',  # noqa: E501
        'allow_wan_login': 'allow_wan_login',  # noqa: E501
        'avatar': 'avatar',  # noqa: E501
        'default_page': 'default_page',  # noqa: E501
        'email': 'email',  # noqa: E501
        'expiry': 'expiry',  # noqa: E501
        'fm_bookmarks': 'fm_bookmarks',  # noqa: E501
        'full_name': 'full_name',  # noqa: E501
        'gid': 'gid',  # noqa: E501
        'home': 'home',  # noqa: E501
        'is_external': 'is_external',  # noqa: E501
        'is_cloud': 'is_cloud',  # noqa: E501
        'is_cloud_default': 'is_cloud_default',  # noqa: E501
        'is_enabled': 'is_enabled',  # noqa: E501
        'language': 'language',  # noqa: E501
        'last_seen': 'last_seen',  # noqa: E501
        'ldap': 'ldap',  # noqa: E501
        'ldap_dn': 'ldap_dn',  # noqa: E501
        'password_change_required': 'password_change_required',  # noqa: E501
        'permissions': 'permissions',  # noqa: E501
        'shaper_ceiling': 'shaper_ceiling',  # noqa: E501
        'shaper_rate': 'shaper_rate',  # noqa: E501
        'totp_enabled': 'totp_enabled',  # noqa: E501
        'uid': 'uid',  # noqa: E501
        'unix_username': 'unix_username',  # noqa: E501
        'username': 'username',  # noqa: E501
        'groups': 'groups',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **xkwargs):  # noqa: E501
        """ElementsUserDetailPartialUpdate - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            allow_changing_password (bool): [optional]  # noqa: E501
            allow_wan_login (bool): [optional]  # noqa: E501
            avatar (str, none_type): [optional]  # noqa: E501
            default_page (str): [optional]  # noqa: E501
            email (str, none_type): [optional]  # noqa: E501
            expiry (datetime, none_type): [optional]  # noqa: E501
            fm_bookmarks ([str, none_type]): [optional]  # noqa: E501
            full_name (str, none_type): [optional]  # noqa: E501
            gid (int, none_type): [optional]  # noqa: E501
            home (int, none_type): [optional]  # noqa: E501
            is_external (bool): [optional]  # noqa: E501
            is_cloud (bool): [optional]  # noqa: E501
            is_cloud_default (bool): [optional]  # noqa: E501
            is_enabled (bool): [optional]  # noqa: E501
            language (str, none_type): [optional]  # noqa: E501
            last_seen (datetime, none_type): [optional]  # noqa: E501
            ldap (bool, date, datetime, dict, float, int, list, str, none_type): [optional]  # noqa: E501
            ldap_dn (str, none_type): [optional]  # noqa: E501
            password_change_required (bool): [optional]  # noqa: E501
            permissions ([str, none_type]): [optional]  # noqa: E501
            shaper_ceiling (int, none_type): [optional]  # noqa: E501
            shaper_rate (int, none_type): [optional]  # noqa: E501
            totp_enabled (bool): [optional]  # noqa: E501
            uid (int, none_type): [optional]  # noqa: E501
            unix_username (str, none_type): [optional]  # noqa: E501
            username (str): [optional]  # noqa: E501
            groups ([int]): [optional]  # noqa: E501
        """

        _check_type = xkwargs.pop('_check_type', True)
        _spec_property_naming = xkwargs.pop('_spec_property_naming', False)
        _path_to_item = xkwargs.pop('_path_to_item', ())
        _configuration = xkwargs.pop('_configuration', None)
        _visited_composed_classes = xkwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)


        for var_name, var_value in xkwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self


    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, *args, **xkwargs):  # noqa: E501
        """ElementsUserDetailPartialUpdate - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            allow_changing_password (bool): [optional]  # noqa: E501
            allow_wan_login (bool): [optional]  # noqa: E501
            avatar (str, none_type): [optional]  # noqa: E501
            default_page (str): [optional]  # noqa: E501
            email (str, none_type): [optional]  # noqa: E501
            expiry (datetime, none_type): [optional]  # noqa: E501
            fm_bookmarks ([str, none_type]): [optional]  # noqa: E501
            full_name (str, none_type): [optional]  # noqa: E501
            gid (int, none_type): [optional]  # noqa: E501
            home (int, none_type): [optional]  # noqa: E501
            is_external (bool): [optional]  # noqa: E501
            is_cloud (bool): [optional]  # noqa: E501
            is_cloud_default (bool): [optional]  # noqa: E501
            is_enabled (bool): [optional]  # noqa: E501
            language (str, none_type): [optional]  # noqa: E501
            last_seen (datetime, none_type): [optional]  # noqa: E501
            ldap (bool, date, datetime, dict, float, int, list, str, none_type): [optional]  # noqa: E501
            ldap_dn (str, none_type): [optional]  # noqa: E501
            password_change_required (bool): [optional]  # noqa: E501
            permissions ([str, none_type]): [optional]  # noqa: E501
            shaper_ceiling (int, none_type): [optional]  # noqa: E501
            shaper_rate (int, none_type): [optional]  # noqa: E501
            totp_enabled (bool): [optional]  # noqa: E501
            uid (int, none_type): [optional]  # noqa: E501
            unix_username (str, none_type): [optional]  # noqa: E501
            username (str): [optional]  # noqa: E501
            groups ([int]): [optional]  # noqa: E501
        """

        _check_type = xkwargs.pop('_check_type', True)
        _spec_property_naming = xkwargs.pop('_spec_property_naming', False)
        _path_to_item = xkwargs.pop('_path_to_item', ())
        _configuration = xkwargs.pop('_configuration', None)
        _visited_composed_classes = xkwargs.pop('_visited_composed_classes', ())

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)


        for var_name, var_value in xkwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")

