from . import sort_direction_pb2 as _sort_direction_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
PARTITION_RAW_FIELD_ID: PartitionRawField
PARTITION_RAW_FIELD_PARENT_PARTITION_IDS: PartitionRawField
PARTITION_RAW_FIELD_POD_MAX: PartitionRawField
PARTITION_RAW_FIELD_POD_RESERVED: PartitionRawField
PARTITION_RAW_FIELD_PREEMPTION_PERCENTAGE: PartitionRawField
PARTITION_RAW_FIELD_PRIORITY: PartitionRawField
PARTITION_RAW_FIELD_UNSPECIFIED: PartitionRawField

class GetPartitionRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetPartitionResponse(_message.Message):
    __slots__ = ["partition"]
    PARTITION_FIELD_NUMBER: _ClassVar[int]
    partition: PartitionRaw
    def __init__(self, partition: _Optional[_Union[PartitionRaw, _Mapping]] = ...) -> None: ...

class ListPartitionsRequest(_message.Message):
    __slots__ = ["filter", "page", "page_size", "sort"]
    class Filter(_message.Message):
        __slots__ = ["id", "parent_partition_id", "pod_max", "pod_reserved", "preemption_percentage", "priority"]
        ID_FIELD_NUMBER: _ClassVar[int]
        PARENT_PARTITION_ID_FIELD_NUMBER: _ClassVar[int]
        POD_MAX_FIELD_NUMBER: _ClassVar[int]
        POD_RESERVED_FIELD_NUMBER: _ClassVar[int]
        PREEMPTION_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
        PRIORITY_FIELD_NUMBER: _ClassVar[int]
        id: str
        parent_partition_id: str
        pod_max: int
        pod_reserved: int
        preemption_percentage: int
        priority: int
        def __init__(self, id: _Optional[str] = ..., parent_partition_id: _Optional[str] = ..., pod_reserved: _Optional[int] = ..., pod_max: _Optional[int] = ..., preemption_percentage: _Optional[int] = ..., priority: _Optional[int] = ...) -> None: ...
    class Sort(_message.Message):
        __slots__ = ["direction", "field"]
        DIRECTION_FIELD_NUMBER: _ClassVar[int]
        FIELD_FIELD_NUMBER: _ClassVar[int]
        direction: _sort_direction_pb2.SortDirection
        field: PartitionField
        def __init__(self, field: _Optional[_Union[PartitionField, _Mapping]] = ..., direction: _Optional[_Union[_sort_direction_pb2.SortDirection, str]] = ...) -> None: ...
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    filter: ListPartitionsRequest.Filter
    page: int
    page_size: int
    sort: ListPartitionsRequest.Sort
    def __init__(self, page: _Optional[int] = ..., page_size: _Optional[int] = ..., filter: _Optional[_Union[ListPartitionsRequest.Filter, _Mapping]] = ..., sort: _Optional[_Union[ListPartitionsRequest.Sort, _Mapping]] = ...) -> None: ...

class ListPartitionsResponse(_message.Message):
    __slots__ = ["page", "page_size", "partitions", "total"]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PARTITIONS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    page: int
    page_size: int
    partitions: _containers.RepeatedCompositeFieldContainer[PartitionRaw]
    total: int
    def __init__(self, partitions: _Optional[_Iterable[_Union[PartitionRaw, _Mapping]]] = ..., page: _Optional[int] = ..., page_size: _Optional[int] = ..., total: _Optional[int] = ...) -> None: ...

class PartitionField(_message.Message):
    __slots__ = ["partition_raw_field"]
    PARTITION_RAW_FIELD_FIELD_NUMBER: _ClassVar[int]
    partition_raw_field: PartitionRawField
    def __init__(self, partition_raw_field: _Optional[_Union[PartitionRawField, str]] = ...) -> None: ...

class PartitionRaw(_message.Message):
    __slots__ = ["id", "parent_partition_ids", "pod_configuration", "pod_max", "pod_reserved", "preemption_percentage", "priority"]
    class PodConfigurationEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_PARTITION_IDS_FIELD_NUMBER: _ClassVar[int]
    POD_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    POD_MAX_FIELD_NUMBER: _ClassVar[int]
    POD_RESERVED_FIELD_NUMBER: _ClassVar[int]
    PREEMPTION_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    id: str
    parent_partition_ids: _containers.RepeatedScalarFieldContainer[str]
    pod_configuration: _containers.ScalarMap[str, str]
    pod_max: int
    pod_reserved: int
    preemption_percentage: int
    priority: int
    def __init__(self, id: _Optional[str] = ..., parent_partition_ids: _Optional[_Iterable[str]] = ..., pod_reserved: _Optional[int] = ..., pod_max: _Optional[int] = ..., pod_configuration: _Optional[_Mapping[str, str]] = ..., preemption_percentage: _Optional[int] = ..., priority: _Optional[int] = ...) -> None: ...

class PartitionRawField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
