"""Generated implementation of batch_output_mode."""

# WARNING DO NOT EDIT
# This code was generated from batch-output-mode.mcn

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
class BatchOutputMode:
    """Output mode for writing tables.
    
    Mode can only be one of:
    - overwrite
    - append
    - errorifexists
    - ignore
    
    Args:
        mode (str): A data field.
    """
    
    mode: str
    
    def __str__(self) -> str:
        """Return a str of the wrapped value."""
        return str(self.mode)
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for BatchOutputMode data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "string"
        }
    
    @classmethod
    def from_json(cls, data: dict) -> BatchOutputMode:
        """Validate and parse JSON data into an instance of BatchOutputMode.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of BatchOutputMode.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return BatchOutputMode(str(data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing BatchOutputMode", exc_info=ex)
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return str(self.mode)
    
    @classmethod
    def from_json_key(cls, data: str) -> BatchOutputMode:
        """Parse a JSON string such as a dictionary key."""
        return BatchOutputMode(str(data))
    
    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.mode)
