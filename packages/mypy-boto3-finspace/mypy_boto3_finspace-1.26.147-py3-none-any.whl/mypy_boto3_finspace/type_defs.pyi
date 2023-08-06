"""
Type annotations for finspace service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_finspace/type_defs/)

Usage::

    ```python
    from mypy_boto3_finspace.type_defs import AutoScalingConfigurationTypeDef

    data: AutoScalingConfigurationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ChangesetStatusType,
    ChangeTypeType,
    EnvironmentStatusType,
    ErrorDetailsType,
    FederationModeType,
    KxAzModeType,
    KxClusterStatusType,
    KxClusterTypeType,
    dnsStatusType,
    tgwStatusType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AutoScalingConfigurationTypeDef",
    "CapacityConfigurationTypeDef",
    "ChangeRequestTypeDef",
    "CodeConfigurationTypeDef",
    "FederationParametersTypeDef",
    "SuperuserParametersTypeDef",
    "ResponseMetadataTypeDef",
    "ErrorInfoTypeDef",
    "KxCacheStorageConfigurationTypeDef",
    "KxCommandLineArgumentTypeDef",
    "KxSavedownStorageConfigurationTypeDef",
    "VpcConfigurationTypeDef",
    "CreateKxDatabaseRequestRequestTypeDef",
    "CreateKxEnvironmentRequestRequestTypeDef",
    "CreateKxUserRequestRequestTypeDef",
    "CustomDNSServerTypeDef",
    "DeleteEnvironmentRequestRequestTypeDef",
    "DeleteKxClusterRequestRequestTypeDef",
    "DeleteKxDatabaseRequestRequestTypeDef",
    "DeleteKxEnvironmentRequestRequestTypeDef",
    "DeleteKxUserRequestRequestTypeDef",
    "GetEnvironmentRequestRequestTypeDef",
    "GetKxChangesetRequestRequestTypeDef",
    "GetKxClusterRequestRequestTypeDef",
    "GetKxConnectionStringRequestRequestTypeDef",
    "GetKxDatabaseRequestRequestTypeDef",
    "GetKxEnvironmentRequestRequestTypeDef",
    "TransitGatewayConfigurationTypeDef",
    "GetKxUserRequestRequestTypeDef",
    "KxChangesetListEntryTypeDef",
    "KxClusterTypeDef",
    "KxDatabaseCacheConfigurationTypeDef",
    "KxDatabaseListEntryTypeDef",
    "KxNodeTypeDef",
    "KxUserTypeDef",
    "ListEnvironmentsRequestRequestTypeDef",
    "ListKxChangesetsRequestRequestTypeDef",
    "ListKxClusterNodesRequestRequestTypeDef",
    "ListKxClustersRequestRequestTypeDef",
    "ListKxDatabasesRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListKxEnvironmentsRequestRequestTypeDef",
    "ListKxUsersRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateKxDatabaseRequestRequestTypeDef",
    "UpdateKxEnvironmentRequestRequestTypeDef",
    "UpdateKxUserRequestRequestTypeDef",
    "CreateKxChangesetRequestRequestTypeDef",
    "EnvironmentTypeDef",
    "UpdateEnvironmentRequestRequestTypeDef",
    "CreateEnvironmentRequestRequestTypeDef",
    "CreateEnvironmentResponseTypeDef",
    "CreateKxDatabaseResponseTypeDef",
    "CreateKxEnvironmentResponseTypeDef",
    "CreateKxUserResponseTypeDef",
    "GetKxConnectionStringResponseTypeDef",
    "GetKxDatabaseResponseTypeDef",
    "GetKxUserResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateKxDatabaseResponseTypeDef",
    "UpdateKxUserResponseTypeDef",
    "CreateKxChangesetResponseTypeDef",
    "GetKxChangesetResponseTypeDef",
    "GetKxEnvironmentResponseTypeDef",
    "KxEnvironmentTypeDef",
    "UpdateKxEnvironmentNetworkRequestRequestTypeDef",
    "UpdateKxEnvironmentNetworkResponseTypeDef",
    "UpdateKxEnvironmentResponseTypeDef",
    "ListKxChangesetsResponseTypeDef",
    "ListKxClustersResponseTypeDef",
    "KxDatabaseConfigurationTypeDef",
    "ListKxDatabasesResponseTypeDef",
    "ListKxClusterNodesResponseTypeDef",
    "ListKxUsersResponseTypeDef",
    "ListKxEnvironmentsRequestListKxEnvironmentsPaginateTypeDef",
    "GetEnvironmentResponseTypeDef",
    "ListEnvironmentsResponseTypeDef",
    "UpdateEnvironmentResponseTypeDef",
    "ListKxEnvironmentsResponseTypeDef",
    "CreateKxClusterRequestRequestTypeDef",
    "CreateKxClusterResponseTypeDef",
    "GetKxClusterResponseTypeDef",
    "UpdateKxClusterDatabasesRequestRequestTypeDef",
)

AutoScalingConfigurationTypeDef = TypedDict(
    "AutoScalingConfigurationTypeDef",
    {
        "minNodeCount": int,
        "maxNodeCount": int,
        "autoScalingMetric": Literal["CPU_UTILIZATION_PERCENTAGE"],
        "metricTarget": float,
        "scaleInCooldownSeconds": float,
        "scaleOutCooldownSeconds": float,
    },
    total=False,
)

CapacityConfigurationTypeDef = TypedDict(
    "CapacityConfigurationTypeDef",
    {
        "nodeType": str,
        "nodeCount": int,
    },
    total=False,
)

_RequiredChangeRequestTypeDef = TypedDict(
    "_RequiredChangeRequestTypeDef",
    {
        "changeType": ChangeTypeType,
        "dbPath": str,
    },
)
_OptionalChangeRequestTypeDef = TypedDict(
    "_OptionalChangeRequestTypeDef",
    {
        "s3Path": str,
    },
    total=False,
)

class ChangeRequestTypeDef(_RequiredChangeRequestTypeDef, _OptionalChangeRequestTypeDef):
    pass

CodeConfigurationTypeDef = TypedDict(
    "CodeConfigurationTypeDef",
    {
        "s3Bucket": str,
        "s3Key": str,
        "s3ObjectVersion": str,
    },
    total=False,
)

FederationParametersTypeDef = TypedDict(
    "FederationParametersTypeDef",
    {
        "samlMetadataDocument": str,
        "samlMetadataURL": str,
        "applicationCallBackURL": str,
        "federationURN": str,
        "federationProviderName": str,
        "attributeMap": Mapping[str, str],
    },
    total=False,
)

SuperuserParametersTypeDef = TypedDict(
    "SuperuserParametersTypeDef",
    {
        "emailAddress": str,
        "firstName": str,
        "lastName": str,
    },
)

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

ErrorInfoTypeDef = TypedDict(
    "ErrorInfoTypeDef",
    {
        "errorMessage": str,
        "errorType": ErrorDetailsType,
    },
    total=False,
)

KxCacheStorageConfigurationTypeDef = TypedDict(
    "KxCacheStorageConfigurationTypeDef",
    {
        "type": str,
        "size": int,
    },
)

KxCommandLineArgumentTypeDef = TypedDict(
    "KxCommandLineArgumentTypeDef",
    {
        "key": str,
        "value": str,
    },
    total=False,
)

KxSavedownStorageConfigurationTypeDef = TypedDict(
    "KxSavedownStorageConfigurationTypeDef",
    {
        "type": Literal["SDS01"],
        "size": int,
    },
)

VpcConfigurationTypeDef = TypedDict(
    "VpcConfigurationTypeDef",
    {
        "vpcId": str,
        "securityGroupIds": Sequence[str],
        "subnetIds": Sequence[str],
        "ipAddressType": Literal["IP_V4"],
    },
    total=False,
)

_RequiredCreateKxDatabaseRequestRequestTypeDef = TypedDict(
    "_RequiredCreateKxDatabaseRequestRequestTypeDef",
    {
        "environmentId": str,
        "databaseName": str,
        "clientToken": str,
    },
)
_OptionalCreateKxDatabaseRequestRequestTypeDef = TypedDict(
    "_OptionalCreateKxDatabaseRequestRequestTypeDef",
    {
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateKxDatabaseRequestRequestTypeDef(
    _RequiredCreateKxDatabaseRequestRequestTypeDef, _OptionalCreateKxDatabaseRequestRequestTypeDef
):
    pass

_RequiredCreateKxEnvironmentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateKxEnvironmentRequestRequestTypeDef",
    {
        "name": str,
        "kmsKeyId": str,
    },
)
_OptionalCreateKxEnvironmentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateKxEnvironmentRequestRequestTypeDef",
    {
        "description": str,
        "tags": Mapping[str, str],
        "clientToken": str,
    },
    total=False,
)

class CreateKxEnvironmentRequestRequestTypeDef(
    _RequiredCreateKxEnvironmentRequestRequestTypeDef,
    _OptionalCreateKxEnvironmentRequestRequestTypeDef,
):
    pass

_RequiredCreateKxUserRequestRequestTypeDef = TypedDict(
    "_RequiredCreateKxUserRequestRequestTypeDef",
    {
        "environmentId": str,
        "userName": str,
        "iamRole": str,
    },
)
_OptionalCreateKxUserRequestRequestTypeDef = TypedDict(
    "_OptionalCreateKxUserRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
        "clientToken": str,
    },
    total=False,
)

class CreateKxUserRequestRequestTypeDef(
    _RequiredCreateKxUserRequestRequestTypeDef, _OptionalCreateKxUserRequestRequestTypeDef
):
    pass

CustomDNSServerTypeDef = TypedDict(
    "CustomDNSServerTypeDef",
    {
        "customDNSServerName": str,
        "customDNSServerIP": str,
    },
)

DeleteEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)

_RequiredDeleteKxClusterRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteKxClusterRequestRequestTypeDef",
    {
        "environmentId": str,
        "clusterName": str,
    },
)
_OptionalDeleteKxClusterRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteKxClusterRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)

class DeleteKxClusterRequestRequestTypeDef(
    _RequiredDeleteKxClusterRequestRequestTypeDef, _OptionalDeleteKxClusterRequestRequestTypeDef
):
    pass

DeleteKxDatabaseRequestRequestTypeDef = TypedDict(
    "DeleteKxDatabaseRequestRequestTypeDef",
    {
        "environmentId": str,
        "databaseName": str,
        "clientToken": str,
    },
)

DeleteKxEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteKxEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)

DeleteKxUserRequestRequestTypeDef = TypedDict(
    "DeleteKxUserRequestRequestTypeDef",
    {
        "userName": str,
        "environmentId": str,
    },
)

GetEnvironmentRequestRequestTypeDef = TypedDict(
    "GetEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)

GetKxChangesetRequestRequestTypeDef = TypedDict(
    "GetKxChangesetRequestRequestTypeDef",
    {
        "environmentId": str,
        "databaseName": str,
        "changesetId": str,
    },
)

GetKxClusterRequestRequestTypeDef = TypedDict(
    "GetKxClusterRequestRequestTypeDef",
    {
        "environmentId": str,
        "clusterName": str,
    },
)

GetKxConnectionStringRequestRequestTypeDef = TypedDict(
    "GetKxConnectionStringRequestRequestTypeDef",
    {
        "userArn": str,
        "environmentId": str,
        "clusterName": str,
    },
)

GetKxDatabaseRequestRequestTypeDef = TypedDict(
    "GetKxDatabaseRequestRequestTypeDef",
    {
        "environmentId": str,
        "databaseName": str,
    },
)

GetKxEnvironmentRequestRequestTypeDef = TypedDict(
    "GetKxEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)

TransitGatewayConfigurationTypeDef = TypedDict(
    "TransitGatewayConfigurationTypeDef",
    {
        "transitGatewayID": str,
        "routableCIDRSpace": str,
    },
)

GetKxUserRequestRequestTypeDef = TypedDict(
    "GetKxUserRequestRequestTypeDef",
    {
        "userName": str,
        "environmentId": str,
    },
)

KxChangesetListEntryTypeDef = TypedDict(
    "KxChangesetListEntryTypeDef",
    {
        "changesetId": str,
        "createdTimestamp": datetime,
        "activeFromTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
        "status": ChangesetStatusType,
    },
    total=False,
)

KxClusterTypeDef = TypedDict(
    "KxClusterTypeDef",
    {
        "status": KxClusterStatusType,
        "statusReason": str,
        "clusterName": str,
        "clusterType": KxClusterTypeType,
        "clusterDescription": str,
        "releaseLabel": str,
        "initializationScript": str,
        "executionRole": str,
        "azMode": KxAzModeType,
        "availabilityZoneId": str,
        "lastModifiedTimestamp": datetime,
        "createdTimestamp": datetime,
    },
    total=False,
)

KxDatabaseCacheConfigurationTypeDef = TypedDict(
    "KxDatabaseCacheConfigurationTypeDef",
    {
        "cacheType": str,
        "dbPaths": Sequence[str],
    },
)

KxDatabaseListEntryTypeDef = TypedDict(
    "KxDatabaseListEntryTypeDef",
    {
        "databaseName": str,
        "createdTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
    },
    total=False,
)

KxNodeTypeDef = TypedDict(
    "KxNodeTypeDef",
    {
        "nodeId": str,
        "availabilityZoneId": str,
        "launchTime": datetime,
    },
    total=False,
)

KxUserTypeDef = TypedDict(
    "KxUserTypeDef",
    {
        "userArn": str,
        "userName": str,
        "iamRole": str,
        "createTimestamp": datetime,
        "updateTimestamp": datetime,
    },
    total=False,
)

ListEnvironmentsRequestRequestTypeDef = TypedDict(
    "ListEnvironmentsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredListKxChangesetsRequestRequestTypeDef = TypedDict(
    "_RequiredListKxChangesetsRequestRequestTypeDef",
    {
        "environmentId": str,
        "databaseName": str,
    },
)
_OptionalListKxChangesetsRequestRequestTypeDef = TypedDict(
    "_OptionalListKxChangesetsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListKxChangesetsRequestRequestTypeDef(
    _RequiredListKxChangesetsRequestRequestTypeDef, _OptionalListKxChangesetsRequestRequestTypeDef
):
    pass

_RequiredListKxClusterNodesRequestRequestTypeDef = TypedDict(
    "_RequiredListKxClusterNodesRequestRequestTypeDef",
    {
        "environmentId": str,
        "clusterName": str,
    },
)
_OptionalListKxClusterNodesRequestRequestTypeDef = TypedDict(
    "_OptionalListKxClusterNodesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListKxClusterNodesRequestRequestTypeDef(
    _RequiredListKxClusterNodesRequestRequestTypeDef,
    _OptionalListKxClusterNodesRequestRequestTypeDef,
):
    pass

_RequiredListKxClustersRequestRequestTypeDef = TypedDict(
    "_RequiredListKxClustersRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)
_OptionalListKxClustersRequestRequestTypeDef = TypedDict(
    "_OptionalListKxClustersRequestRequestTypeDef",
    {
        "clusterType": KxClusterTypeType,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListKxClustersRequestRequestTypeDef(
    _RequiredListKxClustersRequestRequestTypeDef, _OptionalListKxClustersRequestRequestTypeDef
):
    pass

_RequiredListKxDatabasesRequestRequestTypeDef = TypedDict(
    "_RequiredListKxDatabasesRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)
_OptionalListKxDatabasesRequestRequestTypeDef = TypedDict(
    "_OptionalListKxDatabasesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListKxDatabasesRequestRequestTypeDef(
    _RequiredListKxDatabasesRequestRequestTypeDef, _OptionalListKxDatabasesRequestRequestTypeDef
):
    pass

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ListKxEnvironmentsRequestRequestTypeDef = TypedDict(
    "ListKxEnvironmentsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredListKxUsersRequestRequestTypeDef = TypedDict(
    "_RequiredListKxUsersRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)
_OptionalListKxUsersRequestRequestTypeDef = TypedDict(
    "_OptionalListKxUsersRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListKxUsersRequestRequestTypeDef(
    _RequiredListKxUsersRequestRequestTypeDef, _OptionalListKxUsersRequestRequestTypeDef
):
    pass

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateKxDatabaseRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateKxDatabaseRequestRequestTypeDef",
    {
        "environmentId": str,
        "databaseName": str,
        "clientToken": str,
    },
)
_OptionalUpdateKxDatabaseRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateKxDatabaseRequestRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)

class UpdateKxDatabaseRequestRequestTypeDef(
    _RequiredUpdateKxDatabaseRequestRequestTypeDef, _OptionalUpdateKxDatabaseRequestRequestTypeDef
):
    pass

_RequiredUpdateKxEnvironmentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateKxEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)
_OptionalUpdateKxEnvironmentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateKxEnvironmentRequestRequestTypeDef",
    {
        "name": str,
        "description": str,
        "clientToken": str,
    },
    total=False,
)

class UpdateKxEnvironmentRequestRequestTypeDef(
    _RequiredUpdateKxEnvironmentRequestRequestTypeDef,
    _OptionalUpdateKxEnvironmentRequestRequestTypeDef,
):
    pass

_RequiredUpdateKxUserRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateKxUserRequestRequestTypeDef",
    {
        "environmentId": str,
        "userName": str,
        "iamRole": str,
    },
)
_OptionalUpdateKxUserRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateKxUserRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)

class UpdateKxUserRequestRequestTypeDef(
    _RequiredUpdateKxUserRequestRequestTypeDef, _OptionalUpdateKxUserRequestRequestTypeDef
):
    pass

CreateKxChangesetRequestRequestTypeDef = TypedDict(
    "CreateKxChangesetRequestRequestTypeDef",
    {
        "environmentId": str,
        "databaseName": str,
        "changeRequests": Sequence[ChangeRequestTypeDef],
        "clientToken": str,
    },
)

EnvironmentTypeDef = TypedDict(
    "EnvironmentTypeDef",
    {
        "name": str,
        "environmentId": str,
        "awsAccountId": str,
        "status": EnvironmentStatusType,
        "environmentUrl": str,
        "description": str,
        "environmentArn": str,
        "sageMakerStudioDomainUrl": str,
        "kmsKeyId": str,
        "dedicatedServiceAccountId": str,
        "federationMode": FederationModeType,
        "federationParameters": FederationParametersTypeDef,
    },
    total=False,
)

_RequiredUpdateEnvironmentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)
_OptionalUpdateEnvironmentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateEnvironmentRequestRequestTypeDef",
    {
        "name": str,
        "description": str,
        "federationMode": FederationModeType,
        "federationParameters": FederationParametersTypeDef,
    },
    total=False,
)

class UpdateEnvironmentRequestRequestTypeDef(
    _RequiredUpdateEnvironmentRequestRequestTypeDef, _OptionalUpdateEnvironmentRequestRequestTypeDef
):
    pass

_RequiredCreateEnvironmentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateEnvironmentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentRequestRequestTypeDef",
    {
        "description": str,
        "kmsKeyId": str,
        "tags": Mapping[str, str],
        "federationMode": FederationModeType,
        "federationParameters": FederationParametersTypeDef,
        "superuserParameters": SuperuserParametersTypeDef,
        "dataBundles": Sequence[str],
    },
    total=False,
)

class CreateEnvironmentRequestRequestTypeDef(
    _RequiredCreateEnvironmentRequestRequestTypeDef, _OptionalCreateEnvironmentRequestRequestTypeDef
):
    pass

CreateEnvironmentResponseTypeDef = TypedDict(
    "CreateEnvironmentResponseTypeDef",
    {
        "environmentId": str,
        "environmentArn": str,
        "environmentUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateKxDatabaseResponseTypeDef = TypedDict(
    "CreateKxDatabaseResponseTypeDef",
    {
        "databaseName": str,
        "databaseArn": str,
        "environmentId": str,
        "description": str,
        "createdTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateKxEnvironmentResponseTypeDef = TypedDict(
    "CreateKxEnvironmentResponseTypeDef",
    {
        "name": str,
        "status": EnvironmentStatusType,
        "environmentId": str,
        "description": str,
        "environmentArn": str,
        "kmsKeyId": str,
        "creationTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateKxUserResponseTypeDef = TypedDict(
    "CreateKxUserResponseTypeDef",
    {
        "userName": str,
        "userArn": str,
        "environmentId": str,
        "iamRole": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetKxConnectionStringResponseTypeDef = TypedDict(
    "GetKxConnectionStringResponseTypeDef",
    {
        "signedConnectionString": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetKxDatabaseResponseTypeDef = TypedDict(
    "GetKxDatabaseResponseTypeDef",
    {
        "databaseName": str,
        "databaseArn": str,
        "environmentId": str,
        "description": str,
        "createdTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
        "lastCompletedChangesetId": str,
        "numBytes": int,
        "numChangesets": int,
        "numFiles": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetKxUserResponseTypeDef = TypedDict(
    "GetKxUserResponseTypeDef",
    {
        "userName": str,
        "userArn": str,
        "environmentId": str,
        "iamRole": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateKxDatabaseResponseTypeDef = TypedDict(
    "UpdateKxDatabaseResponseTypeDef",
    {
        "databaseName": str,
        "environmentId": str,
        "description": str,
        "lastModifiedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateKxUserResponseTypeDef = TypedDict(
    "UpdateKxUserResponseTypeDef",
    {
        "userName": str,
        "userArn": str,
        "environmentId": str,
        "iamRole": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateKxChangesetResponseTypeDef = TypedDict(
    "CreateKxChangesetResponseTypeDef",
    {
        "changesetId": str,
        "databaseName": str,
        "environmentId": str,
        "changeRequests": List[ChangeRequestTypeDef],
        "createdTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
        "status": ChangesetStatusType,
        "errorInfo": ErrorInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetKxChangesetResponseTypeDef = TypedDict(
    "GetKxChangesetResponseTypeDef",
    {
        "changesetId": str,
        "databaseName": str,
        "environmentId": str,
        "changeRequests": List[ChangeRequestTypeDef],
        "createdTimestamp": datetime,
        "activeFromTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
        "status": ChangesetStatusType,
        "errorInfo": ErrorInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetKxEnvironmentResponseTypeDef = TypedDict(
    "GetKxEnvironmentResponseTypeDef",
    {
        "name": str,
        "environmentId": str,
        "awsAccountId": str,
        "status": EnvironmentStatusType,
        "tgwStatus": tgwStatusType,
        "dnsStatus": dnsStatusType,
        "errorMessage": str,
        "description": str,
        "environmentArn": str,
        "kmsKeyId": str,
        "dedicatedServiceAccountId": str,
        "transitGatewayConfiguration": TransitGatewayConfigurationTypeDef,
        "customDNSConfiguration": List[CustomDNSServerTypeDef],
        "creationTimestamp": datetime,
        "updateTimestamp": datetime,
        "availabilityZoneIds": List[str],
        "certificateAuthorityArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

KxEnvironmentTypeDef = TypedDict(
    "KxEnvironmentTypeDef",
    {
        "name": str,
        "environmentId": str,
        "awsAccountId": str,
        "status": EnvironmentStatusType,
        "tgwStatus": tgwStatusType,
        "dnsStatus": dnsStatusType,
        "errorMessage": str,
        "description": str,
        "environmentArn": str,
        "kmsKeyId": str,
        "dedicatedServiceAccountId": str,
        "transitGatewayConfiguration": TransitGatewayConfigurationTypeDef,
        "customDNSConfiguration": List[CustomDNSServerTypeDef],
        "creationTimestamp": datetime,
        "updateTimestamp": datetime,
        "availabilityZoneIds": List[str],
        "certificateAuthorityArn": str,
    },
    total=False,
)

_RequiredUpdateKxEnvironmentNetworkRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateKxEnvironmentNetworkRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)
_OptionalUpdateKxEnvironmentNetworkRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateKxEnvironmentNetworkRequestRequestTypeDef",
    {
        "transitGatewayConfiguration": TransitGatewayConfigurationTypeDef,
        "customDNSConfiguration": Sequence[CustomDNSServerTypeDef],
        "clientToken": str,
    },
    total=False,
)

class UpdateKxEnvironmentNetworkRequestRequestTypeDef(
    _RequiredUpdateKxEnvironmentNetworkRequestRequestTypeDef,
    _OptionalUpdateKxEnvironmentNetworkRequestRequestTypeDef,
):
    pass

UpdateKxEnvironmentNetworkResponseTypeDef = TypedDict(
    "UpdateKxEnvironmentNetworkResponseTypeDef",
    {
        "name": str,
        "environmentId": str,
        "awsAccountId": str,
        "status": EnvironmentStatusType,
        "tgwStatus": tgwStatusType,
        "dnsStatus": dnsStatusType,
        "errorMessage": str,
        "description": str,
        "environmentArn": str,
        "kmsKeyId": str,
        "dedicatedServiceAccountId": str,
        "transitGatewayConfiguration": TransitGatewayConfigurationTypeDef,
        "customDNSConfiguration": List[CustomDNSServerTypeDef],
        "creationTimestamp": datetime,
        "updateTimestamp": datetime,
        "availabilityZoneIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateKxEnvironmentResponseTypeDef = TypedDict(
    "UpdateKxEnvironmentResponseTypeDef",
    {
        "name": str,
        "environmentId": str,
        "awsAccountId": str,
        "status": EnvironmentStatusType,
        "tgwStatus": tgwStatusType,
        "dnsStatus": dnsStatusType,
        "errorMessage": str,
        "description": str,
        "environmentArn": str,
        "kmsKeyId": str,
        "dedicatedServiceAccountId": str,
        "transitGatewayConfiguration": TransitGatewayConfigurationTypeDef,
        "customDNSConfiguration": List[CustomDNSServerTypeDef],
        "creationTimestamp": datetime,
        "updateTimestamp": datetime,
        "availabilityZoneIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKxChangesetsResponseTypeDef = TypedDict(
    "ListKxChangesetsResponseTypeDef",
    {
        "kxChangesets": List[KxChangesetListEntryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKxClustersResponseTypeDef = TypedDict(
    "ListKxClustersResponseTypeDef",
    {
        "kxClusterSummaries": List[KxClusterTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredKxDatabaseConfigurationTypeDef = TypedDict(
    "_RequiredKxDatabaseConfigurationTypeDef",
    {
        "databaseName": str,
    },
)
_OptionalKxDatabaseConfigurationTypeDef = TypedDict(
    "_OptionalKxDatabaseConfigurationTypeDef",
    {
        "cacheConfigurations": Sequence[KxDatabaseCacheConfigurationTypeDef],
        "changesetId": str,
    },
    total=False,
)

class KxDatabaseConfigurationTypeDef(
    _RequiredKxDatabaseConfigurationTypeDef, _OptionalKxDatabaseConfigurationTypeDef
):
    pass

ListKxDatabasesResponseTypeDef = TypedDict(
    "ListKxDatabasesResponseTypeDef",
    {
        "kxDatabases": List[KxDatabaseListEntryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKxClusterNodesResponseTypeDef = TypedDict(
    "ListKxClusterNodesResponseTypeDef",
    {
        "nodes": List[KxNodeTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKxUsersResponseTypeDef = TypedDict(
    "ListKxUsersResponseTypeDef",
    {
        "users": List[KxUserTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKxEnvironmentsRequestListKxEnvironmentsPaginateTypeDef = TypedDict(
    "ListKxEnvironmentsRequestListKxEnvironmentsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetEnvironmentResponseTypeDef = TypedDict(
    "GetEnvironmentResponseTypeDef",
    {
        "environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEnvironmentsResponseTypeDef = TypedDict(
    "ListEnvironmentsResponseTypeDef",
    {
        "environments": List[EnvironmentTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEnvironmentResponseTypeDef = TypedDict(
    "UpdateEnvironmentResponseTypeDef",
    {
        "environment": EnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListKxEnvironmentsResponseTypeDef = TypedDict(
    "ListKxEnvironmentsResponseTypeDef",
    {
        "environments": List[KxEnvironmentTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateKxClusterRequestRequestTypeDef = TypedDict(
    "_RequiredCreateKxClusterRequestRequestTypeDef",
    {
        "environmentId": str,
        "clusterName": str,
        "clusterType": KxClusterTypeType,
        "capacityConfiguration": CapacityConfigurationTypeDef,
        "releaseLabel": str,
        "azMode": KxAzModeType,
    },
)
_OptionalCreateKxClusterRequestRequestTypeDef = TypedDict(
    "_OptionalCreateKxClusterRequestRequestTypeDef",
    {
        "clientToken": str,
        "databases": Sequence[KxDatabaseConfigurationTypeDef],
        "cacheStorageConfigurations": Sequence[KxCacheStorageConfigurationTypeDef],
        "autoScalingConfiguration": AutoScalingConfigurationTypeDef,
        "clusterDescription": str,
        "vpcConfiguration": VpcConfigurationTypeDef,
        "initializationScript": str,
        "commandLineArguments": Sequence[KxCommandLineArgumentTypeDef],
        "code": CodeConfigurationTypeDef,
        "executionRole": str,
        "savedownStorageConfiguration": KxSavedownStorageConfigurationTypeDef,
        "availabilityZoneId": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateKxClusterRequestRequestTypeDef(
    _RequiredCreateKxClusterRequestRequestTypeDef, _OptionalCreateKxClusterRequestRequestTypeDef
):
    pass

CreateKxClusterResponseTypeDef = TypedDict(
    "CreateKxClusterResponseTypeDef",
    {
        "environmentId": str,
        "status": KxClusterStatusType,
        "statusReason": str,
        "clusterName": str,
        "clusterType": KxClusterTypeType,
        "databases": List[KxDatabaseConfigurationTypeDef],
        "cacheStorageConfigurations": List[KxCacheStorageConfigurationTypeDef],
        "autoScalingConfiguration": AutoScalingConfigurationTypeDef,
        "clusterDescription": str,
        "capacityConfiguration": CapacityConfigurationTypeDef,
        "releaseLabel": str,
        "vpcConfiguration": VpcConfigurationTypeDef,
        "initializationScript": str,
        "commandLineArguments": List[KxCommandLineArgumentTypeDef],
        "code": CodeConfigurationTypeDef,
        "executionRole": str,
        "lastModifiedTimestamp": datetime,
        "savedownStorageConfiguration": KxSavedownStorageConfigurationTypeDef,
        "azMode": KxAzModeType,
        "availabilityZoneId": str,
        "createdTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetKxClusterResponseTypeDef = TypedDict(
    "GetKxClusterResponseTypeDef",
    {
        "status": KxClusterStatusType,
        "statusReason": str,
        "clusterName": str,
        "clusterType": KxClusterTypeType,
        "databases": List[KxDatabaseConfigurationTypeDef],
        "cacheStorageConfigurations": List[KxCacheStorageConfigurationTypeDef],
        "autoScalingConfiguration": AutoScalingConfigurationTypeDef,
        "clusterDescription": str,
        "capacityConfiguration": CapacityConfigurationTypeDef,
        "releaseLabel": str,
        "vpcConfiguration": VpcConfigurationTypeDef,
        "initializationScript": str,
        "commandLineArguments": List[KxCommandLineArgumentTypeDef],
        "code": CodeConfigurationTypeDef,
        "executionRole": str,
        "lastModifiedTimestamp": datetime,
        "savedownStorageConfiguration": KxSavedownStorageConfigurationTypeDef,
        "azMode": KxAzModeType,
        "availabilityZoneId": str,
        "createdTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateKxClusterDatabasesRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateKxClusterDatabasesRequestRequestTypeDef",
    {
        "environmentId": str,
        "clusterName": str,
        "databases": Sequence[KxDatabaseConfigurationTypeDef],
    },
)
_OptionalUpdateKxClusterDatabasesRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateKxClusterDatabasesRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)

class UpdateKxClusterDatabasesRequestRequestTypeDef(
    _RequiredUpdateKxClusterDatabasesRequestRequestTypeDef,
    _OptionalUpdateKxClusterDatabasesRequestRequestTypeDef,
):
    pass
