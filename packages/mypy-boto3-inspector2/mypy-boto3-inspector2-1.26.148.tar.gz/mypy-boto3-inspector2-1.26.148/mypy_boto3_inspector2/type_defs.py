"""
Type annotations for inspector2 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/type_defs/)

Usage::

    ```python
    from mypy_boto3_inspector2.type_defs import SeverityCountsTypeDef

    data: SeverityCountsTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AccountSortByType,
    AggregationFindingTypeType,
    AggregationResourceTypeType,
    AggregationTypeType,
    AmiSortByType,
    ArchitectureType,
    AwsEcrContainerSortByType,
    CoverageResourceTypeType,
    CoverageStringComparisonType,
    DelegatedAdminStatusType,
    Ec2DeepInspectionStatusType,
    Ec2InstanceSortByType,
    Ec2PlatformType,
    EcrRescanDurationStatusType,
    EcrRescanDurationType,
    EcrScanFrequencyType,
    ErrorCodeType,
    ExploitAvailableType,
    ExternalReportStatusType,
    FilterActionType,
    FindingStatusType,
    FindingTypeSortByType,
    FindingTypeType,
    FixAvailableType,
    FreeTrialInfoErrorCodeType,
    FreeTrialStatusType,
    FreeTrialTypeType,
    GroupKeyType,
    ImageLayerSortByType,
    LambdaFunctionSortByType,
    LambdaLayerSortByType,
    NetworkProtocolType,
    OperationType,
    PackageManagerType,
    PackageSortByType,
    PackageTypeType,
    RelationshipStatusType,
    ReportFormatType,
    ReportingErrorCodeType,
    RepositorySortByType,
    ResourceScanTypeType,
    ResourceTypeType,
    RuntimeType,
    ScanStatusCodeType,
    ScanStatusReasonType,
    ScanTypeType,
    ServiceType,
    SeverityType,
    SortFieldType,
    SortOrderType,
    StatusType,
    StringComparisonType,
    TitleSortByType,
    UsageTypeType,
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
    "SeverityCountsTypeDef",
    "AccountAggregationTypeDef",
    "StateTypeDef",
    "ResourceStatusTypeDef",
    "FindingTypeAggregationTypeDef",
    "StringFilterTypeDef",
    "AssociateMemberRequestRequestTypeDef",
    "AssociateMemberResponseTypeDef",
    "AtigDataTypeDef",
    "AutoEnableTypeDef",
    "AwsEc2InstanceDetailsTypeDef",
    "AwsEcrContainerImageDetailsTypeDef",
    "LambdaVpcConfigTypeDef",
    "BatchGetAccountStatusRequestRequestTypeDef",
    "BatchGetFreeTrialInfoRequestRequestTypeDef",
    "FreeTrialInfoErrorTypeDef",
    "BatchGetMemberEc2DeepInspectionStatusRequestRequestTypeDef",
    "FailedMemberAccountEc2DeepInspectionStatusStateTypeDef",
    "MemberAccountEc2DeepInspectionStatusStateTypeDef",
    "MemberAccountEc2DeepInspectionStatusTypeDef",
    "CancelFindingsReportRequestRequestTypeDef",
    "CancelFindingsReportResponseTypeDef",
    "CisaDataTypeDef",
    "CountsTypeDef",
    "CoverageDateFilterTypeDef",
    "CoverageMapFilterTypeDef",
    "CoverageStringFilterTypeDef",
    "ScanStatusTypeDef",
    "CreateFilterResponseTypeDef",
    "DestinationTypeDef",
    "CreateFindingsReportResponseTypeDef",
    "Cvss2TypeDef",
    "Cvss3TypeDef",
    "CvssScoreAdjustmentTypeDef",
    "CvssScoreTypeDef",
    "DateFilterTypeDef",
    "DelegatedAdminAccountTypeDef",
    "DelegatedAdminTypeDef",
    "DeleteFilterRequestRequestTypeDef",
    "DeleteFilterResponseTypeDef",
    "DisableDelegatedAdminAccountRequestRequestTypeDef",
    "DisableDelegatedAdminAccountResponseTypeDef",
    "DisableRequestRequestTypeDef",
    "DisassociateMemberRequestRequestTypeDef",
    "DisassociateMemberResponseTypeDef",
    "MapFilterTypeDef",
    "Ec2MetadataTypeDef",
    "EcrRescanDurationStateTypeDef",
    "EcrConfigurationTypeDef",
    "EcrContainerImageMetadataTypeDef",
    "EcrRepositoryMetadataTypeDef",
    "EnableDelegatedAdminAccountRequestRequestTypeDef",
    "EnableDelegatedAdminAccountResponseTypeDef",
    "EnableRequestRequestTypeDef",
    "EpssTypeDef",
    "ExploitObservedTypeDef",
    "ExploitabilityDetailsTypeDef",
    "NumberFilterTypeDef",
    "PortRangeFilterTypeDef",
    "FreeTrialInfoTypeDef",
    "GetEc2DeepInspectionConfigurationResponseTypeDef",
    "GetFindingsReportStatusRequestRequestTypeDef",
    "GetMemberRequestRequestTypeDef",
    "MemberTypeDef",
    "LambdaFunctionMetadataTypeDef",
    "ListAccountPermissionsRequestListAccountPermissionsPaginateTypeDef",
    "ListAccountPermissionsRequestRequestTypeDef",
    "PermissionTypeDef",
    "ListDelegatedAdminAccountsRequestListDelegatedAdminAccountsPaginateTypeDef",
    "ListDelegatedAdminAccountsRequestRequestTypeDef",
    "ListFiltersRequestListFiltersPaginateTypeDef",
    "ListFiltersRequestRequestTypeDef",
    "SortCriteriaTypeDef",
    "ListMembersRequestListMembersPaginateTypeDef",
    "ListMembersRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListUsageTotalsRequestListUsageTotalsPaginateTypeDef",
    "ListUsageTotalsRequestRequestTypeDef",
    "StepTypeDef",
    "PortRangeTypeDef",
    "VulnerablePackageTypeDef",
    "PaginatorConfigTypeDef",
    "RecommendationTypeDef",
    "ResponseMetadataTypeDef",
    "SearchVulnerabilitiesFilterCriteriaTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateEc2DeepInspectionConfigurationRequestRequestTypeDef",
    "UpdateEc2DeepInspectionConfigurationResponseTypeDef",
    "UpdateFilterResponseTypeDef",
    "UpdateOrgEc2DeepInspectionConfigurationRequestRequestTypeDef",
    "UsageTypeDef",
    "AccountAggregationResponseTypeDef",
    "AmiAggregationResponseTypeDef",
    "AwsEcrContainerAggregationResponseTypeDef",
    "Ec2InstanceAggregationResponseTypeDef",
    "FindingTypeAggregationResponseTypeDef",
    "ImageLayerAggregationResponseTypeDef",
    "LambdaFunctionAggregationResponseTypeDef",
    "LambdaLayerAggregationResponseTypeDef",
    "PackageAggregationResponseTypeDef",
    "RepositoryAggregationResponseTypeDef",
    "TitleAggregationResponseTypeDef",
    "ResourceStateTypeDef",
    "AccountTypeDef",
    "FailedAccountTypeDef",
    "AmiAggregationTypeDef",
    "AwsEcrContainerAggregationTypeDef",
    "ImageLayerAggregationTypeDef",
    "LambdaLayerAggregationTypeDef",
    "PackageAggregationTypeDef",
    "RepositoryAggregationTypeDef",
    "TitleAggregationTypeDef",
    "DescribeOrganizationConfigurationResponseTypeDef",
    "UpdateOrganizationConfigurationRequestRequestTypeDef",
    "UpdateOrganizationConfigurationResponseTypeDef",
    "AwsLambdaFunctionDetailsTypeDef",
    "BatchGetMemberEc2DeepInspectionStatusResponseTypeDef",
    "BatchUpdateMemberEc2DeepInspectionStatusResponseTypeDef",
    "BatchUpdateMemberEc2DeepInspectionStatusRequestRequestTypeDef",
    "ListCoverageStatisticsResponseTypeDef",
    "CoverageFilterCriteriaTypeDef",
    "CvssScoreDetailsTypeDef",
    "ListDelegatedAdminAccountsResponseTypeDef",
    "GetDelegatedAdminAccountResponseTypeDef",
    "Ec2InstanceAggregationTypeDef",
    "LambdaFunctionAggregationTypeDef",
    "EcrConfigurationStateTypeDef",
    "UpdateConfigurationRequestRequestTypeDef",
    "VulnerabilityTypeDef",
    "PackageFilterTypeDef",
    "FreeTrialAccountInfoTypeDef",
    "GetMemberResponseTypeDef",
    "ListMembersResponseTypeDef",
    "ResourceScanMetadataTypeDef",
    "ListAccountPermissionsResponseTypeDef",
    "NetworkPathTypeDef",
    "PackageVulnerabilityDetailsTypeDef",
    "RemediationTypeDef",
    "SearchVulnerabilitiesRequestRequestTypeDef",
    "SearchVulnerabilitiesRequestSearchVulnerabilitiesPaginateTypeDef",
    "UsageTotalTypeDef",
    "AggregationResponseTypeDef",
    "AccountStateTypeDef",
    "DisableResponseTypeDef",
    "EnableResponseTypeDef",
    "ResourceDetailsTypeDef",
    "ListCoverageRequestListCoveragePaginateTypeDef",
    "ListCoverageRequestRequestTypeDef",
    "ListCoverageStatisticsRequestListCoverageStatisticsPaginateTypeDef",
    "ListCoverageStatisticsRequestRequestTypeDef",
    "InspectorScoreDetailsTypeDef",
    "AggregationRequestTypeDef",
    "GetConfigurationResponseTypeDef",
    "SearchVulnerabilitiesResponseTypeDef",
    "FilterCriteriaTypeDef",
    "BatchGetFreeTrialInfoResponseTypeDef",
    "CoveredResourceTypeDef",
    "NetworkReachabilityDetailsTypeDef",
    "ListUsageTotalsResponseTypeDef",
    "ListFindingAggregationsResponseTypeDef",
    "BatchGetAccountStatusResponseTypeDef",
    "ResourceTypeDef",
    "ListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef",
    "ListFindingAggregationsRequestRequestTypeDef",
    "CreateFilterRequestRequestTypeDef",
    "CreateFindingsReportRequestRequestTypeDef",
    "FilterTypeDef",
    "GetFindingsReportStatusResponseTypeDef",
    "ListFindingsRequestListFindingsPaginateTypeDef",
    "ListFindingsRequestRequestTypeDef",
    "UpdateFilterRequestRequestTypeDef",
    "ListCoverageResponseTypeDef",
    "FindingTypeDef",
    "ListFiltersResponseTypeDef",
    "ListFindingsResponseTypeDef",
)

SeverityCountsTypeDef = TypedDict(
    "SeverityCountsTypeDef",
    {
        "all": int,
        "critical": int,
        "high": int,
        "medium": int,
    },
    total=False,
)

AccountAggregationTypeDef = TypedDict(
    "AccountAggregationTypeDef",
    {
        "findingType": AggregationFindingTypeType,
        "resourceType": AggregationResourceTypeType,
        "sortBy": AccountSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

StateTypeDef = TypedDict(
    "StateTypeDef",
    {
        "errorCode": ErrorCodeType,
        "errorMessage": str,
        "status": StatusType,
    },
)

_RequiredResourceStatusTypeDef = TypedDict(
    "_RequiredResourceStatusTypeDef",
    {
        "ec2": StatusType,
        "ecr": StatusType,
    },
)
_OptionalResourceStatusTypeDef = TypedDict(
    "_OptionalResourceStatusTypeDef",
    {
        "lambda": StatusType,
    },
    total=False,
)


class ResourceStatusTypeDef(_RequiredResourceStatusTypeDef, _OptionalResourceStatusTypeDef):
    pass


FindingTypeAggregationTypeDef = TypedDict(
    "FindingTypeAggregationTypeDef",
    {
        "findingType": AggregationFindingTypeType,
        "resourceType": AggregationResourceTypeType,
        "sortBy": FindingTypeSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

StringFilterTypeDef = TypedDict(
    "StringFilterTypeDef",
    {
        "comparison": StringComparisonType,
        "value": str,
    },
)

AssociateMemberRequestRequestTypeDef = TypedDict(
    "AssociateMemberRequestRequestTypeDef",
    {
        "accountId": str,
    },
)

AssociateMemberResponseTypeDef = TypedDict(
    "AssociateMemberResponseTypeDef",
    {
        "accountId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AtigDataTypeDef = TypedDict(
    "AtigDataTypeDef",
    {
        "firstSeen": datetime,
        "lastSeen": datetime,
        "targets": List[str],
        "ttps": List[str],
    },
    total=False,
)

_RequiredAutoEnableTypeDef = TypedDict(
    "_RequiredAutoEnableTypeDef",
    {
        "ec2": bool,
        "ecr": bool,
    },
)
_OptionalAutoEnableTypeDef = TypedDict(
    "_OptionalAutoEnableTypeDef",
    {
        "lambda": bool,
    },
    total=False,
)


class AutoEnableTypeDef(_RequiredAutoEnableTypeDef, _OptionalAutoEnableTypeDef):
    pass


AwsEc2InstanceDetailsTypeDef = TypedDict(
    "AwsEc2InstanceDetailsTypeDef",
    {
        "iamInstanceProfileArn": str,
        "imageId": str,
        "ipV4Addresses": List[str],
        "ipV6Addresses": List[str],
        "keyName": str,
        "launchedAt": datetime,
        "platform": str,
        "subnetId": str,
        "type": str,
        "vpcId": str,
    },
    total=False,
)

_RequiredAwsEcrContainerImageDetailsTypeDef = TypedDict(
    "_RequiredAwsEcrContainerImageDetailsTypeDef",
    {
        "imageHash": str,
        "registry": str,
        "repositoryName": str,
    },
)
_OptionalAwsEcrContainerImageDetailsTypeDef = TypedDict(
    "_OptionalAwsEcrContainerImageDetailsTypeDef",
    {
        "architecture": str,
        "author": str,
        "imageTags": List[str],
        "platform": str,
        "pushedAt": datetime,
    },
    total=False,
)


class AwsEcrContainerImageDetailsTypeDef(
    _RequiredAwsEcrContainerImageDetailsTypeDef, _OptionalAwsEcrContainerImageDetailsTypeDef
):
    pass


LambdaVpcConfigTypeDef = TypedDict(
    "LambdaVpcConfigTypeDef",
    {
        "securityGroupIds": List[str],
        "subnetIds": List[str],
        "vpcId": str,
    },
    total=False,
)

BatchGetAccountStatusRequestRequestTypeDef = TypedDict(
    "BatchGetAccountStatusRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
    },
    total=False,
)

BatchGetFreeTrialInfoRequestRequestTypeDef = TypedDict(
    "BatchGetFreeTrialInfoRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
    },
)

FreeTrialInfoErrorTypeDef = TypedDict(
    "FreeTrialInfoErrorTypeDef",
    {
        "accountId": str,
        "code": FreeTrialInfoErrorCodeType,
        "message": str,
    },
)

BatchGetMemberEc2DeepInspectionStatusRequestRequestTypeDef = TypedDict(
    "BatchGetMemberEc2DeepInspectionStatusRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
    },
    total=False,
)

_RequiredFailedMemberAccountEc2DeepInspectionStatusStateTypeDef = TypedDict(
    "_RequiredFailedMemberAccountEc2DeepInspectionStatusStateTypeDef",
    {
        "accountId": str,
    },
)
_OptionalFailedMemberAccountEc2DeepInspectionStatusStateTypeDef = TypedDict(
    "_OptionalFailedMemberAccountEc2DeepInspectionStatusStateTypeDef",
    {
        "ec2ScanStatus": StatusType,
        "errorMessage": str,
    },
    total=False,
)


class FailedMemberAccountEc2DeepInspectionStatusStateTypeDef(
    _RequiredFailedMemberAccountEc2DeepInspectionStatusStateTypeDef,
    _OptionalFailedMemberAccountEc2DeepInspectionStatusStateTypeDef,
):
    pass


_RequiredMemberAccountEc2DeepInspectionStatusStateTypeDef = TypedDict(
    "_RequiredMemberAccountEc2DeepInspectionStatusStateTypeDef",
    {
        "accountId": str,
    },
)
_OptionalMemberAccountEc2DeepInspectionStatusStateTypeDef = TypedDict(
    "_OptionalMemberAccountEc2DeepInspectionStatusStateTypeDef",
    {
        "errorMessage": str,
        "status": Ec2DeepInspectionStatusType,
    },
    total=False,
)


class MemberAccountEc2DeepInspectionStatusStateTypeDef(
    _RequiredMemberAccountEc2DeepInspectionStatusStateTypeDef,
    _OptionalMemberAccountEc2DeepInspectionStatusStateTypeDef,
):
    pass


MemberAccountEc2DeepInspectionStatusTypeDef = TypedDict(
    "MemberAccountEc2DeepInspectionStatusTypeDef",
    {
        "accountId": str,
        "activateDeepInspection": bool,
    },
)

CancelFindingsReportRequestRequestTypeDef = TypedDict(
    "CancelFindingsReportRequestRequestTypeDef",
    {
        "reportId": str,
    },
)

CancelFindingsReportResponseTypeDef = TypedDict(
    "CancelFindingsReportResponseTypeDef",
    {
        "reportId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CisaDataTypeDef = TypedDict(
    "CisaDataTypeDef",
    {
        "action": str,
        "dateAdded": datetime,
        "dateDue": datetime,
    },
    total=False,
)

CountsTypeDef = TypedDict(
    "CountsTypeDef",
    {
        "count": int,
        "groupKey": GroupKeyType,
    },
    total=False,
)

CoverageDateFilterTypeDef = TypedDict(
    "CoverageDateFilterTypeDef",
    {
        "endInclusive": Union[datetime, str],
        "startInclusive": Union[datetime, str],
    },
    total=False,
)

_RequiredCoverageMapFilterTypeDef = TypedDict(
    "_RequiredCoverageMapFilterTypeDef",
    {
        "comparison": Literal["EQUALS"],
        "key": str,
    },
)
_OptionalCoverageMapFilterTypeDef = TypedDict(
    "_OptionalCoverageMapFilterTypeDef",
    {
        "value": str,
    },
    total=False,
)


class CoverageMapFilterTypeDef(
    _RequiredCoverageMapFilterTypeDef, _OptionalCoverageMapFilterTypeDef
):
    pass


CoverageStringFilterTypeDef = TypedDict(
    "CoverageStringFilterTypeDef",
    {
        "comparison": CoverageStringComparisonType,
        "value": str,
    },
)

ScanStatusTypeDef = TypedDict(
    "ScanStatusTypeDef",
    {
        "reason": ScanStatusReasonType,
        "statusCode": ScanStatusCodeType,
    },
)

CreateFilterResponseTypeDef = TypedDict(
    "CreateFilterResponseTypeDef",
    {
        "arn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDestinationTypeDef = TypedDict(
    "_RequiredDestinationTypeDef",
    {
        "bucketName": str,
        "kmsKeyArn": str,
    },
)
_OptionalDestinationTypeDef = TypedDict(
    "_OptionalDestinationTypeDef",
    {
        "keyPrefix": str,
    },
    total=False,
)


class DestinationTypeDef(_RequiredDestinationTypeDef, _OptionalDestinationTypeDef):
    pass


CreateFindingsReportResponseTypeDef = TypedDict(
    "CreateFindingsReportResponseTypeDef",
    {
        "reportId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

Cvss2TypeDef = TypedDict(
    "Cvss2TypeDef",
    {
        "baseScore": float,
        "scoringVector": str,
    },
    total=False,
)

Cvss3TypeDef = TypedDict(
    "Cvss3TypeDef",
    {
        "baseScore": float,
        "scoringVector": str,
    },
    total=False,
)

CvssScoreAdjustmentTypeDef = TypedDict(
    "CvssScoreAdjustmentTypeDef",
    {
        "metric": str,
        "reason": str,
    },
)

CvssScoreTypeDef = TypedDict(
    "CvssScoreTypeDef",
    {
        "baseScore": float,
        "scoringVector": str,
        "source": str,
        "version": str,
    },
)

DateFilterTypeDef = TypedDict(
    "DateFilterTypeDef",
    {
        "endInclusive": Union[datetime, str],
        "startInclusive": Union[datetime, str],
    },
    total=False,
)

DelegatedAdminAccountTypeDef = TypedDict(
    "DelegatedAdminAccountTypeDef",
    {
        "accountId": str,
        "status": DelegatedAdminStatusType,
    },
    total=False,
)

DelegatedAdminTypeDef = TypedDict(
    "DelegatedAdminTypeDef",
    {
        "accountId": str,
        "relationshipStatus": RelationshipStatusType,
    },
    total=False,
)

DeleteFilterRequestRequestTypeDef = TypedDict(
    "DeleteFilterRequestRequestTypeDef",
    {
        "arn": str,
    },
)

DeleteFilterResponseTypeDef = TypedDict(
    "DeleteFilterResponseTypeDef",
    {
        "arn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DisableDelegatedAdminAccountRequestRequestTypeDef = TypedDict(
    "DisableDelegatedAdminAccountRequestRequestTypeDef",
    {
        "delegatedAdminAccountId": str,
    },
)

DisableDelegatedAdminAccountResponseTypeDef = TypedDict(
    "DisableDelegatedAdminAccountResponseTypeDef",
    {
        "delegatedAdminAccountId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DisableRequestRequestTypeDef = TypedDict(
    "DisableRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
        "resourceTypes": Sequence[ResourceScanTypeType],
    },
    total=False,
)

DisassociateMemberRequestRequestTypeDef = TypedDict(
    "DisassociateMemberRequestRequestTypeDef",
    {
        "accountId": str,
    },
)

DisassociateMemberResponseTypeDef = TypedDict(
    "DisassociateMemberResponseTypeDef",
    {
        "accountId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredMapFilterTypeDef = TypedDict(
    "_RequiredMapFilterTypeDef",
    {
        "comparison": Literal["EQUALS"],
        "key": str,
    },
)
_OptionalMapFilterTypeDef = TypedDict(
    "_OptionalMapFilterTypeDef",
    {
        "value": str,
    },
    total=False,
)


class MapFilterTypeDef(_RequiredMapFilterTypeDef, _OptionalMapFilterTypeDef):
    pass


Ec2MetadataTypeDef = TypedDict(
    "Ec2MetadataTypeDef",
    {
        "amiId": str,
        "platform": Ec2PlatformType,
        "tags": Dict[str, str],
    },
    total=False,
)

EcrRescanDurationStateTypeDef = TypedDict(
    "EcrRescanDurationStateTypeDef",
    {
        "rescanDuration": EcrRescanDurationType,
        "status": EcrRescanDurationStatusType,
        "updatedAt": datetime,
    },
    total=False,
)

EcrConfigurationTypeDef = TypedDict(
    "EcrConfigurationTypeDef",
    {
        "rescanDuration": EcrRescanDurationType,
    },
)

EcrContainerImageMetadataTypeDef = TypedDict(
    "EcrContainerImageMetadataTypeDef",
    {
        "tags": List[str],
    },
    total=False,
)

EcrRepositoryMetadataTypeDef = TypedDict(
    "EcrRepositoryMetadataTypeDef",
    {
        "name": str,
        "scanFrequency": EcrScanFrequencyType,
    },
    total=False,
)

_RequiredEnableDelegatedAdminAccountRequestRequestTypeDef = TypedDict(
    "_RequiredEnableDelegatedAdminAccountRequestRequestTypeDef",
    {
        "delegatedAdminAccountId": str,
    },
)
_OptionalEnableDelegatedAdminAccountRequestRequestTypeDef = TypedDict(
    "_OptionalEnableDelegatedAdminAccountRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class EnableDelegatedAdminAccountRequestRequestTypeDef(
    _RequiredEnableDelegatedAdminAccountRequestRequestTypeDef,
    _OptionalEnableDelegatedAdminAccountRequestRequestTypeDef,
):
    pass


EnableDelegatedAdminAccountResponseTypeDef = TypedDict(
    "EnableDelegatedAdminAccountResponseTypeDef",
    {
        "delegatedAdminAccountId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredEnableRequestRequestTypeDef = TypedDict(
    "_RequiredEnableRequestRequestTypeDef",
    {
        "resourceTypes": Sequence[ResourceScanTypeType],
    },
)
_OptionalEnableRequestRequestTypeDef = TypedDict(
    "_OptionalEnableRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
        "clientToken": str,
    },
    total=False,
)


class EnableRequestRequestTypeDef(
    _RequiredEnableRequestRequestTypeDef, _OptionalEnableRequestRequestTypeDef
):
    pass


EpssTypeDef = TypedDict(
    "EpssTypeDef",
    {
        "score": float,
    },
    total=False,
)

ExploitObservedTypeDef = TypedDict(
    "ExploitObservedTypeDef",
    {
        "firstSeen": datetime,
        "lastSeen": datetime,
    },
    total=False,
)

ExploitabilityDetailsTypeDef = TypedDict(
    "ExploitabilityDetailsTypeDef",
    {
        "lastKnownExploitAt": datetime,
    },
    total=False,
)

NumberFilterTypeDef = TypedDict(
    "NumberFilterTypeDef",
    {
        "lowerInclusive": float,
        "upperInclusive": float,
    },
    total=False,
)

PortRangeFilterTypeDef = TypedDict(
    "PortRangeFilterTypeDef",
    {
        "beginInclusive": int,
        "endInclusive": int,
    },
    total=False,
)

FreeTrialInfoTypeDef = TypedDict(
    "FreeTrialInfoTypeDef",
    {
        "end": datetime,
        "start": datetime,
        "status": FreeTrialStatusType,
        "type": FreeTrialTypeType,
    },
)

GetEc2DeepInspectionConfigurationResponseTypeDef = TypedDict(
    "GetEc2DeepInspectionConfigurationResponseTypeDef",
    {
        "errorMessage": str,
        "orgPackagePaths": List[str],
        "packagePaths": List[str],
        "status": Ec2DeepInspectionStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetFindingsReportStatusRequestRequestTypeDef = TypedDict(
    "GetFindingsReportStatusRequestRequestTypeDef",
    {
        "reportId": str,
    },
    total=False,
)

GetMemberRequestRequestTypeDef = TypedDict(
    "GetMemberRequestRequestTypeDef",
    {
        "accountId": str,
    },
)

MemberTypeDef = TypedDict(
    "MemberTypeDef",
    {
        "accountId": str,
        "delegatedAdminAccountId": str,
        "relationshipStatus": RelationshipStatusType,
        "updatedAt": datetime,
    },
    total=False,
)

LambdaFunctionMetadataTypeDef = TypedDict(
    "LambdaFunctionMetadataTypeDef",
    {
        "functionName": str,
        "functionTags": Dict[str, str],
        "layers": List[str],
        "runtime": RuntimeType,
    },
    total=False,
)

ListAccountPermissionsRequestListAccountPermissionsPaginateTypeDef = TypedDict(
    "ListAccountPermissionsRequestListAccountPermissionsPaginateTypeDef",
    {
        "service": ServiceType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListAccountPermissionsRequestRequestTypeDef = TypedDict(
    "ListAccountPermissionsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "service": ServiceType,
    },
    total=False,
)

PermissionTypeDef = TypedDict(
    "PermissionTypeDef",
    {
        "operation": OperationType,
        "service": ServiceType,
    },
)

ListDelegatedAdminAccountsRequestListDelegatedAdminAccountsPaginateTypeDef = TypedDict(
    "ListDelegatedAdminAccountsRequestListDelegatedAdminAccountsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDelegatedAdminAccountsRequestRequestTypeDef = TypedDict(
    "ListDelegatedAdminAccountsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListFiltersRequestListFiltersPaginateTypeDef = TypedDict(
    "ListFiltersRequestListFiltersPaginateTypeDef",
    {
        "action": FilterActionType,
        "arns": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListFiltersRequestRequestTypeDef = TypedDict(
    "ListFiltersRequestRequestTypeDef",
    {
        "action": FilterActionType,
        "arns": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

SortCriteriaTypeDef = TypedDict(
    "SortCriteriaTypeDef",
    {
        "field": SortFieldType,
        "sortOrder": SortOrderType,
    },
)

ListMembersRequestListMembersPaginateTypeDef = TypedDict(
    "ListMembersRequestListMembersPaginateTypeDef",
    {
        "onlyAssociated": bool,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListMembersRequestRequestTypeDef = TypedDict(
    "ListMembersRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "onlyAssociated": bool,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListUsageTotalsRequestListUsageTotalsPaginateTypeDef = TypedDict(
    "ListUsageTotalsRequestListUsageTotalsPaginateTypeDef",
    {
        "accountIds": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListUsageTotalsRequestRequestTypeDef = TypedDict(
    "ListUsageTotalsRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

StepTypeDef = TypedDict(
    "StepTypeDef",
    {
        "componentId": str,
        "componentType": str,
    },
)

PortRangeTypeDef = TypedDict(
    "PortRangeTypeDef",
    {
        "begin": int,
        "end": int,
    },
)

_RequiredVulnerablePackageTypeDef = TypedDict(
    "_RequiredVulnerablePackageTypeDef",
    {
        "name": str,
        "version": str,
    },
)
_OptionalVulnerablePackageTypeDef = TypedDict(
    "_OptionalVulnerablePackageTypeDef",
    {
        "arch": str,
        "epoch": int,
        "filePath": str,
        "fixedInVersion": str,
        "packageManager": PackageManagerType,
        "release": str,
        "remediation": str,
        "sourceLambdaLayerArn": str,
        "sourceLayerHash": str,
    },
    total=False,
)


class VulnerablePackageTypeDef(
    _RequiredVulnerablePackageTypeDef, _OptionalVulnerablePackageTypeDef
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

RecommendationTypeDef = TypedDict(
    "RecommendationTypeDef",
    {
        "Url": str,
        "text": str,
    },
    total=False,
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

SearchVulnerabilitiesFilterCriteriaTypeDef = TypedDict(
    "SearchVulnerabilitiesFilterCriteriaTypeDef",
    {
        "vulnerabilityIds": Sequence[str],
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

UpdateEc2DeepInspectionConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateEc2DeepInspectionConfigurationRequestRequestTypeDef",
    {
        "activateDeepInspection": bool,
        "packagePaths": Sequence[str],
    },
    total=False,
)

UpdateEc2DeepInspectionConfigurationResponseTypeDef = TypedDict(
    "UpdateEc2DeepInspectionConfigurationResponseTypeDef",
    {
        "errorMessage": str,
        "orgPackagePaths": List[str],
        "packagePaths": List[str],
        "status": Ec2DeepInspectionStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateFilterResponseTypeDef = TypedDict(
    "UpdateFilterResponseTypeDef",
    {
        "arn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateOrgEc2DeepInspectionConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateOrgEc2DeepInspectionConfigurationRequestRequestTypeDef",
    {
        "orgPackagePaths": Sequence[str],
    },
)

UsageTypeDef = TypedDict(
    "UsageTypeDef",
    {
        "currency": Literal["USD"],
        "estimatedMonthlyCost": float,
        "total": float,
        "type": UsageTypeType,
    },
    total=False,
)

AccountAggregationResponseTypeDef = TypedDict(
    "AccountAggregationResponseTypeDef",
    {
        "accountId": str,
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)

_RequiredAmiAggregationResponseTypeDef = TypedDict(
    "_RequiredAmiAggregationResponseTypeDef",
    {
        "ami": str,
    },
)
_OptionalAmiAggregationResponseTypeDef = TypedDict(
    "_OptionalAmiAggregationResponseTypeDef",
    {
        "accountId": str,
        "affectedInstances": int,
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)


class AmiAggregationResponseTypeDef(
    _RequiredAmiAggregationResponseTypeDef, _OptionalAmiAggregationResponseTypeDef
):
    pass


_RequiredAwsEcrContainerAggregationResponseTypeDef = TypedDict(
    "_RequiredAwsEcrContainerAggregationResponseTypeDef",
    {
        "resourceId": str,
    },
)
_OptionalAwsEcrContainerAggregationResponseTypeDef = TypedDict(
    "_OptionalAwsEcrContainerAggregationResponseTypeDef",
    {
        "accountId": str,
        "architecture": str,
        "imageSha": str,
        "imageTags": List[str],
        "repository": str,
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)


class AwsEcrContainerAggregationResponseTypeDef(
    _RequiredAwsEcrContainerAggregationResponseTypeDef,
    _OptionalAwsEcrContainerAggregationResponseTypeDef,
):
    pass


_RequiredEc2InstanceAggregationResponseTypeDef = TypedDict(
    "_RequiredEc2InstanceAggregationResponseTypeDef",
    {
        "instanceId": str,
    },
)
_OptionalEc2InstanceAggregationResponseTypeDef = TypedDict(
    "_OptionalEc2InstanceAggregationResponseTypeDef",
    {
        "accountId": str,
        "ami": str,
        "instanceTags": Dict[str, str],
        "networkFindings": int,
        "operatingSystem": str,
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)


class Ec2InstanceAggregationResponseTypeDef(
    _RequiredEc2InstanceAggregationResponseTypeDef, _OptionalEc2InstanceAggregationResponseTypeDef
):
    pass


FindingTypeAggregationResponseTypeDef = TypedDict(
    "FindingTypeAggregationResponseTypeDef",
    {
        "accountId": str,
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)

_RequiredImageLayerAggregationResponseTypeDef = TypedDict(
    "_RequiredImageLayerAggregationResponseTypeDef",
    {
        "accountId": str,
        "layerHash": str,
        "repository": str,
        "resourceId": str,
    },
)
_OptionalImageLayerAggregationResponseTypeDef = TypedDict(
    "_OptionalImageLayerAggregationResponseTypeDef",
    {
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)


class ImageLayerAggregationResponseTypeDef(
    _RequiredImageLayerAggregationResponseTypeDef, _OptionalImageLayerAggregationResponseTypeDef
):
    pass


_RequiredLambdaFunctionAggregationResponseTypeDef = TypedDict(
    "_RequiredLambdaFunctionAggregationResponseTypeDef",
    {
        "resourceId": str,
    },
)
_OptionalLambdaFunctionAggregationResponseTypeDef = TypedDict(
    "_OptionalLambdaFunctionAggregationResponseTypeDef",
    {
        "accountId": str,
        "functionName": str,
        "lambdaTags": Dict[str, str],
        "lastModifiedAt": datetime,
        "runtime": str,
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)


class LambdaFunctionAggregationResponseTypeDef(
    _RequiredLambdaFunctionAggregationResponseTypeDef,
    _OptionalLambdaFunctionAggregationResponseTypeDef,
):
    pass


_RequiredLambdaLayerAggregationResponseTypeDef = TypedDict(
    "_RequiredLambdaLayerAggregationResponseTypeDef",
    {
        "accountId": str,
        "functionName": str,
        "layerArn": str,
        "resourceId": str,
    },
)
_OptionalLambdaLayerAggregationResponseTypeDef = TypedDict(
    "_OptionalLambdaLayerAggregationResponseTypeDef",
    {
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)


class LambdaLayerAggregationResponseTypeDef(
    _RequiredLambdaLayerAggregationResponseTypeDef, _OptionalLambdaLayerAggregationResponseTypeDef
):
    pass


_RequiredPackageAggregationResponseTypeDef = TypedDict(
    "_RequiredPackageAggregationResponseTypeDef",
    {
        "packageName": str,
    },
)
_OptionalPackageAggregationResponseTypeDef = TypedDict(
    "_OptionalPackageAggregationResponseTypeDef",
    {
        "accountId": str,
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)


class PackageAggregationResponseTypeDef(
    _RequiredPackageAggregationResponseTypeDef, _OptionalPackageAggregationResponseTypeDef
):
    pass


_RequiredRepositoryAggregationResponseTypeDef = TypedDict(
    "_RequiredRepositoryAggregationResponseTypeDef",
    {
        "repository": str,
    },
)
_OptionalRepositoryAggregationResponseTypeDef = TypedDict(
    "_OptionalRepositoryAggregationResponseTypeDef",
    {
        "accountId": str,
        "affectedImages": int,
        "severityCounts": SeverityCountsTypeDef,
    },
    total=False,
)


class RepositoryAggregationResponseTypeDef(
    _RequiredRepositoryAggregationResponseTypeDef, _OptionalRepositoryAggregationResponseTypeDef
):
    pass


_RequiredTitleAggregationResponseTypeDef = TypedDict(
    "_RequiredTitleAggregationResponseTypeDef",
    {
        "title": str,
    },
)
_OptionalTitleAggregationResponseTypeDef = TypedDict(
    "_OptionalTitleAggregationResponseTypeDef",
    {
        "accountId": str,
        "severityCounts": SeverityCountsTypeDef,
        "vulnerabilityId": str,
    },
    total=False,
)


class TitleAggregationResponseTypeDef(
    _RequiredTitleAggregationResponseTypeDef, _OptionalTitleAggregationResponseTypeDef
):
    pass


_RequiredResourceStateTypeDef = TypedDict(
    "_RequiredResourceStateTypeDef",
    {
        "ec2": StateTypeDef,
        "ecr": StateTypeDef,
    },
)
_OptionalResourceStateTypeDef = TypedDict(
    "_OptionalResourceStateTypeDef",
    {
        "lambda": StateTypeDef,
    },
    total=False,
)


class ResourceStateTypeDef(_RequiredResourceStateTypeDef, _OptionalResourceStateTypeDef):
    pass


AccountTypeDef = TypedDict(
    "AccountTypeDef",
    {
        "accountId": str,
        "resourceStatus": ResourceStatusTypeDef,
        "status": StatusType,
    },
)

_RequiredFailedAccountTypeDef = TypedDict(
    "_RequiredFailedAccountTypeDef",
    {
        "accountId": str,
        "errorCode": ErrorCodeType,
        "errorMessage": str,
    },
)
_OptionalFailedAccountTypeDef = TypedDict(
    "_OptionalFailedAccountTypeDef",
    {
        "resourceStatus": ResourceStatusTypeDef,
        "status": StatusType,
    },
    total=False,
)


class FailedAccountTypeDef(_RequiredFailedAccountTypeDef, _OptionalFailedAccountTypeDef):
    pass


AmiAggregationTypeDef = TypedDict(
    "AmiAggregationTypeDef",
    {
        "amis": Sequence[StringFilterTypeDef],
        "sortBy": AmiSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

AwsEcrContainerAggregationTypeDef = TypedDict(
    "AwsEcrContainerAggregationTypeDef",
    {
        "architectures": Sequence[StringFilterTypeDef],
        "imageShas": Sequence[StringFilterTypeDef],
        "imageTags": Sequence[StringFilterTypeDef],
        "repositories": Sequence[StringFilterTypeDef],
        "resourceIds": Sequence[StringFilterTypeDef],
        "sortBy": AwsEcrContainerSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

ImageLayerAggregationTypeDef = TypedDict(
    "ImageLayerAggregationTypeDef",
    {
        "layerHashes": Sequence[StringFilterTypeDef],
        "repositories": Sequence[StringFilterTypeDef],
        "resourceIds": Sequence[StringFilterTypeDef],
        "sortBy": ImageLayerSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

LambdaLayerAggregationTypeDef = TypedDict(
    "LambdaLayerAggregationTypeDef",
    {
        "functionNames": Sequence[StringFilterTypeDef],
        "layerArns": Sequence[StringFilterTypeDef],
        "resourceIds": Sequence[StringFilterTypeDef],
        "sortBy": LambdaLayerSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

PackageAggregationTypeDef = TypedDict(
    "PackageAggregationTypeDef",
    {
        "packageNames": Sequence[StringFilterTypeDef],
        "sortBy": PackageSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

RepositoryAggregationTypeDef = TypedDict(
    "RepositoryAggregationTypeDef",
    {
        "repositories": Sequence[StringFilterTypeDef],
        "sortBy": RepositorySortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

TitleAggregationTypeDef = TypedDict(
    "TitleAggregationTypeDef",
    {
        "resourceType": AggregationResourceTypeType,
        "sortBy": TitleSortByType,
        "sortOrder": SortOrderType,
        "titles": Sequence[StringFilterTypeDef],
        "vulnerabilityIds": Sequence[StringFilterTypeDef],
    },
    total=False,
)

DescribeOrganizationConfigurationResponseTypeDef = TypedDict(
    "DescribeOrganizationConfigurationResponseTypeDef",
    {
        "autoEnable": AutoEnableTypeDef,
        "maxAccountLimitReached": bool,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateOrganizationConfigurationRequestRequestTypeDef",
    {
        "autoEnable": AutoEnableTypeDef,
    },
)

UpdateOrganizationConfigurationResponseTypeDef = TypedDict(
    "UpdateOrganizationConfigurationResponseTypeDef",
    {
        "autoEnable": AutoEnableTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredAwsLambdaFunctionDetailsTypeDef = TypedDict(
    "_RequiredAwsLambdaFunctionDetailsTypeDef",
    {
        "codeSha256": str,
        "executionRoleArn": str,
        "functionName": str,
        "runtime": RuntimeType,
        "version": str,
    },
)
_OptionalAwsLambdaFunctionDetailsTypeDef = TypedDict(
    "_OptionalAwsLambdaFunctionDetailsTypeDef",
    {
        "architectures": List[ArchitectureType],
        "lastModifiedAt": datetime,
        "layers": List[str],
        "packageType": PackageTypeType,
        "vpcConfig": LambdaVpcConfigTypeDef,
    },
    total=False,
)


class AwsLambdaFunctionDetailsTypeDef(
    _RequiredAwsLambdaFunctionDetailsTypeDef, _OptionalAwsLambdaFunctionDetailsTypeDef
):
    pass


BatchGetMemberEc2DeepInspectionStatusResponseTypeDef = TypedDict(
    "BatchGetMemberEc2DeepInspectionStatusResponseTypeDef",
    {
        "accountIds": List[MemberAccountEc2DeepInspectionStatusStateTypeDef],
        "failedAccountIds": List[FailedMemberAccountEc2DeepInspectionStatusStateTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchUpdateMemberEc2DeepInspectionStatusResponseTypeDef = TypedDict(
    "BatchUpdateMemberEc2DeepInspectionStatusResponseTypeDef",
    {
        "accountIds": List[MemberAccountEc2DeepInspectionStatusStateTypeDef],
        "failedAccountIds": List[FailedMemberAccountEc2DeepInspectionStatusStateTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchUpdateMemberEc2DeepInspectionStatusRequestRequestTypeDef = TypedDict(
    "BatchUpdateMemberEc2DeepInspectionStatusRequestRequestTypeDef",
    {
        "accountIds": Sequence[MemberAccountEc2DeepInspectionStatusTypeDef],
    },
)

ListCoverageStatisticsResponseTypeDef = TypedDict(
    "ListCoverageStatisticsResponseTypeDef",
    {
        "countsByGroup": List[CountsTypeDef],
        "nextToken": str,
        "totalCounts": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CoverageFilterCriteriaTypeDef = TypedDict(
    "CoverageFilterCriteriaTypeDef",
    {
        "accountId": Sequence[CoverageStringFilterTypeDef],
        "ec2InstanceTags": Sequence[CoverageMapFilterTypeDef],
        "ecrImageTags": Sequence[CoverageStringFilterTypeDef],
        "ecrRepositoryName": Sequence[CoverageStringFilterTypeDef],
        "lambdaFunctionName": Sequence[CoverageStringFilterTypeDef],
        "lambdaFunctionRuntime": Sequence[CoverageStringFilterTypeDef],
        "lambdaFunctionTags": Sequence[CoverageMapFilterTypeDef],
        "lastScannedAt": Sequence[CoverageDateFilterTypeDef],
        "resourceId": Sequence[CoverageStringFilterTypeDef],
        "resourceType": Sequence[CoverageStringFilterTypeDef],
        "scanStatusCode": Sequence[CoverageStringFilterTypeDef],
        "scanStatusReason": Sequence[CoverageStringFilterTypeDef],
        "scanType": Sequence[CoverageStringFilterTypeDef],
    },
    total=False,
)

_RequiredCvssScoreDetailsTypeDef = TypedDict(
    "_RequiredCvssScoreDetailsTypeDef",
    {
        "score": float,
        "scoreSource": str,
        "scoringVector": str,
        "version": str,
    },
)
_OptionalCvssScoreDetailsTypeDef = TypedDict(
    "_OptionalCvssScoreDetailsTypeDef",
    {
        "adjustments": List[CvssScoreAdjustmentTypeDef],
        "cvssSource": str,
    },
    total=False,
)


class CvssScoreDetailsTypeDef(_RequiredCvssScoreDetailsTypeDef, _OptionalCvssScoreDetailsTypeDef):
    pass


ListDelegatedAdminAccountsResponseTypeDef = TypedDict(
    "ListDelegatedAdminAccountsResponseTypeDef",
    {
        "delegatedAdminAccounts": List[DelegatedAdminAccountTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetDelegatedAdminAccountResponseTypeDef = TypedDict(
    "GetDelegatedAdminAccountResponseTypeDef",
    {
        "delegatedAdmin": DelegatedAdminTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

Ec2InstanceAggregationTypeDef = TypedDict(
    "Ec2InstanceAggregationTypeDef",
    {
        "amis": Sequence[StringFilterTypeDef],
        "instanceIds": Sequence[StringFilterTypeDef],
        "instanceTags": Sequence[MapFilterTypeDef],
        "operatingSystems": Sequence[StringFilterTypeDef],
        "sortBy": Ec2InstanceSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

LambdaFunctionAggregationTypeDef = TypedDict(
    "LambdaFunctionAggregationTypeDef",
    {
        "functionNames": Sequence[StringFilterTypeDef],
        "functionTags": Sequence[MapFilterTypeDef],
        "resourceIds": Sequence[StringFilterTypeDef],
        "runtimes": Sequence[StringFilterTypeDef],
        "sortBy": LambdaFunctionSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

EcrConfigurationStateTypeDef = TypedDict(
    "EcrConfigurationStateTypeDef",
    {
        "rescanDurationState": EcrRescanDurationStateTypeDef,
    },
    total=False,
)

UpdateConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateConfigurationRequestRequestTypeDef",
    {
        "ecrConfiguration": EcrConfigurationTypeDef,
    },
)

_RequiredVulnerabilityTypeDef = TypedDict(
    "_RequiredVulnerabilityTypeDef",
    {
        "id": str,
    },
)
_OptionalVulnerabilityTypeDef = TypedDict(
    "_OptionalVulnerabilityTypeDef",
    {
        "atigData": AtigDataTypeDef,
        "cisaData": CisaDataTypeDef,
        "cvss2": Cvss2TypeDef,
        "cvss3": Cvss3TypeDef,
        "cwes": List[str],
        "description": str,
        "detectionPlatforms": List[str],
        "epss": EpssTypeDef,
        "exploitObserved": ExploitObservedTypeDef,
        "referenceUrls": List[str],
        "relatedVulnerabilities": List[str],
        "source": Literal["NVD"],
        "sourceUrl": str,
        "vendorCreatedAt": datetime,
        "vendorSeverity": str,
        "vendorUpdatedAt": datetime,
    },
    total=False,
)


class VulnerabilityTypeDef(_RequiredVulnerabilityTypeDef, _OptionalVulnerabilityTypeDef):
    pass


PackageFilterTypeDef = TypedDict(
    "PackageFilterTypeDef",
    {
        "architecture": StringFilterTypeDef,
        "epoch": NumberFilterTypeDef,
        "name": StringFilterTypeDef,
        "release": StringFilterTypeDef,
        "sourceLambdaLayerArn": StringFilterTypeDef,
        "sourceLayerHash": StringFilterTypeDef,
        "version": StringFilterTypeDef,
    },
    total=False,
)

FreeTrialAccountInfoTypeDef = TypedDict(
    "FreeTrialAccountInfoTypeDef",
    {
        "accountId": str,
        "freeTrialInfo": List[FreeTrialInfoTypeDef],
    },
)

GetMemberResponseTypeDef = TypedDict(
    "GetMemberResponseTypeDef",
    {
        "member": MemberTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListMembersResponseTypeDef = TypedDict(
    "ListMembersResponseTypeDef",
    {
        "members": List[MemberTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ResourceScanMetadataTypeDef = TypedDict(
    "ResourceScanMetadataTypeDef",
    {
        "ec2": Ec2MetadataTypeDef,
        "ecrImage": EcrContainerImageMetadataTypeDef,
        "ecrRepository": EcrRepositoryMetadataTypeDef,
        "lambdaFunction": LambdaFunctionMetadataTypeDef,
    },
    total=False,
)

ListAccountPermissionsResponseTypeDef = TypedDict(
    "ListAccountPermissionsResponseTypeDef",
    {
        "nextToken": str,
        "permissions": List[PermissionTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

NetworkPathTypeDef = TypedDict(
    "NetworkPathTypeDef",
    {
        "steps": List[StepTypeDef],
    },
    total=False,
)

_RequiredPackageVulnerabilityDetailsTypeDef = TypedDict(
    "_RequiredPackageVulnerabilityDetailsTypeDef",
    {
        "source": str,
        "vulnerabilityId": str,
    },
)
_OptionalPackageVulnerabilityDetailsTypeDef = TypedDict(
    "_OptionalPackageVulnerabilityDetailsTypeDef",
    {
        "cvss": List[CvssScoreTypeDef],
        "referenceUrls": List[str],
        "relatedVulnerabilities": List[str],
        "sourceUrl": str,
        "vendorCreatedAt": datetime,
        "vendorSeverity": str,
        "vendorUpdatedAt": datetime,
        "vulnerablePackages": List[VulnerablePackageTypeDef],
    },
    total=False,
)


class PackageVulnerabilityDetailsTypeDef(
    _RequiredPackageVulnerabilityDetailsTypeDef, _OptionalPackageVulnerabilityDetailsTypeDef
):
    pass


RemediationTypeDef = TypedDict(
    "RemediationTypeDef",
    {
        "recommendation": RecommendationTypeDef,
    },
    total=False,
)

_RequiredSearchVulnerabilitiesRequestRequestTypeDef = TypedDict(
    "_RequiredSearchVulnerabilitiesRequestRequestTypeDef",
    {
        "filterCriteria": SearchVulnerabilitiesFilterCriteriaTypeDef,
    },
)
_OptionalSearchVulnerabilitiesRequestRequestTypeDef = TypedDict(
    "_OptionalSearchVulnerabilitiesRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class SearchVulnerabilitiesRequestRequestTypeDef(
    _RequiredSearchVulnerabilitiesRequestRequestTypeDef,
    _OptionalSearchVulnerabilitiesRequestRequestTypeDef,
):
    pass


_RequiredSearchVulnerabilitiesRequestSearchVulnerabilitiesPaginateTypeDef = TypedDict(
    "_RequiredSearchVulnerabilitiesRequestSearchVulnerabilitiesPaginateTypeDef",
    {
        "filterCriteria": SearchVulnerabilitiesFilterCriteriaTypeDef,
    },
)
_OptionalSearchVulnerabilitiesRequestSearchVulnerabilitiesPaginateTypeDef = TypedDict(
    "_OptionalSearchVulnerabilitiesRequestSearchVulnerabilitiesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class SearchVulnerabilitiesRequestSearchVulnerabilitiesPaginateTypeDef(
    _RequiredSearchVulnerabilitiesRequestSearchVulnerabilitiesPaginateTypeDef,
    _OptionalSearchVulnerabilitiesRequestSearchVulnerabilitiesPaginateTypeDef,
):
    pass


UsageTotalTypeDef = TypedDict(
    "UsageTotalTypeDef",
    {
        "accountId": str,
        "usage": List[UsageTypeDef],
    },
    total=False,
)

AggregationResponseTypeDef = TypedDict(
    "AggregationResponseTypeDef",
    {
        "accountAggregation": AccountAggregationResponseTypeDef,
        "amiAggregation": AmiAggregationResponseTypeDef,
        "awsEcrContainerAggregation": AwsEcrContainerAggregationResponseTypeDef,
        "ec2InstanceAggregation": Ec2InstanceAggregationResponseTypeDef,
        "findingTypeAggregation": FindingTypeAggregationResponseTypeDef,
        "imageLayerAggregation": ImageLayerAggregationResponseTypeDef,
        "lambdaFunctionAggregation": LambdaFunctionAggregationResponseTypeDef,
        "lambdaLayerAggregation": LambdaLayerAggregationResponseTypeDef,
        "packageAggregation": PackageAggregationResponseTypeDef,
        "repositoryAggregation": RepositoryAggregationResponseTypeDef,
        "titleAggregation": TitleAggregationResponseTypeDef,
    },
    total=False,
)

AccountStateTypeDef = TypedDict(
    "AccountStateTypeDef",
    {
        "accountId": str,
        "resourceState": ResourceStateTypeDef,
        "state": StateTypeDef,
    },
)

DisableResponseTypeDef = TypedDict(
    "DisableResponseTypeDef",
    {
        "accounts": List[AccountTypeDef],
        "failedAccounts": List[FailedAccountTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EnableResponseTypeDef = TypedDict(
    "EnableResponseTypeDef",
    {
        "accounts": List[AccountTypeDef],
        "failedAccounts": List[FailedAccountTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ResourceDetailsTypeDef = TypedDict(
    "ResourceDetailsTypeDef",
    {
        "awsEc2Instance": AwsEc2InstanceDetailsTypeDef,
        "awsEcrContainerImage": AwsEcrContainerImageDetailsTypeDef,
        "awsLambdaFunction": AwsLambdaFunctionDetailsTypeDef,
    },
    total=False,
)

ListCoverageRequestListCoveragePaginateTypeDef = TypedDict(
    "ListCoverageRequestListCoveragePaginateTypeDef",
    {
        "filterCriteria": CoverageFilterCriteriaTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListCoverageRequestRequestTypeDef = TypedDict(
    "ListCoverageRequestRequestTypeDef",
    {
        "filterCriteria": CoverageFilterCriteriaTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListCoverageStatisticsRequestListCoverageStatisticsPaginateTypeDef = TypedDict(
    "ListCoverageStatisticsRequestListCoverageStatisticsPaginateTypeDef",
    {
        "filterCriteria": CoverageFilterCriteriaTypeDef,
        "groupBy": GroupKeyType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListCoverageStatisticsRequestRequestTypeDef = TypedDict(
    "ListCoverageStatisticsRequestRequestTypeDef",
    {
        "filterCriteria": CoverageFilterCriteriaTypeDef,
        "groupBy": GroupKeyType,
        "nextToken": str,
    },
    total=False,
)

InspectorScoreDetailsTypeDef = TypedDict(
    "InspectorScoreDetailsTypeDef",
    {
        "adjustedCvss": CvssScoreDetailsTypeDef,
    },
    total=False,
)

AggregationRequestTypeDef = TypedDict(
    "AggregationRequestTypeDef",
    {
        "accountAggregation": AccountAggregationTypeDef,
        "amiAggregation": AmiAggregationTypeDef,
        "awsEcrContainerAggregation": AwsEcrContainerAggregationTypeDef,
        "ec2InstanceAggregation": Ec2InstanceAggregationTypeDef,
        "findingTypeAggregation": FindingTypeAggregationTypeDef,
        "imageLayerAggregation": ImageLayerAggregationTypeDef,
        "lambdaFunctionAggregation": LambdaFunctionAggregationTypeDef,
        "lambdaLayerAggregation": LambdaLayerAggregationTypeDef,
        "packageAggregation": PackageAggregationTypeDef,
        "repositoryAggregation": RepositoryAggregationTypeDef,
        "titleAggregation": TitleAggregationTypeDef,
    },
    total=False,
)

GetConfigurationResponseTypeDef = TypedDict(
    "GetConfigurationResponseTypeDef",
    {
        "ecrConfiguration": EcrConfigurationStateTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SearchVulnerabilitiesResponseTypeDef = TypedDict(
    "SearchVulnerabilitiesResponseTypeDef",
    {
        "nextToken": str,
        "vulnerabilities": List[VulnerabilityTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FilterCriteriaTypeDef = TypedDict(
    "FilterCriteriaTypeDef",
    {
        "awsAccountId": Sequence[StringFilterTypeDef],
        "componentId": Sequence[StringFilterTypeDef],
        "componentType": Sequence[StringFilterTypeDef],
        "ec2InstanceImageId": Sequence[StringFilterTypeDef],
        "ec2InstanceSubnetId": Sequence[StringFilterTypeDef],
        "ec2InstanceVpcId": Sequence[StringFilterTypeDef],
        "ecrImageArchitecture": Sequence[StringFilterTypeDef],
        "ecrImageHash": Sequence[StringFilterTypeDef],
        "ecrImagePushedAt": Sequence[DateFilterTypeDef],
        "ecrImageRegistry": Sequence[StringFilterTypeDef],
        "ecrImageRepositoryName": Sequence[StringFilterTypeDef],
        "ecrImageTags": Sequence[StringFilterTypeDef],
        "exploitAvailable": Sequence[StringFilterTypeDef],
        "findingArn": Sequence[StringFilterTypeDef],
        "findingStatus": Sequence[StringFilterTypeDef],
        "findingType": Sequence[StringFilterTypeDef],
        "firstObservedAt": Sequence[DateFilterTypeDef],
        "fixAvailable": Sequence[StringFilterTypeDef],
        "inspectorScore": Sequence[NumberFilterTypeDef],
        "lambdaFunctionExecutionRoleArn": Sequence[StringFilterTypeDef],
        "lambdaFunctionLastModifiedAt": Sequence[DateFilterTypeDef],
        "lambdaFunctionLayers": Sequence[StringFilterTypeDef],
        "lambdaFunctionName": Sequence[StringFilterTypeDef],
        "lambdaFunctionRuntime": Sequence[StringFilterTypeDef],
        "lastObservedAt": Sequence[DateFilterTypeDef],
        "networkProtocol": Sequence[StringFilterTypeDef],
        "portRange": Sequence[PortRangeFilterTypeDef],
        "relatedVulnerabilities": Sequence[StringFilterTypeDef],
        "resourceId": Sequence[StringFilterTypeDef],
        "resourceTags": Sequence[MapFilterTypeDef],
        "resourceType": Sequence[StringFilterTypeDef],
        "severity": Sequence[StringFilterTypeDef],
        "title": Sequence[StringFilterTypeDef],
        "updatedAt": Sequence[DateFilterTypeDef],
        "vendorSeverity": Sequence[StringFilterTypeDef],
        "vulnerabilityId": Sequence[StringFilterTypeDef],
        "vulnerabilitySource": Sequence[StringFilterTypeDef],
        "vulnerablePackages": Sequence[PackageFilterTypeDef],
    },
    total=False,
)

BatchGetFreeTrialInfoResponseTypeDef = TypedDict(
    "BatchGetFreeTrialInfoResponseTypeDef",
    {
        "accounts": List[FreeTrialAccountInfoTypeDef],
        "failedAccounts": List[FreeTrialInfoErrorTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCoveredResourceTypeDef = TypedDict(
    "_RequiredCoveredResourceTypeDef",
    {
        "accountId": str,
        "resourceId": str,
        "resourceType": CoverageResourceTypeType,
        "scanType": ScanTypeType,
    },
)
_OptionalCoveredResourceTypeDef = TypedDict(
    "_OptionalCoveredResourceTypeDef",
    {
        "lastScannedAt": datetime,
        "resourceMetadata": ResourceScanMetadataTypeDef,
        "scanStatus": ScanStatusTypeDef,
    },
    total=False,
)


class CoveredResourceTypeDef(_RequiredCoveredResourceTypeDef, _OptionalCoveredResourceTypeDef):
    pass


NetworkReachabilityDetailsTypeDef = TypedDict(
    "NetworkReachabilityDetailsTypeDef",
    {
        "networkPath": NetworkPathTypeDef,
        "openPortRange": PortRangeTypeDef,
        "protocol": NetworkProtocolType,
    },
)

ListUsageTotalsResponseTypeDef = TypedDict(
    "ListUsageTotalsResponseTypeDef",
    {
        "nextToken": str,
        "totals": List[UsageTotalTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListFindingAggregationsResponseTypeDef = TypedDict(
    "ListFindingAggregationsResponseTypeDef",
    {
        "aggregationType": AggregationTypeType,
        "nextToken": str,
        "responses": List[AggregationResponseTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchGetAccountStatusResponseTypeDef = TypedDict(
    "BatchGetAccountStatusResponseTypeDef",
    {
        "accounts": List[AccountStateTypeDef],
        "failedAccounts": List[FailedAccountTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredResourceTypeDef = TypedDict(
    "_RequiredResourceTypeDef",
    {
        "id": str,
        "type": ResourceTypeType,
    },
)
_OptionalResourceTypeDef = TypedDict(
    "_OptionalResourceTypeDef",
    {
        "details": ResourceDetailsTypeDef,
        "partition": str,
        "region": str,
        "tags": Dict[str, str],
    },
    total=False,
)


class ResourceTypeDef(_RequiredResourceTypeDef, _OptionalResourceTypeDef):
    pass


_RequiredListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef = TypedDict(
    "_RequiredListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef",
    {
        "aggregationType": AggregationTypeType,
    },
)
_OptionalListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef = TypedDict(
    "_OptionalListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef",
    {
        "accountIds": Sequence[StringFilterTypeDef],
        "aggregationRequest": AggregationRequestTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef(
    _RequiredListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef,
    _OptionalListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef,
):
    pass


_RequiredListFindingAggregationsRequestRequestTypeDef = TypedDict(
    "_RequiredListFindingAggregationsRequestRequestTypeDef",
    {
        "aggregationType": AggregationTypeType,
    },
)
_OptionalListFindingAggregationsRequestRequestTypeDef = TypedDict(
    "_OptionalListFindingAggregationsRequestRequestTypeDef",
    {
        "accountIds": Sequence[StringFilterTypeDef],
        "aggregationRequest": AggregationRequestTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListFindingAggregationsRequestRequestTypeDef(
    _RequiredListFindingAggregationsRequestRequestTypeDef,
    _OptionalListFindingAggregationsRequestRequestTypeDef,
):
    pass


_RequiredCreateFilterRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFilterRequestRequestTypeDef",
    {
        "action": FilterActionType,
        "filterCriteria": FilterCriteriaTypeDef,
        "name": str,
    },
)
_OptionalCreateFilterRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFilterRequestRequestTypeDef",
    {
        "description": str,
        "reason": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateFilterRequestRequestTypeDef(
    _RequiredCreateFilterRequestRequestTypeDef, _OptionalCreateFilterRequestRequestTypeDef
):
    pass


_RequiredCreateFindingsReportRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFindingsReportRequestRequestTypeDef",
    {
        "reportFormat": ReportFormatType,
        "s3Destination": DestinationTypeDef,
    },
)
_OptionalCreateFindingsReportRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFindingsReportRequestRequestTypeDef",
    {
        "filterCriteria": FilterCriteriaTypeDef,
    },
    total=False,
)


class CreateFindingsReportRequestRequestTypeDef(
    _RequiredCreateFindingsReportRequestRequestTypeDef,
    _OptionalCreateFindingsReportRequestRequestTypeDef,
):
    pass


_RequiredFilterTypeDef = TypedDict(
    "_RequiredFilterTypeDef",
    {
        "action": FilterActionType,
        "arn": str,
        "createdAt": datetime,
        "criteria": FilterCriteriaTypeDef,
        "name": str,
        "ownerId": str,
        "updatedAt": datetime,
    },
)
_OptionalFilterTypeDef = TypedDict(
    "_OptionalFilterTypeDef",
    {
        "description": str,
        "reason": str,
        "tags": Dict[str, str],
    },
    total=False,
)


class FilterTypeDef(_RequiredFilterTypeDef, _OptionalFilterTypeDef):
    pass


GetFindingsReportStatusResponseTypeDef = TypedDict(
    "GetFindingsReportStatusResponseTypeDef",
    {
        "destination": DestinationTypeDef,
        "errorCode": ReportingErrorCodeType,
        "errorMessage": str,
        "filterCriteria": FilterCriteriaTypeDef,
        "reportId": str,
        "status": ExternalReportStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListFindingsRequestListFindingsPaginateTypeDef = TypedDict(
    "ListFindingsRequestListFindingsPaginateTypeDef",
    {
        "filterCriteria": FilterCriteriaTypeDef,
        "sortCriteria": SortCriteriaTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListFindingsRequestRequestTypeDef = TypedDict(
    "ListFindingsRequestRequestTypeDef",
    {
        "filterCriteria": FilterCriteriaTypeDef,
        "maxResults": int,
        "nextToken": str,
        "sortCriteria": SortCriteriaTypeDef,
    },
    total=False,
)

_RequiredUpdateFilterRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFilterRequestRequestTypeDef",
    {
        "filterArn": str,
    },
)
_OptionalUpdateFilterRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFilterRequestRequestTypeDef",
    {
        "action": FilterActionType,
        "description": str,
        "filterCriteria": FilterCriteriaTypeDef,
        "name": str,
        "reason": str,
    },
    total=False,
)


class UpdateFilterRequestRequestTypeDef(
    _RequiredUpdateFilterRequestRequestTypeDef, _OptionalUpdateFilterRequestRequestTypeDef
):
    pass


ListCoverageResponseTypeDef = TypedDict(
    "ListCoverageResponseTypeDef",
    {
        "coveredResources": List[CoveredResourceTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredFindingTypeDef = TypedDict(
    "_RequiredFindingTypeDef",
    {
        "awsAccountId": str,
        "description": str,
        "findingArn": str,
        "firstObservedAt": datetime,
        "lastObservedAt": datetime,
        "remediation": RemediationTypeDef,
        "resources": List[ResourceTypeDef],
        "severity": SeverityType,
        "status": FindingStatusType,
        "type": FindingTypeType,
    },
)
_OptionalFindingTypeDef = TypedDict(
    "_OptionalFindingTypeDef",
    {
        "exploitAvailable": ExploitAvailableType,
        "exploitabilityDetails": ExploitabilityDetailsTypeDef,
        "fixAvailable": FixAvailableType,
        "inspectorScore": float,
        "inspectorScoreDetails": InspectorScoreDetailsTypeDef,
        "networkReachabilityDetails": NetworkReachabilityDetailsTypeDef,
        "packageVulnerabilityDetails": PackageVulnerabilityDetailsTypeDef,
        "title": str,
        "updatedAt": datetime,
    },
    total=False,
)


class FindingTypeDef(_RequiredFindingTypeDef, _OptionalFindingTypeDef):
    pass


ListFiltersResponseTypeDef = TypedDict(
    "ListFiltersResponseTypeDef",
    {
        "filters": List[FilterTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListFindingsResponseTypeDef = TypedDict(
    "ListFindingsResponseTypeDef",
    {
        "findings": List[FindingTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
