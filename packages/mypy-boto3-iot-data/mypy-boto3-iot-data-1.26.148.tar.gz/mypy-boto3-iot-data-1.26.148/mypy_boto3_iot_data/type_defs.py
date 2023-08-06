"""
Type annotations for iot-data service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/type_defs/)

Usage::

    ```python
    from mypy_boto3_iot_data.type_defs import DeleteThingShadowRequestRequestTypeDef

    data: DeleteThingShadowRequestRequestTypeDef = {...}
    ```
"""
import sys
from typing import IO, Any, Dict, List, Union

from botocore.response import StreamingBody

from .literals import PayloadFormatIndicatorType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "DeleteThingShadowRequestRequestTypeDef",
    "DeleteThingShadowResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetRetainedMessageRequestRequestTypeDef",
    "GetRetainedMessageResponseTypeDef",
    "GetThingShadowRequestRequestTypeDef",
    "GetThingShadowResponseTypeDef",
    "ListNamedShadowsForThingRequestRequestTypeDef",
    "ListNamedShadowsForThingResponseTypeDef",
    "ListRetainedMessagesRequestListRetainedMessagesPaginateTypeDef",
    "ListRetainedMessagesRequestRequestTypeDef",
    "RetainedMessageSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "PublishRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "UpdateThingShadowRequestRequestTypeDef",
    "UpdateThingShadowResponseTypeDef",
    "ListRetainedMessagesResponseTypeDef",
)

_RequiredDeleteThingShadowRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteThingShadowRequestRequestTypeDef",
    {
        "thingName": str,
    },
)
_OptionalDeleteThingShadowRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteThingShadowRequestRequestTypeDef",
    {
        "shadowName": str,
    },
    total=False,
)


class DeleteThingShadowRequestRequestTypeDef(
    _RequiredDeleteThingShadowRequestRequestTypeDef, _OptionalDeleteThingShadowRequestRequestTypeDef
):
    pass


DeleteThingShadowResponseTypeDef = TypedDict(
    "DeleteThingShadowResponseTypeDef",
    {
        "payload": StreamingBody,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetRetainedMessageRequestRequestTypeDef = TypedDict(
    "GetRetainedMessageRequestRequestTypeDef",
    {
        "topic": str,
    },
)

GetRetainedMessageResponseTypeDef = TypedDict(
    "GetRetainedMessageResponseTypeDef",
    {
        "topic": str,
        "payload": bytes,
        "qos": int,
        "lastModifiedTime": int,
        "userProperties": bytes,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetThingShadowRequestRequestTypeDef = TypedDict(
    "_RequiredGetThingShadowRequestRequestTypeDef",
    {
        "thingName": str,
    },
)
_OptionalGetThingShadowRequestRequestTypeDef = TypedDict(
    "_OptionalGetThingShadowRequestRequestTypeDef",
    {
        "shadowName": str,
    },
    total=False,
)


class GetThingShadowRequestRequestTypeDef(
    _RequiredGetThingShadowRequestRequestTypeDef, _OptionalGetThingShadowRequestRequestTypeDef
):
    pass


GetThingShadowResponseTypeDef = TypedDict(
    "GetThingShadowResponseTypeDef",
    {
        "payload": StreamingBody,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListNamedShadowsForThingRequestRequestTypeDef = TypedDict(
    "_RequiredListNamedShadowsForThingRequestRequestTypeDef",
    {
        "thingName": str,
    },
)
_OptionalListNamedShadowsForThingRequestRequestTypeDef = TypedDict(
    "_OptionalListNamedShadowsForThingRequestRequestTypeDef",
    {
        "nextToken": str,
        "pageSize": int,
    },
    total=False,
)


class ListNamedShadowsForThingRequestRequestTypeDef(
    _RequiredListNamedShadowsForThingRequestRequestTypeDef,
    _OptionalListNamedShadowsForThingRequestRequestTypeDef,
):
    pass


ListNamedShadowsForThingResponseTypeDef = TypedDict(
    "ListNamedShadowsForThingResponseTypeDef",
    {
        "results": List[str],
        "nextToken": str,
        "timestamp": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListRetainedMessagesRequestListRetainedMessagesPaginateTypeDef = TypedDict(
    "ListRetainedMessagesRequestListRetainedMessagesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListRetainedMessagesRequestRequestTypeDef = TypedDict(
    "ListRetainedMessagesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

RetainedMessageSummaryTypeDef = TypedDict(
    "RetainedMessageSummaryTypeDef",
    {
        "topic": str,
        "payloadSize": int,
        "qos": int,
        "lastModifiedTime": int,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredPublishRequestRequestTypeDef = TypedDict(
    "_RequiredPublishRequestRequestTypeDef",
    {
        "topic": str,
    },
)
_OptionalPublishRequestRequestTypeDef = TypedDict(
    "_OptionalPublishRequestRequestTypeDef",
    {
        "qos": int,
        "retain": bool,
        "payload": Union[str, bytes, IO[Any], StreamingBody],
        "userProperties": str,
        "payloadFormatIndicator": PayloadFormatIndicatorType,
        "contentType": str,
        "responseTopic": str,
        "correlationData": str,
        "messageExpiry": int,
    },
    total=False,
)


class PublishRequestRequestTypeDef(
    _RequiredPublishRequestRequestTypeDef, _OptionalPublishRequestRequestTypeDef
):
    pass


ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

_RequiredUpdateThingShadowRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateThingShadowRequestRequestTypeDef",
    {
        "thingName": str,
        "payload": Union[str, bytes, IO[Any], StreamingBody],
    },
)
_OptionalUpdateThingShadowRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateThingShadowRequestRequestTypeDef",
    {
        "shadowName": str,
    },
    total=False,
)


class UpdateThingShadowRequestRequestTypeDef(
    _RequiredUpdateThingShadowRequestRequestTypeDef, _OptionalUpdateThingShadowRequestRequestTypeDef
):
    pass


UpdateThingShadowResponseTypeDef = TypedDict(
    "UpdateThingShadowResponseTypeDef",
    {
        "payload": StreamingBody,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListRetainedMessagesResponseTypeDef = TypedDict(
    "ListRetainedMessagesResponseTypeDef",
    {
        "retainedTopics": List[RetainedMessageSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
