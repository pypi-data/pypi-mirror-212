"""Generated implementation of run_error."""

# WARNING DO NOT EDIT
# This code was generated from run-error.mcn

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


@dataclasses.dataclass(frozen=True)
class RunError:
    """An error with a potential stack trace.
    
    Args:
        message (str): A data field.
        stackTrace (typing.Optional[str]): A data field.
        code (typing.Optional[str]): A data field.
        params (typing.Optional[typing.Dict[str, str]]): A data field.
    """
    
    message: str
    stackTrace: typing.Optional[str]
    code: typing.Optional[str]
    params: typing.Optional[typing.Dict[str, str]]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for RunError data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string"
                },
                "stackTrace": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "string"},
                    ]
                },
                "code": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "string"},
                    ]
                },
                "params": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "object", "additionalProperties": {"type": "string"}},
                    ]
                }
            },
            "required": [
                "message",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> RunError:
        """Validate and parse JSON data into an instance of RunError.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of RunError.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return RunError(
                message=str(data["message"]),
                stackTrace=(
                    lambda v: str(v) if v is not None else None
                )(
                    data.get("stackTrace", None)
                ),
                code=(lambda v: str(v) if v is not None else None)(data.get("code", None)),
                params=(
                    lambda v: {str(k): str(v) for k, v in v.items()} if v is not None else None
                )(
                    data.get("params", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing RunError",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "message": str(self.message),
            "stackTrace": (lambda v: str(v) if v is not None else v)(self.stackTrace),
            "code": (lambda v: str(v) if v is not None else v)(self.code),
            "params": (lambda v: {str(k): str(v) for k, v in v.items()} if v is not None else v)(self.params)
        }
