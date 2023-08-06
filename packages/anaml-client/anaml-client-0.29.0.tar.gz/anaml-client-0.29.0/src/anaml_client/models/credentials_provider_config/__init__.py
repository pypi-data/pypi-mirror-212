"""Generated implementation of credentials_provider_config."""

# WARNING DO NOT EDIT
# This code was generated from credentials-provider-config.mcn

from __future__ import annotations

import abc  # noqa: F401
import dataclasses  # noqa: F401
import datetime  # noqa: F401
import enum  # noqa: F401
import isodate  # noqa: F401
import json  # noqa: F401
import jsonschema  # noqa: F401
import logging  # noqa: F401
import typing  # noqa: F401
import uuid  # noqa: F401
try:
    from anaml_client.utils.serialisation import JsonObject  # noqa: F401
except ImportError:
    pass

from ..user_group_id import UserGroupId


@dataclasses.dataclass(frozen=True)
class GroupRule:
    """A Rule to determine which groups can receive credentials from a provider.
    
    Args:
        groups (typing.List[UserGroupId]): A data field.
        requireAll (bool): A data field.
        provider (CredentialsProviderConfig): A data field.
    """
    
    groups: typing.List[UserGroupId]
    requireAll: bool
    provider: CredentialsProviderConfig
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for GroupRule data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "groups": {
                    "type": "array",
                    "item": UserGroupId.json_schema()
                },
                "requireAll": {
                    "type": "boolean"
                },
                "provider": CredentialsProviderConfig.json_schema()
            },
            "required": [
                "groups",
                "requireAll",
                "provider",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> GroupRule:
        """Validate and parse JSON data into an instance of GroupRule.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of GroupRule.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return GroupRule(
                groups=[UserGroupId.from_json(v) for v in data["groups"]],
                requireAll=bool(data["requireAll"]),
                provider=CredentialsProviderConfig.from_json(data["provider"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing GroupRule",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "groups": [v.to_json() for v in self.groups],
            "requireAll": self.requireAll,
            "provider": self.provider.to_json()
        }


@dataclasses.dataclass(frozen=True)
class CredentialsProviderConfig(abc.ABC):
    """Configuration for credential loading."""
    
    ADT_TYPE: typing.ClassVar[str] = ""
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    @classmethod
    def json_schema(cls) -> CredentialsProviderConfig:
        """JSON schema for variant CredentialsProviderConfig.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        adt_types = [klass.ADT_TYPE for klass in cls.__subclasses__()]
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": adt_types
                }
            },
            "required": [
                "adt_type",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> CredentialsProviderConfig:
        """Validate and parse JSON data into an instance of CredentialsProviderConfig.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of CredentialsProviderConfig.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            adt_type = data.get("adt_type", None)
            for klass in cls.__subclasses__():
                if klass.ADT_TYPE == adt_type:
                    return klass.from_json(data)
            raise ValueError("Unknown adt_type: '{ty}'".format(ty=adt_type))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing CredentialsProviderConfig", exc_info=ex)
            raise
    
    @abc.abstractmethod
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class BasicCredentialsProviderConfig(CredentialsProviderConfig):
    """Basic credentials supplied directly.
    
    Args:
        username (str): A data field.
        password (str): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "basic"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    username: str
    password: str
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for BasicCredentialsProviderConfig data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [cls.ADT_TYPE]
                },
                "username": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                }
            },
            "required": [
                "adt_type",
                "username",
                "password",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> BasicCredentialsProviderConfig:
        """Validate and parse JSON data into an instance of BasicCredentialsProviderConfig.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of BasicCredentialsProviderConfig.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return BasicCredentialsProviderConfig(
                username=str(data["username"]),
                password=str(data["password"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing BasicCredentialsProviderConfig",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "adt_type": self.ADT_TYPE,
            "username": str(self.username),
            "password": str(self.password)
        }


@dataclasses.dataclass(frozen=True)
class FileCredentialsProviderConfig(CredentialsProviderConfig):
    """Credentials supplied by a file on drivers.
    
    Args:
        username (str): A data field.
        filepath (str): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "file"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    username: str
    filepath: str
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for FileCredentialsProviderConfig data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [cls.ADT_TYPE]
                },
                "username": {
                    "type": "string"
                },
                "filepath": {
                    "type": "string"
                }
            },
            "required": [
                "adt_type",
                "username",
                "filepath",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> FileCredentialsProviderConfig:
        """Validate and parse JSON data into an instance of FileCredentialsProviderConfig.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of FileCredentialsProviderConfig.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return FileCredentialsProviderConfig(
                username=str(data["username"]),
                filepath=str(data["filepath"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing FileCredentialsProviderConfig",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "adt_type": self.ADT_TYPE,
            "username": str(self.username),
            "filepath": str(self.filepath)
        }


@dataclasses.dataclass(frozen=True)
class AWSSMCredentialsProviderConfig(CredentialsProviderConfig):
    """Credentials supplied by AWS Secret Manager.
    
    Args:
        username (str): A data field.
        secretId (str): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "awssm"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    username: str
    secretId: str
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for AWSSMCredentialsProviderConfig data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [cls.ADT_TYPE]
                },
                "username": {
                    "type": "string"
                },
                "secretId": {
                    "type": "string"
                }
            },
            "required": [
                "adt_type",
                "username",
                "secretId",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> AWSSMCredentialsProviderConfig:
        """Validate and parse JSON data into an instance of AWSSMCredentialsProviderConfig.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of AWSSMCredentialsProviderConfig.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return AWSSMCredentialsProviderConfig(
                username=str(data["username"]),
                secretId=str(data["secretId"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing AWSSMCredentialsProviderConfig",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "adt_type": self.ADT_TYPE,
            "username": str(self.username),
            "secretId": str(self.secretId)
        }


@dataclasses.dataclass(frozen=True)
class GCPSMCredentialsProviderConfig(CredentialsProviderConfig):
    """Credentials supplied by GCP Secret Manager.
    
    Args:
        username (str): A data field.
        secretProject (str): A data field.
        secretId (str): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "gcpsm"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    username: str
    secretProject: str
    secretId: str
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for GCPSMCredentialsProviderConfig data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [cls.ADT_TYPE]
                },
                "username": {
                    "type": "string"
                },
                "secretProject": {
                    "type": "string"
                },
                "secretId": {
                    "type": "string"
                }
            },
            "required": [
                "adt_type",
                "username",
                "secretProject",
                "secretId",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> GCPSMCredentialsProviderConfig:
        """Validate and parse JSON data into an instance of GCPSMCredentialsProviderConfig.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of GCPSMCredentialsProviderConfig.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return GCPSMCredentialsProviderConfig(
                username=str(data["username"]),
                secretProject=str(data["secretProject"]),
                secretId=str(data["secretId"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing GCPSMCredentialsProviderConfig",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "adt_type": self.ADT_TYPE,
            "username": str(self.username),
            "secretProject": str(self.secretProject),
            "secretId": str(self.secretId)
        }


@dataclasses.dataclass(frozen=True)
class GroupCredentialsProviderConfig(CredentialsProviderConfig):
    """Credentials provider rules which are scoped to particular user roles.
    
    Args:
        rules (typing.List[GroupRule]): A data field.
        fallback (typing.Optional[CredentialsProviderConfig]): A data field.
    """
    
    ADT_TYPE: typing.ClassVar[str] = "group"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    rules: typing.List[GroupRule]
    fallback: typing.Optional[CredentialsProviderConfig]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for GroupCredentialsProviderConfig data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [cls.ADT_TYPE]
                },
                "rules": {
                    "type": "array",
                    "item": GroupRule.json_schema()
                },
                "fallback": {
                    "oneOf": [
                        {"type": "null"},
                        CredentialsProviderConfig.json_schema(),
                    ]
                }
            },
            "required": [
                "adt_type",
                "rules",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> GroupCredentialsProviderConfig:
        """Validate and parse JSON data into an instance of GroupCredentialsProviderConfig.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of GroupCredentialsProviderConfig.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return GroupCredentialsProviderConfig(
                rules=[GroupRule.from_json(v) for v in data["rules"]],
                fallback=(
                    lambda v: CredentialsProviderConfig.from_json(v) if v is not None else None
                )(
                    data.get("fallback", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing GroupCredentialsProviderConfig",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "adt_type": self.ADT_TYPE,
            "rules": [v.to_json() for v in self.rules],
            "fallback": (lambda v: v.to_json() if v is not None else v)(self.fallback)
        }
