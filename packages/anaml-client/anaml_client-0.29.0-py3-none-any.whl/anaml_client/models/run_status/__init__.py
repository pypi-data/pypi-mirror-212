"""Generated implementation of run_status."""

# WARNING DO NOT EDIT
# This code was generated from run-status.mcn

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


class RunStatus(enum.Enum):
    """Status of a job."""
    Pending = "pending"
    """The job is waiting to be started."""
    Running = "running"
    """The job is running."""
    Completed = "completed"
    """The job has completed successfully."""
    Cancel = "cancel"
    """A user has requested that the job should be cancelled."""
    Cancelled = "cancelled"
    """The job was cancelled by a user."""
    Failed = "failed"
    """The job has failed."""
    Redundant = "redundant"
    """The job was scheduled but no work is required of it."""
    
    @classmethod
    def json_schema(cls) -> dict:
        """JSON schema for 'RunStatus'.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": [
                        "pending",
                        "running",
                        "completed",
                        "cancel",
                        "cancelled",
                        "failed",
                        "redundant",
                    ]
                }
            },
            "required": [
                "adt_type",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> RunStatus:
        """Validate and parse JSON data into an instance of RunStatus.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of RunStatus.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return RunStatus(str(data['adt_type']))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing RunStatus", exc_info=ex)
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            JSON data ready to be serialised.
        """
        return {'adt_type': self.value}
    
    @classmethod
    def from_json_key(cls, data: str) -> RunStatus:
        """Validate and parse a value from a JSON dictionary key.
        
        Args:
            data (str): JSON data to validate and parse.
        
        Returns:
            An instance of RunStatus.
        """
        return RunStatus(str(data))
    
    def to_json_key(self) -> str:
        """Serialised this instanse as a JSON string for use as a dictionary key.
        
        Returns:
            A JSON string ready to be used as a key.
        """
        return str(self.value)
