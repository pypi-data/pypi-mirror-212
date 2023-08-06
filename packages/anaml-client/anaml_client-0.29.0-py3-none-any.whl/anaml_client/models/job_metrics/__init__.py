"""Generated implementation of job_metrics."""

# WARNING DO NOT EDIT
# This code was generated from job-metrics.mcn

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
class JobMetrics:
    """Execution statistics for a job run.
    
    Args:
        appId (str): A data field.
        anamlVersion (str): A data field.
        executorInstances (typing.Optional[str]): A data field.
        executorCores (typing.Optional[str]): A data field.
        executorMemory (typing.Optional[str]): A data field.
        executorsMax (int): A data field.
        coresMax (int): A data field.
        assignedExecutorSeconds (typing.Optional[int]): A data field.
        runTimeSeconds (int): A data field.
        cpuTimeSeconds (int): A data field.
        gcTimeSeconds (int): A data field.
        bytesRead (int): A data field.
        bytesWritten (int): A data field.
        recordsWritten (typing.Optional[int]): A data field.
        runningTasks (int): A data field.
        successfulTasks (int): A data field.
        failedTasks (int): A data field.
        totalTasks (int): A data field.
        shuffleLocalBytesRead (int): A data field.
        shuffleRemoteBytesRead (int): A data field.
        shuffleBytesWritten (int): A data field.
        updated (typing.Optional[datetime.datetime]): A data field.
    """
    
    appId: str
    anamlVersion: str
    executorInstances: typing.Optional[str]
    executorCores: typing.Optional[str]
    executorMemory: typing.Optional[str]
    executorsMax: int
    coresMax: int
    assignedExecutorSeconds: typing.Optional[int]
    runTimeSeconds: int
    cpuTimeSeconds: int
    gcTimeSeconds: int
    bytesRead: int
    bytesWritten: int
    recordsWritten: typing.Optional[int]
    runningTasks: int
    successfulTasks: int
    failedTasks: int
    totalTasks: int
    shuffleLocalBytesRead: int
    shuffleRemoteBytesRead: int
    shuffleBytesWritten: int
    updated: typing.Optional[datetime.datetime]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for JobMetrics data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "appId": {
                    "type": "string"
                },
                "anamlVersion": {
                    "type": "string"
                },
                "executorInstances": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "string"},
                    ]
                },
                "executorCores": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "string"},
                    ]
                },
                "executorMemory": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "string"},
                    ]
                },
                "executorsMax": {
                    "type": "integer"
                },
                "coresMax": {
                    "type": "integer"
                },
                "assignedExecutorSeconds": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "integer"},
                    ]
                },
                "runTimeSeconds": {
                    "type": "integer"
                },
                "cpuTimeSeconds": {
                    "type": "integer"
                },
                "gcTimeSeconds": {
                    "type": "integer"
                },
                "bytesRead": {
                    "type": "integer"
                },
                "bytesWritten": {
                    "type": "integer"
                },
                "recordsWritten": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "integer"},
                    ]
                },
                "runningTasks": {
                    "type": "integer"
                },
                "successfulTasks": {
                    "type": "integer"
                },
                "failedTasks": {
                    "type": "integer"
                },
                "totalTasks": {
                    "type": "integer"
                },
                "shuffleLocalBytesRead": {
                    "type": "integer"
                },
                "shuffleRemoteBytesRead": {
                    "type": "integer"
                },
                "shuffleBytesWritten": {
                    "type": "integer"
                },
                "updated": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "string", "format": "date-time"},
                    ]
                }
            },
            "required": [
                "appId",
                "anamlVersion",
                "executorsMax",
                "coresMax",
                "runTimeSeconds",
                "cpuTimeSeconds",
                "gcTimeSeconds",
                "bytesRead",
                "bytesWritten",
                "runningTasks",
                "successfulTasks",
                "failedTasks",
                "totalTasks",
                "shuffleLocalBytesRead",
                "shuffleRemoteBytesRead",
                "shuffleBytesWritten",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> JobMetrics:
        """Validate and parse JSON data into an instance of JobMetrics.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of JobMetrics.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return JobMetrics(
                appId=str(data["appId"]),
                anamlVersion=str(data["anamlVersion"]),
                executorInstances=(
                    lambda v: str(v) if v is not None else None
                )(
                    data.get("executorInstances", None)
                ),
                executorCores=(
                    lambda v: str(v) if v is not None else None
                )(
                    data.get("executorCores", None)
                ),
                executorMemory=(
                    lambda v: str(v) if v is not None else None
                )(
                    data.get("executorMemory", None)
                ),
                executorsMax=int(data["executorsMax"]),
                coresMax=int(data["coresMax"]),
                assignedExecutorSeconds=(
                    lambda v: int(v) if v is not None else None
                )(
                    data.get("assignedExecutorSeconds", None)
                ),
                runTimeSeconds=int(data["runTimeSeconds"]),
                cpuTimeSeconds=int(data["cpuTimeSeconds"]),
                gcTimeSeconds=int(data["gcTimeSeconds"]),
                bytesRead=int(data["bytesRead"]),
                bytesWritten=int(data["bytesWritten"]),
                recordsWritten=(
                    lambda v: int(v) if v is not None else None
                )(
                    data.get("recordsWritten", None)
                ),
                runningTasks=int(data["runningTasks"]),
                successfulTasks=int(data["successfulTasks"]),
                failedTasks=int(data["failedTasks"]),
                totalTasks=int(data["totalTasks"]),
                shuffleLocalBytesRead=int(data["shuffleLocalBytesRead"]),
                shuffleRemoteBytesRead=int(data["shuffleRemoteBytesRead"]),
                shuffleBytesWritten=int(data["shuffleBytesWritten"]),
                updated=(
                    lambda v: isodate.parse_datetime(v) if v is not None else None
                )(
                    data.get("updated", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing JobMetrics",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "appId": str(self.appId),
            "anamlVersion": str(self.anamlVersion),
            "executorInstances": (lambda v: str(v) if v is not None else v)(self.executorInstances),
            "executorCores": (lambda v: str(v) if v is not None else v)(self.executorCores),
            "executorMemory": (lambda v: str(v) if v is not None else v)(self.executorMemory),
            "executorsMax": int(self.executorsMax),
            "coresMax": int(self.coresMax),
            "assignedExecutorSeconds": (lambda v: v if v is not None else v)(self.assignedExecutorSeconds),
            "runTimeSeconds": self.runTimeSeconds,
            "cpuTimeSeconds": self.cpuTimeSeconds,
            "gcTimeSeconds": self.gcTimeSeconds,
            "bytesRead": self.bytesRead,
            "bytesWritten": self.bytesWritten,
            "recordsWritten": (lambda v: v if v is not None else v)(self.recordsWritten),
            "runningTasks": int(self.runningTasks),
            "successfulTasks": int(self.successfulTasks),
            "failedTasks": int(self.failedTasks),
            "totalTasks": int(self.totalTasks),
            "shuffleLocalBytesRead": self.shuffleLocalBytesRead,
            "shuffleRemoteBytesRead": self.shuffleRemoteBytesRead,
            "shuffleBytesWritten": self.shuffleBytesWritten,
            "updated": (lambda v: v.strftime('%Y-%m-%dT%H:%M:%S.%f%z') if v is not None else v)(self.updated)
        }
