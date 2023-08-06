"""Generated implementation of date_range."""

# WARNING DO NOT EDIT
# This code was generated from date-range.mcn

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
class DateRange:
    """Inclusive Date range.
    
    Args:
        startDate (datetime.date): A data field.
        endDate (datetime.date): A data field.
    """
    
    startDate: datetime.date
    endDate: datetime.date
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for DateRange data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "startDate": {
                    "type": "string",
                    "format": "date"
                },
                "endDate": {
                    "type": "string",
                    "format": "date"
                }
            },
            "required": [
                "startDate",
                "endDate",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> DateRange:
        """Validate and parse JSON data into an instance of DateRange.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of DateRange.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return DateRange(
                startDate=datetime.date.fromisoformat(data["startDate"]),
                endDate=datetime.date.fromisoformat(data["endDate"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing DateRange",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "startDate": self.startDate.isoformat(),
            "endDate": self.endDate.isoformat()
        }
