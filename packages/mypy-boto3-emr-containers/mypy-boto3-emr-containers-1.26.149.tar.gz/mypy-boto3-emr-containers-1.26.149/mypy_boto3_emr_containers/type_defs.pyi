"""
Type annotations for emr-containers service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/type_defs/)

Usage::

    ```python
    from mypy_boto3_emr_containers.type_defs import CancelJobRunRequestRequestTypeDef

    data: CancelJobRunRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    EndpointStateType,
    FailureReasonType,
    JobRunStateType,
    PersistentAppUIType,
    TemplateParameterDataTypeType,
    VirtualClusterStateType,
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
    "CancelJobRunRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CertificateTypeDef",
    "CloudWatchMonitoringConfigurationTypeDef",
    "ConfigurationTypeDef",
    "EksInfoTypeDef",
    "ContainerLogRotationConfigurationTypeDef",
    "CredentialsTypeDef",
    "DeleteJobTemplateRequestRequestTypeDef",
    "DeleteManagedEndpointRequestRequestTypeDef",
    "DeleteVirtualClusterRequestRequestTypeDef",
    "DescribeJobRunRequestRequestTypeDef",
    "DescribeJobTemplateRequestRequestTypeDef",
    "DescribeManagedEndpointRequestRequestTypeDef",
    "DescribeVirtualClusterRequestRequestTypeDef",
    "GetManagedEndpointSessionCredentialsRequestRequestTypeDef",
    "SparkSqlJobDriverTypeDef",
    "SparkSubmitJobDriverTypeDef",
    "RetryPolicyConfigurationTypeDef",
    "RetryPolicyExecutionTypeDef",
    "TemplateParameterConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ListJobRunsRequestRequestTypeDef",
    "ListJobTemplatesRequestRequestTypeDef",
    "ListManagedEndpointsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListVirtualClustersRequestRequestTypeDef",
    "S3MonitoringConfigurationTypeDef",
    "ParametricCloudWatchMonitoringConfigurationTypeDef",
    "ParametricS3MonitoringConfigurationTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "CancelJobRunResponseTypeDef",
    "CreateJobTemplateResponseTypeDef",
    "CreateManagedEndpointResponseTypeDef",
    "CreateVirtualClusterResponseTypeDef",
    "DeleteJobTemplateResponseTypeDef",
    "DeleteManagedEndpointResponseTypeDef",
    "DeleteVirtualClusterResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "StartJobRunResponseTypeDef",
    "ContainerInfoTypeDef",
    "GetManagedEndpointSessionCredentialsResponseTypeDef",
    "JobDriverTypeDef",
    "ListJobRunsRequestListJobRunsPaginateTypeDef",
    "ListJobTemplatesRequestListJobTemplatesPaginateTypeDef",
    "ListManagedEndpointsRequestListManagedEndpointsPaginateTypeDef",
    "ListVirtualClustersRequestListVirtualClustersPaginateTypeDef",
    "MonitoringConfigurationTypeDef",
    "ParametricMonitoringConfigurationTypeDef",
    "ContainerProviderTypeDef",
    "ConfigurationOverridesTypeDef",
    "ParametricConfigurationOverridesTypeDef",
    "CreateVirtualClusterRequestRequestTypeDef",
    "VirtualClusterTypeDef",
    "CreateManagedEndpointRequestRequestTypeDef",
    "EndpointTypeDef",
    "JobRunTypeDef",
    "StartJobRunRequestRequestTypeDef",
    "JobTemplateDataTypeDef",
    "DescribeVirtualClusterResponseTypeDef",
    "ListVirtualClustersResponseTypeDef",
    "DescribeManagedEndpointResponseTypeDef",
    "ListManagedEndpointsResponseTypeDef",
    "DescribeJobRunResponseTypeDef",
    "ListJobRunsResponseTypeDef",
    "CreateJobTemplateRequestRequestTypeDef",
    "JobTemplateTypeDef",
    "DescribeJobTemplateResponseTypeDef",
    "ListJobTemplatesResponseTypeDef",
)

CancelJobRunRequestRequestTypeDef = TypedDict(
    "CancelJobRunRequestRequestTypeDef",
    {
        "id": str,
        "virtualClusterId": str,
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

CertificateTypeDef = TypedDict(
    "CertificateTypeDef",
    {
        "certificateArn": str,
        "certificateData": str,
    },
    total=False,
)

_RequiredCloudWatchMonitoringConfigurationTypeDef = TypedDict(
    "_RequiredCloudWatchMonitoringConfigurationTypeDef",
    {
        "logGroupName": str,
    },
)
_OptionalCloudWatchMonitoringConfigurationTypeDef = TypedDict(
    "_OptionalCloudWatchMonitoringConfigurationTypeDef",
    {
        "logStreamNamePrefix": str,
    },
    total=False,
)

class CloudWatchMonitoringConfigurationTypeDef(
    _RequiredCloudWatchMonitoringConfigurationTypeDef,
    _OptionalCloudWatchMonitoringConfigurationTypeDef,
):
    pass

_RequiredConfigurationTypeDef = TypedDict(
    "_RequiredConfigurationTypeDef",
    {
        "classification": str,
    },
)
_OptionalConfigurationTypeDef = TypedDict(
    "_OptionalConfigurationTypeDef",
    {
        "properties": Mapping[str, str],
        "configurations": Sequence[Dict[str, Any]],
    },
    total=False,
)

class ConfigurationTypeDef(_RequiredConfigurationTypeDef, _OptionalConfigurationTypeDef):
    pass

EksInfoTypeDef = TypedDict(
    "EksInfoTypeDef",
    {
        "namespace": str,
    },
    total=False,
)

ContainerLogRotationConfigurationTypeDef = TypedDict(
    "ContainerLogRotationConfigurationTypeDef",
    {
        "rotationSize": str,
        "maxFilesToKeep": int,
    },
)

CredentialsTypeDef = TypedDict(
    "CredentialsTypeDef",
    {
        "token": str,
    },
    total=False,
)

DeleteJobTemplateRequestRequestTypeDef = TypedDict(
    "DeleteJobTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)

DeleteManagedEndpointRequestRequestTypeDef = TypedDict(
    "DeleteManagedEndpointRequestRequestTypeDef",
    {
        "id": str,
        "virtualClusterId": str,
    },
)

DeleteVirtualClusterRequestRequestTypeDef = TypedDict(
    "DeleteVirtualClusterRequestRequestTypeDef",
    {
        "id": str,
    },
)

DescribeJobRunRequestRequestTypeDef = TypedDict(
    "DescribeJobRunRequestRequestTypeDef",
    {
        "id": str,
        "virtualClusterId": str,
    },
)

DescribeJobTemplateRequestRequestTypeDef = TypedDict(
    "DescribeJobTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)

DescribeManagedEndpointRequestRequestTypeDef = TypedDict(
    "DescribeManagedEndpointRequestRequestTypeDef",
    {
        "id": str,
        "virtualClusterId": str,
    },
)

DescribeVirtualClusterRequestRequestTypeDef = TypedDict(
    "DescribeVirtualClusterRequestRequestTypeDef",
    {
        "id": str,
    },
)

_RequiredGetManagedEndpointSessionCredentialsRequestRequestTypeDef = TypedDict(
    "_RequiredGetManagedEndpointSessionCredentialsRequestRequestTypeDef",
    {
        "endpointIdentifier": str,
        "virtualClusterIdentifier": str,
        "executionRoleArn": str,
        "credentialType": str,
    },
)
_OptionalGetManagedEndpointSessionCredentialsRequestRequestTypeDef = TypedDict(
    "_OptionalGetManagedEndpointSessionCredentialsRequestRequestTypeDef",
    {
        "durationInSeconds": int,
        "logContext": str,
        "clientToken": str,
    },
    total=False,
)

class GetManagedEndpointSessionCredentialsRequestRequestTypeDef(
    _RequiredGetManagedEndpointSessionCredentialsRequestRequestTypeDef,
    _OptionalGetManagedEndpointSessionCredentialsRequestRequestTypeDef,
):
    pass

SparkSqlJobDriverTypeDef = TypedDict(
    "SparkSqlJobDriverTypeDef",
    {
        "entryPoint": str,
        "sparkSqlParameters": str,
    },
    total=False,
)

_RequiredSparkSubmitJobDriverTypeDef = TypedDict(
    "_RequiredSparkSubmitJobDriverTypeDef",
    {
        "entryPoint": str,
    },
)
_OptionalSparkSubmitJobDriverTypeDef = TypedDict(
    "_OptionalSparkSubmitJobDriverTypeDef",
    {
        "entryPointArguments": Sequence[str],
        "sparkSubmitParameters": str,
    },
    total=False,
)

class SparkSubmitJobDriverTypeDef(
    _RequiredSparkSubmitJobDriverTypeDef, _OptionalSparkSubmitJobDriverTypeDef
):
    pass

RetryPolicyConfigurationTypeDef = TypedDict(
    "RetryPolicyConfigurationTypeDef",
    {
        "maxAttempts": int,
    },
)

RetryPolicyExecutionTypeDef = TypedDict(
    "RetryPolicyExecutionTypeDef",
    {
        "currentAttemptCount": int,
    },
)

TemplateParameterConfigurationTypeDef = TypedDict(
    "TemplateParameterConfigurationTypeDef",
    {
        "type": TemplateParameterDataTypeType,
        "defaultValue": str,
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

_RequiredListJobRunsRequestRequestTypeDef = TypedDict(
    "_RequiredListJobRunsRequestRequestTypeDef",
    {
        "virtualClusterId": str,
    },
)
_OptionalListJobRunsRequestRequestTypeDef = TypedDict(
    "_OptionalListJobRunsRequestRequestTypeDef",
    {
        "createdBefore": Union[datetime, str],
        "createdAfter": Union[datetime, str],
        "name": str,
        "states": Sequence[JobRunStateType],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListJobRunsRequestRequestTypeDef(
    _RequiredListJobRunsRequestRequestTypeDef, _OptionalListJobRunsRequestRequestTypeDef
):
    pass

ListJobTemplatesRequestRequestTypeDef = TypedDict(
    "ListJobTemplatesRequestRequestTypeDef",
    {
        "createdAfter": Union[datetime, str],
        "createdBefore": Union[datetime, str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListManagedEndpointsRequestRequestTypeDef = TypedDict(
    "_RequiredListManagedEndpointsRequestRequestTypeDef",
    {
        "virtualClusterId": str,
    },
)
_OptionalListManagedEndpointsRequestRequestTypeDef = TypedDict(
    "_OptionalListManagedEndpointsRequestRequestTypeDef",
    {
        "createdBefore": Union[datetime, str],
        "createdAfter": Union[datetime, str],
        "types": Sequence[str],
        "states": Sequence[EndpointStateType],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListManagedEndpointsRequestRequestTypeDef(
    _RequiredListManagedEndpointsRequestRequestTypeDef,
    _OptionalListManagedEndpointsRequestRequestTypeDef,
):
    pass

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListVirtualClustersRequestRequestTypeDef = TypedDict(
    "ListVirtualClustersRequestRequestTypeDef",
    {
        "containerProviderId": str,
        "containerProviderType": Literal["EKS"],
        "createdAfter": Union[datetime, str],
        "createdBefore": Union[datetime, str],
        "states": Sequence[VirtualClusterStateType],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

S3MonitoringConfigurationTypeDef = TypedDict(
    "S3MonitoringConfigurationTypeDef",
    {
        "logUri": str,
    },
)

ParametricCloudWatchMonitoringConfigurationTypeDef = TypedDict(
    "ParametricCloudWatchMonitoringConfigurationTypeDef",
    {
        "logGroupName": str,
        "logStreamNamePrefix": str,
    },
    total=False,
)

ParametricS3MonitoringConfigurationTypeDef = TypedDict(
    "ParametricS3MonitoringConfigurationTypeDef",
    {
        "logUri": str,
    },
    total=False,
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

CancelJobRunResponseTypeDef = TypedDict(
    "CancelJobRunResponseTypeDef",
    {
        "id": str,
        "virtualClusterId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateJobTemplateResponseTypeDef = TypedDict(
    "CreateJobTemplateResponseTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "createdAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateManagedEndpointResponseTypeDef = TypedDict(
    "CreateManagedEndpointResponseTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "virtualClusterId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateVirtualClusterResponseTypeDef = TypedDict(
    "CreateVirtualClusterResponseTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteJobTemplateResponseTypeDef = TypedDict(
    "DeleteJobTemplateResponseTypeDef",
    {
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteManagedEndpointResponseTypeDef = TypedDict(
    "DeleteManagedEndpointResponseTypeDef",
    {
        "id": str,
        "virtualClusterId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVirtualClusterResponseTypeDef = TypedDict(
    "DeleteVirtualClusterResponseTypeDef",
    {
        "id": str,
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

StartJobRunResponseTypeDef = TypedDict(
    "StartJobRunResponseTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "virtualClusterId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ContainerInfoTypeDef = TypedDict(
    "ContainerInfoTypeDef",
    {
        "eksInfo": EksInfoTypeDef,
    },
    total=False,
)

GetManagedEndpointSessionCredentialsResponseTypeDef = TypedDict(
    "GetManagedEndpointSessionCredentialsResponseTypeDef",
    {
        "id": str,
        "credentials": CredentialsTypeDef,
        "expiresAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

JobDriverTypeDef = TypedDict(
    "JobDriverTypeDef",
    {
        "sparkSubmitJobDriver": SparkSubmitJobDriverTypeDef,
        "sparkSqlJobDriver": SparkSqlJobDriverTypeDef,
    },
    total=False,
)

_RequiredListJobRunsRequestListJobRunsPaginateTypeDef = TypedDict(
    "_RequiredListJobRunsRequestListJobRunsPaginateTypeDef",
    {
        "virtualClusterId": str,
    },
)
_OptionalListJobRunsRequestListJobRunsPaginateTypeDef = TypedDict(
    "_OptionalListJobRunsRequestListJobRunsPaginateTypeDef",
    {
        "createdBefore": Union[datetime, str],
        "createdAfter": Union[datetime, str],
        "name": str,
        "states": Sequence[JobRunStateType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListJobRunsRequestListJobRunsPaginateTypeDef(
    _RequiredListJobRunsRequestListJobRunsPaginateTypeDef,
    _OptionalListJobRunsRequestListJobRunsPaginateTypeDef,
):
    pass

ListJobTemplatesRequestListJobTemplatesPaginateTypeDef = TypedDict(
    "ListJobTemplatesRequestListJobTemplatesPaginateTypeDef",
    {
        "createdAfter": Union[datetime, str],
        "createdBefore": Union[datetime, str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListManagedEndpointsRequestListManagedEndpointsPaginateTypeDef = TypedDict(
    "_RequiredListManagedEndpointsRequestListManagedEndpointsPaginateTypeDef",
    {
        "virtualClusterId": str,
    },
)
_OptionalListManagedEndpointsRequestListManagedEndpointsPaginateTypeDef = TypedDict(
    "_OptionalListManagedEndpointsRequestListManagedEndpointsPaginateTypeDef",
    {
        "createdBefore": Union[datetime, str],
        "createdAfter": Union[datetime, str],
        "types": Sequence[str],
        "states": Sequence[EndpointStateType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListManagedEndpointsRequestListManagedEndpointsPaginateTypeDef(
    _RequiredListManagedEndpointsRequestListManagedEndpointsPaginateTypeDef,
    _OptionalListManagedEndpointsRequestListManagedEndpointsPaginateTypeDef,
):
    pass

ListVirtualClustersRequestListVirtualClustersPaginateTypeDef = TypedDict(
    "ListVirtualClustersRequestListVirtualClustersPaginateTypeDef",
    {
        "containerProviderId": str,
        "containerProviderType": Literal["EKS"],
        "createdAfter": Union[datetime, str],
        "createdBefore": Union[datetime, str],
        "states": Sequence[VirtualClusterStateType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

MonitoringConfigurationTypeDef = TypedDict(
    "MonitoringConfigurationTypeDef",
    {
        "persistentAppUI": PersistentAppUIType,
        "cloudWatchMonitoringConfiguration": CloudWatchMonitoringConfigurationTypeDef,
        "s3MonitoringConfiguration": S3MonitoringConfigurationTypeDef,
        "containerLogRotationConfiguration": ContainerLogRotationConfigurationTypeDef,
    },
    total=False,
)

ParametricMonitoringConfigurationTypeDef = TypedDict(
    "ParametricMonitoringConfigurationTypeDef",
    {
        "persistentAppUI": str,
        "cloudWatchMonitoringConfiguration": ParametricCloudWatchMonitoringConfigurationTypeDef,
        "s3MonitoringConfiguration": ParametricS3MonitoringConfigurationTypeDef,
    },
    total=False,
)

_RequiredContainerProviderTypeDef = TypedDict(
    "_RequiredContainerProviderTypeDef",
    {
        "type": Literal["EKS"],
        "id": str,
    },
)
_OptionalContainerProviderTypeDef = TypedDict(
    "_OptionalContainerProviderTypeDef",
    {
        "info": ContainerInfoTypeDef,
    },
    total=False,
)

class ContainerProviderTypeDef(
    _RequiredContainerProviderTypeDef, _OptionalContainerProviderTypeDef
):
    pass

ConfigurationOverridesTypeDef = TypedDict(
    "ConfigurationOverridesTypeDef",
    {
        "applicationConfiguration": Sequence["ConfigurationTypeDef"],
        "monitoringConfiguration": MonitoringConfigurationTypeDef,
    },
    total=False,
)

ParametricConfigurationOverridesTypeDef = TypedDict(
    "ParametricConfigurationOverridesTypeDef",
    {
        "applicationConfiguration": Sequence["ConfigurationTypeDef"],
        "monitoringConfiguration": ParametricMonitoringConfigurationTypeDef,
    },
    total=False,
)

_RequiredCreateVirtualClusterRequestRequestTypeDef = TypedDict(
    "_RequiredCreateVirtualClusterRequestRequestTypeDef",
    {
        "name": str,
        "containerProvider": ContainerProviderTypeDef,
        "clientToken": str,
    },
)
_OptionalCreateVirtualClusterRequestRequestTypeDef = TypedDict(
    "_OptionalCreateVirtualClusterRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateVirtualClusterRequestRequestTypeDef(
    _RequiredCreateVirtualClusterRequestRequestTypeDef,
    _OptionalCreateVirtualClusterRequestRequestTypeDef,
):
    pass

VirtualClusterTypeDef = TypedDict(
    "VirtualClusterTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "state": VirtualClusterStateType,
        "containerProvider": ContainerProviderTypeDef,
        "createdAt": datetime,
        "tags": Dict[str, str],
    },
    total=False,
)

_RequiredCreateManagedEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredCreateManagedEndpointRequestRequestTypeDef",
    {
        "name": str,
        "virtualClusterId": str,
        "type": str,
        "releaseLabel": str,
        "executionRoleArn": str,
        "clientToken": str,
    },
)
_OptionalCreateManagedEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalCreateManagedEndpointRequestRequestTypeDef",
    {
        "certificateArn": str,
        "configurationOverrides": ConfigurationOverridesTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateManagedEndpointRequestRequestTypeDef(
    _RequiredCreateManagedEndpointRequestRequestTypeDef,
    _OptionalCreateManagedEndpointRequestRequestTypeDef,
):
    pass

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "virtualClusterId": str,
        "type": str,
        "state": EndpointStateType,
        "releaseLabel": str,
        "executionRoleArn": str,
        "certificateArn": str,
        "certificateAuthority": CertificateTypeDef,
        "configurationOverrides": ConfigurationOverridesTypeDef,
        "serverUrl": str,
        "createdAt": datetime,
        "securityGroup": str,
        "subnetIds": List[str],
        "stateDetails": str,
        "failureReason": FailureReasonType,
        "tags": Dict[str, str],
    },
    total=False,
)

JobRunTypeDef = TypedDict(
    "JobRunTypeDef",
    {
        "id": str,
        "name": str,
        "virtualClusterId": str,
        "arn": str,
        "state": JobRunStateType,
        "clientToken": str,
        "executionRoleArn": str,
        "releaseLabel": str,
        "configurationOverrides": ConfigurationOverridesTypeDef,
        "jobDriver": JobDriverTypeDef,
        "createdAt": datetime,
        "createdBy": str,
        "finishedAt": datetime,
        "stateDetails": str,
        "failureReason": FailureReasonType,
        "tags": Dict[str, str],
        "retryPolicyConfiguration": RetryPolicyConfigurationTypeDef,
        "retryPolicyExecution": RetryPolicyExecutionTypeDef,
    },
    total=False,
)

_RequiredStartJobRunRequestRequestTypeDef = TypedDict(
    "_RequiredStartJobRunRequestRequestTypeDef",
    {
        "virtualClusterId": str,
        "clientToken": str,
    },
)
_OptionalStartJobRunRequestRequestTypeDef = TypedDict(
    "_OptionalStartJobRunRequestRequestTypeDef",
    {
        "name": str,
        "executionRoleArn": str,
        "releaseLabel": str,
        "jobDriver": JobDriverTypeDef,
        "configurationOverrides": ConfigurationOverridesTypeDef,
        "tags": Mapping[str, str],
        "jobTemplateId": str,
        "jobTemplateParameters": Mapping[str, str],
        "retryPolicyConfiguration": RetryPolicyConfigurationTypeDef,
    },
    total=False,
)

class StartJobRunRequestRequestTypeDef(
    _RequiredStartJobRunRequestRequestTypeDef, _OptionalStartJobRunRequestRequestTypeDef
):
    pass

_RequiredJobTemplateDataTypeDef = TypedDict(
    "_RequiredJobTemplateDataTypeDef",
    {
        "executionRoleArn": str,
        "releaseLabel": str,
        "jobDriver": JobDriverTypeDef,
    },
)
_OptionalJobTemplateDataTypeDef = TypedDict(
    "_OptionalJobTemplateDataTypeDef",
    {
        "configurationOverrides": ParametricConfigurationOverridesTypeDef,
        "parameterConfiguration": Mapping[str, TemplateParameterConfigurationTypeDef],
        "jobTags": Mapping[str, str],
    },
    total=False,
)

class JobTemplateDataTypeDef(_RequiredJobTemplateDataTypeDef, _OptionalJobTemplateDataTypeDef):
    pass

DescribeVirtualClusterResponseTypeDef = TypedDict(
    "DescribeVirtualClusterResponseTypeDef",
    {
        "virtualCluster": VirtualClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVirtualClustersResponseTypeDef = TypedDict(
    "ListVirtualClustersResponseTypeDef",
    {
        "virtualClusters": List[VirtualClusterTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeManagedEndpointResponseTypeDef = TypedDict(
    "DescribeManagedEndpointResponseTypeDef",
    {
        "endpoint": EndpointTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListManagedEndpointsResponseTypeDef = TypedDict(
    "ListManagedEndpointsResponseTypeDef",
    {
        "endpoints": List[EndpointTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeJobRunResponseTypeDef = TypedDict(
    "DescribeJobRunResponseTypeDef",
    {
        "jobRun": JobRunTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJobRunsResponseTypeDef = TypedDict(
    "ListJobRunsResponseTypeDef",
    {
        "jobRuns": List[JobRunTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateJobTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredCreateJobTemplateRequestRequestTypeDef",
    {
        "name": str,
        "clientToken": str,
        "jobTemplateData": JobTemplateDataTypeDef,
    },
)
_OptionalCreateJobTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalCreateJobTemplateRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
        "kmsKeyArn": str,
    },
    total=False,
)

class CreateJobTemplateRequestRequestTypeDef(
    _RequiredCreateJobTemplateRequestRequestTypeDef, _OptionalCreateJobTemplateRequestRequestTypeDef
):
    pass

_RequiredJobTemplateTypeDef = TypedDict(
    "_RequiredJobTemplateTypeDef",
    {
        "jobTemplateData": JobTemplateDataTypeDef,
    },
)
_OptionalJobTemplateTypeDef = TypedDict(
    "_OptionalJobTemplateTypeDef",
    {
        "name": str,
        "id": str,
        "arn": str,
        "createdAt": datetime,
        "createdBy": str,
        "tags": Dict[str, str],
        "kmsKeyArn": str,
        "decryptionError": str,
    },
    total=False,
)

class JobTemplateTypeDef(_RequiredJobTemplateTypeDef, _OptionalJobTemplateTypeDef):
    pass

DescribeJobTemplateResponseTypeDef = TypedDict(
    "DescribeJobTemplateResponseTypeDef",
    {
        "jobTemplate": JobTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJobTemplatesResponseTypeDef = TypedDict(
    "ListJobTemplatesResponseTypeDef",
    {
        "templates": List[JobTemplateTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
