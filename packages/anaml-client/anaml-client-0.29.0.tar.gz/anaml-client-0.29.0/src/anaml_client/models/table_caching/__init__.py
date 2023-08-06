"""Generated implementation of table_caching."""

# WARNING DO NOT EDIT
# This code was generated from table-caching.mcn

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

from ..cluster import ClusterId, ClusterPropertySetId
from ..commit import CommitId
from ..entity import EntityId
from ..feature_store import VersionTarget
from ..feature_store_run import ExecutionStatistics
from ..run_error import RunError
from ..run_status import RunStatus
from ..schedule import Duration, Schedule
from ..table import TableId


@dataclasses.dataclass(frozen=True)
class TableCachingJobId:
    """Unique identifier of a table caching job.
    
    Args:
        value (int): A data field.
    """
    
    value: int
    
    def __str__(self) -> str:
        """Return a str of the wrapped value."""
        return str(self.value)
    
    def __int__(self) -> int:
        """Return an int of the wrapped value."""
        return int(self.value)
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableCachingJobId data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "integer"
        }
    
    @classmethod
    def from_json(cls, data: dict) -> TableCachingJobId:
        """Validate and parse JSON data into an instance of TableCachingJobId.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of TableCachingJobId.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableCachingJobId(int(data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing TableCachingJobId", exc_info=ex)
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return int(self.value)
    
    @classmethod
    def from_json_key(cls, data: str) -> TableCachingJobId:
        """Parse a JSON string such as a dictionary key."""
        return TableCachingJobId(int(data))
    
    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.value)


@dataclasses.dataclass(frozen=True)
class TableCachingJobName:
    """Unique name for a table caching job.
    
    Args:
        value (str): A data field.
    """
    
    value: str
    
    def __str__(self) -> str:
        """Return a str of the wrapped value."""
        return str(self.value)
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableCachingJobName data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "string"
        }
    
    @classmethod
    def from_json(cls, data: dict) -> TableCachingJobName:
        """Validate and parse JSON data into an instance of TableCachingJobName.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of TableCachingJobName.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableCachingJobName(str(data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing TableCachingJobName", exc_info=ex)
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return str(self.value)
    
    @classmethod
    def from_json_key(cls, data: str) -> TableCachingJobName:
        """Parse a JSON string such as a dictionary key."""
        return TableCachingJobName(str(data))
    
    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.value)


@dataclasses.dataclass(frozen=True)
class TableCachingJobVersionId:
    """Unique identifier for a specific version of a table caching job.
    
    Args:
        value (uuid.UUID): A data field.
    """
    
    value: uuid.UUID
    
    def __str__(self) -> str:
        """Return a str of the wrapped value."""
        return str(self.value)
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableCachingJobVersionId data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "string",
            "format": "uuid"
        }
    
    @classmethod
    def from_json(cls, data: dict) -> TableCachingJobVersionId:
        """Validate and parse JSON data into an instance of TableCachingJobVersionId.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of TableCachingJobVersionId.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableCachingJobVersionId(uuid.UUID(hex=data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing TableCachingJobVersionId", exc_info=ex)
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return str(self.value)
    
    @classmethod
    def from_json_key(cls, data: str) -> TableCachingJobVersionId:
        """Parse a JSON string such as a dictionary key."""
        return TableCachingJobVersionId((lambda s: uuid.UUID(hex=s))(data))
    
    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.value)


@dataclasses.dataclass(frozen=True)
class TableCachingRunId:
    """Unique identifier of a table caching job run.
    
    Args:
        value (int): A data field.
    """
    
    value: int
    
    def __str__(self) -> str:
        """Return a str of the wrapped value."""
        return str(self.value)
    
    def __int__(self) -> int:
        """Return an int of the wrapped value."""
        return int(self.value)
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableCachingRunId data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "integer"
        }
    
    @classmethod
    def from_json(cls, data: dict) -> TableCachingRunId:
        """Validate and parse JSON data into an instance of TableCachingRunId.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of TableCachingRunId.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableCachingRunId(int(data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing TableCachingRunId", exc_info=ex)
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return self.value
    
    @classmethod
    def from_json_key(cls, data: str) -> TableCachingRunId:
        """Parse a JSON string such as a dictionary key."""
        return TableCachingRunId(int(data))
    
    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.value)


@dataclasses.dataclass(frozen=True)
class TableCacheId:
    """Unique identifier of a table cache.
    
    Args:
        value (uuid.UUID): A data field.
    """
    
    value: uuid.UUID
    
    def __str__(self) -> str:
        """Return a str of the wrapped value."""
        return str(self.value)
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableCacheId data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "string",
            "format": "uuid"
        }
    
    @classmethod
    def from_json(cls, data: dict) -> TableCacheId:
        """Validate and parse JSON data into an instance of TableCacheId.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of TableCacheId.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableCacheId(uuid.UUID(hex=data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing TableCacheId", exc_info=ex)
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return str(self.value)
    
    @classmethod
    def from_json_key(cls, data: str) -> TableCacheId:
        """Parse a JSON string such as a dictionary key."""
        return TableCacheId((lambda s: uuid.UUID(hex=s))(data))
    
    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.value)


@dataclasses.dataclass(frozen=True)
class HashBits:
    """The number of bits used to partition the data.
    
    Args:
        bits (int): A data field.
    """
    
    bits: int
    
    def __str__(self) -> str:
        """Return a str of the wrapped value."""
        return str(self.bits)
    
    def __int__(self) -> int:
        """Return an int of the wrapped value."""
        return int(self.bits)
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for HashBits data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "integer"
        }
    
    @classmethod
    def from_json(cls, data: dict) -> HashBits:
        """Validate and parse JSON data into an instance of HashBits.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of HashBits.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return HashBits(int(data))
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug("Invalid JSON data received while parsing HashBits", exc_info=ex)
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return int(self.bits)
    
    @classmethod
    def from_json_key(cls, data: str) -> HashBits:
        """Parse a JSON string such as a dictionary key."""
        return HashBits(int(data))
    
    def to_json_key(self) -> str:
        """Serialise as a JSON string suitable for use as a dictionary key."""
        return str(self.bits)


@dataclasses.dataclass(frozen=True)
class TableCache:
    """Details of a table cache.
    
    Args:
        id (TableCacheId): A data field.
        job (typing.Optional[TableCachingJobId]): A data field.
        run (typing.Optional[TableCachingRunId]): A data field.
        uri (str): A data field.
        table (TableId): A data field.
        entity (EntityId): A data field.
        hashBits (typing.Optional[HashBits]): A data field.
        commit (CommitId): A data field.
        created (datetime.datetime): A data field.
    """
    
    id: TableCacheId
    job: typing.Optional[TableCachingJobId]
    run: typing.Optional[TableCachingRunId]
    uri: str
    table: TableId
    entity: EntityId
    hashBits: typing.Optional[HashBits]
    commit: CommitId
    created: datetime.datetime
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableCache data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "id": TableCacheId.json_schema(),
                "job": {
                    "oneOf": [
                        {"type": "null"},
                        TableCachingJobId.json_schema(),
                    ]
                },
                "run": {
                    "oneOf": [
                        {"type": "null"},
                        TableCachingRunId.json_schema(),
                    ]
                },
                "uri": {
                    "type": "string"
                },
                "table": TableId.json_schema(),
                "entity": EntityId.json_schema(),
                "hashBits": {
                    "oneOf": [
                        {"type": "null"},
                        HashBits.json_schema(),
                    ]
                },
                "commit": CommitId.json_schema(),
                "created": {
                    "type": "string",
                    "format": "date-time"
                }
            },
            "required": [
                "id",
                "uri",
                "table",
                "entity",
                "commit",
                "created",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> TableCache:
        """Validate and parse JSON data into an instance of TableCache.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of TableCache.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableCache(
                id=TableCacheId.from_json(data["id"]),
                job=(
                    lambda v: TableCachingJobId.from_json(v) if v is not None else None
                )(
                    data.get("job", None)
                ),
                run=(
                    lambda v: TableCachingRunId.from_json(v) if v is not None else None
                )(
                    data.get("run", None)
                ),
                uri=str(data["uri"]),
                table=TableId.from_json(data["table"]),
                entity=EntityId.from_json(data["entity"]),
                hashBits=(
                    lambda v: HashBits.from_json(v) if v is not None else None
                )(
                    data.get("hashBits", None)
                ),
                commit=CommitId.from_json(data["commit"]),
                created=isodate.parse_datetime(data["created"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing TableCache",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "id": self.id.to_json(),
            "job": (lambda v: v.to_json() if v is not None else v)(self.job),
            "run": (lambda v: v.to_json() if v is not None else v)(self.run),
            "uri": str(self.uri),
            "table": self.table.to_json(),
            "entity": self.entity.to_json(),
            "hashBits": (lambda v: v.to_json() if v is not None else v)(self.hashBits),
            "commit": self.commit.to_json(),
            "created": self.created.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        }


@dataclasses.dataclass(frozen=True)
class TableCachingSpec:
    """Details of the table and entity to be cached.
    
    Args:
        table (TableId): A data field.
        entity (EntityId): A data field.
    """
    
    table: TableId
    entity: EntityId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableCachingSpec data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "table": TableId.json_schema(),
                "entity": EntityId.json_schema()
            },
            "required": [
                "table",
                "entity",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> TableCachingSpec:
        """Validate and parse JSON data into an instance of TableCachingSpec.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of TableCachingSpec.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableCachingSpec(
                table=TableId.from_json(data["table"]),
                entity=EntityId.from_json(data["entity"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing TableCachingSpec",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "table": self.table.to_json(),
            "entity": self.entity.to_json()
        }


@dataclasses.dataclass(frozen=True)
class CachingPlan(abc.ABC):
    """Method for determining which tables and entities to collect samples for."""
    
    ADT_TYPE: typing.ClassVar[str] = ""
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    @classmethod
    def json_schema(cls) -> CachingPlan:
        """JSON schema for variant CachingPlan.
        
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
    def from_json(cls, data: dict) -> CachingPlan:
        """Validate and parse JSON data into an instance of CachingPlan.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of CachingPlan.
        
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
            logging.debug("Invalid JSON data received while parsing CachingPlan", exc_info=ex)
            raise
    
    @abc.abstractmethod
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class InclusionCachingPlan(CachingPlan):
    """Args:
        specs (typing.List[TableCachingSpec]): A data field."""
    
    ADT_TYPE: typing.ClassVar[str] = "inclusion"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    specs: typing.List[TableCachingSpec]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for InclusionCachingPlan data.
        
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
                "specs": {
                    "type": "array",
                    "item": TableCachingSpec.json_schema()
                }
            },
            "required": [
                "adt_type",
                "specs",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> InclusionCachingPlan:
        """Validate and parse JSON data into an instance of InclusionCachingPlan.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of InclusionCachingPlan.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return InclusionCachingPlan(
                specs=[TableCachingSpec.from_json(v) for v in data["specs"]],
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing InclusionCachingPlan",
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
            "specs": [v.to_json() for v in self.specs]
        }


@dataclasses.dataclass(frozen=True)
class AutoCachingPlan(CachingPlan):
    """Args:
        excluded (typing.List[TableCachingSpec]): A data field."""
    
    ADT_TYPE: typing.ClassVar[str] = "auto"
    adt_type: str = dataclasses.field(init=False, repr=False, default=ADT_TYPE)
    
    excluded: typing.List[TableCachingSpec]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for AutoCachingPlan data.
        
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
                "excluded": {
                    "type": "array",
                    "item": TableCachingSpec.json_schema()
                }
            },
            "required": [
                "adt_type",
                "excluded",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> AutoCachingPlan:
        """Validate and parse JSON data into an instance of AutoCachingPlan.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of AutoCachingPlan.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return AutoCachingPlan(
                excluded=[TableCachingSpec.from_json(v) for v in data["excluded"]],
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing AutoCachingPlan",
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
            "excluded": [v.to_json() for v in self.excluded]
        }


@dataclasses.dataclass(frozen=True)
class TableCachingJobCreationRequest:
    """Request to create a new table caching job.
    
    Args:
        name (TableCachingJobName): A data field.
        description (str): A data field.
        plan (CachingPlan): A data field.
        retainment (typing.Optional[Duration]): A data field.
        prefixURI (str): A data field.
        schedule (Schedule): A data field.
        cluster (ClusterId): A data field.
        clusterPropertySets (typing.Optional[typing.List[ClusterPropertySetId]]): A data field.
        versionTarget (typing.Optional[VersionTarget]): A data field.
    """
    
    name: TableCachingJobName
    description: str
    plan: CachingPlan
    retainment: typing.Optional[Duration]
    prefixURI: str
    schedule: Schedule
    cluster: ClusterId
    clusterPropertySets: typing.Optional[typing.List[ClusterPropertySetId]]
    versionTarget: typing.Optional[VersionTarget]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableCachingJobCreationRequest data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "name": TableCachingJobName.json_schema(),
                "description": {
                    "type": "string"
                },
                "plan": CachingPlan.json_schema(),
                "retainment": {
                    "oneOf": [
                        {"type": "null"},
                        Duration.json_schema(),
                    ]
                },
                "prefixURI": {
                    "type": "string"
                },
                "schedule": Schedule.json_schema(),
                "cluster": ClusterId.json_schema(),
                "clusterPropertySets": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "array", "item": ClusterPropertySetId.json_schema()},
                    ]
                },
                "versionTarget": {
                    "oneOf": [
                        {"type": "null"},
                        VersionTarget.json_schema(),
                    ]
                }
            },
            "required": [
                "name",
                "description",
                "plan",
                "prefixURI",
                "schedule",
                "cluster",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> TableCachingJobCreationRequest:
        """Validate and parse JSON data into an instance of TableCachingJobCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of TableCachingJobCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableCachingJobCreationRequest(
                name=TableCachingJobName.from_json(data["name"]),
                description=str(data["description"]),
                plan=CachingPlan.from_json(data["plan"]),
                retainment=(
                    lambda v: Duration.from_json(v) if v is not None else None
                )(
                    data.get("retainment", None)
                ),
                prefixURI=str(data["prefixURI"]),
                schedule=Schedule.from_json(data["schedule"]),
                cluster=ClusterId.from_json(data["cluster"]),
                clusterPropertySets=(
                    lambda v: [ClusterPropertySetId.from_json(v) for v in v] if v is not None else None
                )(
                    data.get("clusterPropertySets", None)
                ),
                versionTarget=(
                    lambda v: VersionTarget.from_json(v) if v is not None else None
                )(
                    data.get("versionTarget", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing TableCachingJobCreationRequest",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "name": self.name.to_json(),
            "description": str(self.description),
            "plan": self.plan.to_json(),
            "retainment": (lambda v: v.to_json() if v is not None else v)(self.retainment),
            "prefixURI": str(self.prefixURI),
            "schedule": self.schedule.to_json(),
            "cluster": self.cluster.to_json(),
            "clusterPropertySets": (lambda v: [v.to_json() for v in v] if v is not None else v)(self.clusterPropertySets),
            "versionTarget": (lambda v: v.to_json() if v is not None else v)(self.versionTarget)
        }


@dataclasses.dataclass(frozen=True)
class TableCachingJob:
    """Details of a table caching job.
    
    Args:
        id (TableCachingJobId): A data field.
        name (TableCachingJobName): A data field.
        description (str): A data field.
        plan (CachingPlan): A data field.
        retainment (typing.Optional[Duration]): A data field.
        prefixURI (str): A data field.
        schedule (Schedule): A data field.
        cluster (ClusterId): A data field.
        clusterPropertySets (typing.List[ClusterPropertySetId]): A data field.
        versionTarget (typing.Optional[VersionTarget]): A data field.
        version (TableCachingJobVersionId): A data field.
    """
    
    id: TableCachingJobId
    name: TableCachingJobName
    description: str
    plan: CachingPlan
    retainment: typing.Optional[Duration]
    prefixURI: str
    schedule: Schedule
    cluster: ClusterId
    clusterPropertySets: typing.List[ClusterPropertySetId]
    versionTarget: typing.Optional[VersionTarget]
    version: TableCachingJobVersionId
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableCachingJob data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "id": TableCachingJobId.json_schema(),
                "name": TableCachingJobName.json_schema(),
                "description": {
                    "type": "string"
                },
                "plan": CachingPlan.json_schema(),
                "retainment": {
                    "oneOf": [
                        {"type": "null"},
                        Duration.json_schema(),
                    ]
                },
                "prefixURI": {
                    "type": "string"
                },
                "schedule": Schedule.json_schema(),
                "cluster": ClusterId.json_schema(),
                "clusterPropertySets": {
                    "type": "array",
                    "item": ClusterPropertySetId.json_schema()
                },
                "versionTarget": {
                    "oneOf": [
                        {"type": "null"},
                        VersionTarget.json_schema(),
                    ]
                },
                "version": TableCachingJobVersionId.json_schema()
            },
            "required": [
                "id",
                "name",
                "description",
                "plan",
                "prefixURI",
                "schedule",
                "cluster",
                "clusterPropertySets",
                "version",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> TableCachingJob:
        """Validate and parse JSON data into an instance of TableCachingJob.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of TableCachingJob.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableCachingJob(
                id=TableCachingJobId.from_json(data["id"]),
                name=TableCachingJobName.from_json(data["name"]),
                description=str(data["description"]),
                plan=CachingPlan.from_json(data["plan"]),
                retainment=(
                    lambda v: Duration.from_json(v) if v is not None else None
                )(
                    data.get("retainment", None)
                ),
                prefixURI=str(data["prefixURI"]),
                schedule=Schedule.from_json(data["schedule"]),
                cluster=ClusterId.from_json(data["cluster"]),
                clusterPropertySets=[ClusterPropertySetId.from_json(v) for v in data["clusterPropertySets"]],
                versionTarget=(
                    lambda v: VersionTarget.from_json(v) if v is not None else None
                )(
                    data.get("versionTarget", None)
                ),
                version=TableCachingJobVersionId.from_json(data["version"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing TableCachingJob",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "id": self.id.to_json(),
            "name": self.name.to_json(),
            "description": str(self.description),
            "plan": self.plan.to_json(),
            "retainment": (lambda v: v.to_json() if v is not None else v)(self.retainment),
            "prefixURI": str(self.prefixURI),
            "schedule": self.schedule.to_json(),
            "cluster": self.cluster.to_json(),
            "clusterPropertySets": [v.to_json() for v in self.clusterPropertySets],
            "versionTarget": (lambda v: v.to_json() if v is not None else v)(self.versionTarget),
            "version": self.version.to_json()
        }


@dataclasses.dataclass(frozen=True)
class TableCachingRunCreationRequest:
    """Request to create a new table caching job run.
    
    Args:
        jobId (TableCachingJobId): A data field.
        jobVersionId (TableCachingJobVersionId): A data field.
        scheduled_start_time (typing.Optional[datetime.datetime]): A data field.
        retryCount (typing.Optional[int]): A data field.
    """
    
    jobId: TableCachingJobId
    jobVersionId: TableCachingJobVersionId
    scheduled_start_time: typing.Optional[datetime.datetime]
    retryCount: typing.Optional[int]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableCachingRunCreationRequest data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "jobId": TableCachingJobId.json_schema(),
                "jobVersionId": TableCachingJobVersionId.json_schema(),
                "scheduled_start_time": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "string", "format": "date-time"},
                    ]
                },
                "retryCount": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "integer"},
                    ]
                }
            },
            "required": [
                "jobId",
                "jobVersionId",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> TableCachingRunCreationRequest:
        """Validate and parse JSON data into an instance of TableCachingRunCreationRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of TableCachingRunCreationRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableCachingRunCreationRequest(
                jobId=TableCachingJobId.from_json(data["jobId"]),
                jobVersionId=TableCachingJobVersionId.from_json(data["jobVersionId"]),
                scheduled_start_time=(
                    lambda v: isodate.parse_datetime(v) if v is not None else None
                )(
                    data.get("scheduled_start_time", None)
                ),
                retryCount=(
                    lambda v: int(v) if v is not None else None
                )(
                    data.get("retryCount", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing TableCachingRunCreationRequest",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "jobId": self.jobId.to_json(),
            "jobVersionId": self.jobVersionId.to_json(),
            "scheduled_start_time": (lambda v: v.strftime('%Y-%m-%dT%H:%M:%S.%f%z') if v is not None else v)(self.scheduled_start_time),
            "retryCount": (lambda v: int(v) if v is not None else v)(self.retryCount)
        }


@dataclasses.dataclass(frozen=True)
class TableCachingRunUpdateRequest:
    """Request to update a table caching job run.
    
    Args:
        status (RunStatus): A data field.
        error (typing.Optional[RunError]): A data field.
    """
    
    status: RunStatus
    error: typing.Optional[RunError]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableCachingRunUpdateRequest data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "status": RunStatus.json_schema(),
                "error": {
                    "oneOf": [
                        {"type": "null"},
                        RunError.json_schema(),
                    ]
                }
            },
            "required": [
                "status",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> TableCachingRunUpdateRequest:
        """Validate and parse JSON data into an instance of TableCachingRunUpdateRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of TableCachingRunUpdateRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableCachingRunUpdateRequest(
                status=RunStatus.from_json(data["status"]),
                error=(
                    lambda v: RunError.from_json(v) if v is not None else None
                )(
                    data.get("error", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing TableCachingRunUpdateRequest",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "status": self.status.to_json(),
            "error": (lambda v: v.to_json() if v is not None else v)(self.error)
        }


@dataclasses.dataclass(frozen=True)
class TableCachingRun:
    """Details of a table caching job run.
    
    Args:
        id (TableCachingRunId): A data field.
        jobId (TableCachingJobId): A data field.
        jobVersionId (TableCachingJobVersionId): A data field.
        scheduled_start_time (typing.Optional[datetime.datetime]): A data field.
        retryCount (typing.Optional[int]): A data field.
        status (RunStatus): A data field.
        error (typing.Optional[RunError]): A data field.
        executionStatistics (typing.Optional[ExecutionStatistics]): A data field.
        created (datetime.datetime): A data field.
    """
    
    id: TableCachingRunId
    jobId: TableCachingJobId
    jobVersionId: TableCachingJobVersionId
    scheduled_start_time: typing.Optional[datetime.datetime]
    retryCount: typing.Optional[int]
    status: RunStatus
    error: typing.Optional[RunError]
    executionStatistics: typing.Optional[ExecutionStatistics]
    created: datetime.datetime
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for TableCachingRun data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "id": TableCachingRunId.json_schema(),
                "jobId": TableCachingJobId.json_schema(),
                "jobVersionId": TableCachingJobVersionId.json_schema(),
                "scheduled_start_time": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "string", "format": "date-time"},
                    ]
                },
                "retryCount": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "integer"},
                    ]
                },
                "status": RunStatus.json_schema(),
                "error": {
                    "oneOf": [
                        {"type": "null"},
                        RunError.json_schema(),
                    ]
                },
                "executionStatistics": {
                    "oneOf": [
                        {"type": "null"},
                        ExecutionStatistics.json_schema(),
                    ]
                },
                "created": {
                    "type": "string",
                    "format": "date-time"
                }
            },
            "required": [
                "id",
                "jobId",
                "jobVersionId",
                "status",
                "created",
            ]
        }
    
    @classmethod
    def from_json(cls, data: dict) -> TableCachingRun:
        """Validate and parse JSON data into an instance of TableCachingRun.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of TableCachingRun.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return TableCachingRun(
                id=TableCachingRunId.from_json(data["id"]),
                jobId=TableCachingJobId.from_json(data["jobId"]),
                jobVersionId=TableCachingJobVersionId.from_json(data["jobVersionId"]),
                scheduled_start_time=(
                    lambda v: isodate.parse_datetime(v) if v is not None else None
                )(
                    data.get("scheduled_start_time", None)
                ),
                retryCount=(
                    lambda v: int(v) if v is not None else None
                )(
                    data.get("retryCount", None)
                ),
                status=RunStatus.from_json(data["status"]),
                error=(
                    lambda v: RunError.from_json(v) if v is not None else None
                )(
                    data.get("error", None)
                ),
                executionStatistics=(
                    lambda v: ExecutionStatistics.from_json(v) if v is not None else None
                )(
                    data.get("executionStatistics", None)
                ),
                created=isodate.parse_datetime(data["created"]),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing TableCachingRun",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "id": self.id.to_json(),
            "jobId": self.jobId.to_json(),
            "jobVersionId": self.jobVersionId.to_json(),
            "scheduled_start_time": (lambda v: v.strftime('%Y-%m-%dT%H:%M:%S.%f%z') if v is not None else v)(self.scheduled_start_time),
            "retryCount": (lambda v: int(v) if v is not None else v)(self.retryCount),
            "status": self.status.to_json(),
            "error": (lambda v: v.to_json() if v is not None else v)(self.error),
            "executionStatistics": (lambda v: v.to_json() if v is not None else v)(self.executionStatistics),
            "created": self.created.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        }
