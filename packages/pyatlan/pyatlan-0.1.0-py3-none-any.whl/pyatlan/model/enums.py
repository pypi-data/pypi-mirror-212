# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)
from datetime import datetime
from enum import Enum


class ADLSEncryptionTypes(Enum):
    MICROSOFT_STORAGE = "Microsoft.Storage"
    MICROSOFT_KEYVAULT = "Microsoft.Keyvault"


class ADLSPerformance(Enum):
    STANDARD = "Standard"
    PREMIUM = "Premium"


class ADLSReplicationType(Enum):
    LRS = "LRS"
    ZRS = "ZRS"
    GRS = "GRS"
    GZRS = "GZRS"
    RA_GRS = "RA-GRS"


class ADLSAccountStatus(Enum):
    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"


class ADLSStorageKind(Enum):
    BLOB_STORAGE = "BlobStorage"
    BLOCK_BLOB_STORAGE = "BlockBlobStorage"
    FILE_STORAGE = "FileStorage"
    STORAGE = "Storage"
    STORAGE_V2 = "StorageV2"


class ADLSProvisionState(Enum):
    CREATING = "Creating"
    RESOLVING_DNS = "ResolvingDNS"
    SUCCEEDED = "Succeeded"


class ADLSAccessTier(Enum):
    COOL = "Cool"
    HOT = "Hot"
    ARCHIVE = "Archive"


class ADLSLeaseState(Enum):
    AVAILABLE = "Available"
    LEASED = "Leased"
    EXPIRED = "Expired"
    BREAKING = "Breaking"
    BROKEN = "Broken"


class ADLSLeaseStatus(Enum):
    LOCKED = "Locked"
    UNLOCKED = "Unlocked"


class ADLSObjectType(Enum):
    BLOCK_BLOB = "BlockBlob"
    PAGE_BLOB = "PageBlob"
    APPEND_BLOB = "AppendBlob"


class ADLSObjectArchiveStatus(Enum):
    REHYDRATE_PENDING_TO_HOT = "rehydrate-pending-to-hot"
    REHYDRATE_PENDING_TO_COOL = "rehydrate-pending-to-cool"


class AnnouncementType(Enum):
    INFORMATION = "information"
    WARNING = "warning"
    ISSUE = "issue"


class Cardinality(Enum):
    SINGLE = "SINGLE"
    LIST = "LIST"
    SET = "SET"


class CertificateStatus(Enum):
    VERIFIED = "VERIFIED"
    DRAFT = "DRAFT"
    DEPRECATED = "DEPRECATED"


class EntityStatus(Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"


class AtlanTypeCategory(Enum):
    ENUM = "ENUM"
    STRUCT = "STRUCT"
    CLASSIFICATION = "CLASSIFICATION"
    ENTITY = "ENTITY"
    RELATIONSHIP = "RELATIONSHIP"
    CUSTOM_METADATA = "BUSINESS_METADATA"


class TypeName(Enum):
    STRING = "string"
    ARRAY_STRING = "array<string>"


class IndexType(Enum):
    DEFAULT = "DEFAULT"
    STRING = "STRING"


class GoogleDatastudioAssetType(Enum):
    DATA_SOURCE = "DATA_SOURCE"
    REPORT = "REPORT"


class PowerbiEndorsement(Enum):
    PROMOTED = "Promoted"
    CERTIFIED = "Certified"


class QueryUsernameStrategy(Enum):
    CONNECTION_USERNAME = ("connectionUsername",)
    ATLAN_USERNAME = "atlanUsername"


class IconType(Enum):
    IMAGE = "Image"
    EMOJI = "Emoji"


class SourceCostUnitType(Enum):
    CREDITS = "Credits"


class AtlanDeleteType(Enum):
    HARD = "HARD"
    SOFT = "SOFT"


class KafkaTopicCompressionType(Enum):
    UNCOMPRESSED = "uncompressed"
    ZSTD = "zstd"
    LZ4 = "lz4"
    SNAPPY = "snappy"
    GZIP = "gzip"
    PRODUCER = "producer"


class KafkaTopicCleanupPolicy(Enum):
    COMPACT = "compact"
    DELETE = "delete"


class QuickSightFolderType(Enum):
    SHARED = "SHARED"


class QuickSightDatasetFieldType(Enum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    DATETIME = "DATETIME"


class QuickSightAnalysisStatus(Enum):
    CREATION_IN_PROGRESS = "CREATION_IN_PROGRESS"
    CREATION_SUCCESSFUL = "CREATION_SUCCESSFUL"
    CREATION_FAILED = "CREATION_FAILED"
    UPDATE_IN_PROGRESS = "UPDATE_IN_PROGRESS"
    UPDATE_SUCCESSFUL = "UPDATE_SUCCESSFUL"
    UPDATE_FAILED = "UPDATE_FAILED"
    DELETED = "DELETED"


class QuickSightDatasetImportMode(Enum):
    SPICE = "SPICE"
    DIRECT_QUERY = "DIRECT_QUERY"


class AtlanConnectionCategory(Enum):
    WAREHOUSE = "warehouse"
    BI = "bi"
    OBJECT_STORE = "ObjectStore"
    SAAS = "SaaS"
    LAKE = "lake"
    QUERY_ENGINE = "queryengine"
    ELT = "elt"
    DATABASE = "database"
    API = "API"
    EVENT_BUS = "eventbus"


class AtlanConnectorType(str, Enum):
    category: AtlanConnectionCategory

    @classmethod
    def _get_connector_type_from_qualified_name(
        cls, qualified_name: str
    ) -> "AtlanConnectorType":
        tokens = qualified_name.split("/")
        if len(tokens) > 1:
            return AtlanConnectorType[tokens[1].upper()]
        raise ValueError(
            f"Could not determine AtlanConnectorType from {qualified_name}"
        )

    def __new__(
        cls, value: str, category: AtlanConnectionCategory
    ) -> "AtlanConnectorType":
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.category = category
        return obj

    def to_qualified_name(self):
        return f"default/{self.value}/{int(datetime.now().timestamp() * 1000)}"

    SNOWFLAKE = ("snowflake", AtlanConnectionCategory.WAREHOUSE)
    TABLEAU = ("tableau", AtlanConnectionCategory.BI)
    REDSHIFT = ("redshift", AtlanConnectionCategory.WAREHOUSE)
    POSTGRES = ("postgres", AtlanConnectionCategory.DATABASE)
    ATHENA = ("athena", AtlanConnectionCategory.QUERY_ENGINE)
    DATABRICKS = ("databricks", AtlanConnectionCategory.LAKE)
    POWERBI = ("powerbi", AtlanConnectionCategory.BI)
    BIGQUERY = ("bigquery", AtlanConnectionCategory.WAREHOUSE)
    LOOKER = ("looker", AtlanConnectionCategory.BI)
    METABASE = ("metabase", AtlanConnectionCategory.BI)
    SALESFORCE = ("salesforce", AtlanConnectionCategory.SAAS)
    MYSQL = ("mysql", AtlanConnectionCategory.WAREHOUSE)
    MSSQL = ("mssql", AtlanConnectionCategory.WAREHOUSE)
    S3 = ("s3", AtlanConnectionCategory.OBJECT_STORE)
    PRESTO = ("presto", AtlanConnectionCategory.DATABASE)
    TRINO = ("trino", AtlanConnectionCategory.DATABASE)
    DATASTUDIO = ("datastudio", AtlanConnectionCategory.BI)
    GLUE = ("glue", AtlanConnectionCategory.LAKE)
    ORACLE = ("oracle", AtlanConnectionCategory.WAREHOUSE)
    NETSUITE = ("netsuite", AtlanConnectionCategory.WAREHOUSE)
    MODE = ("mode", AtlanConnectionCategory.BI)
    DBT = ("dbt", AtlanConnectionCategory.ELT)
    FIVETRAN = ("fivetran", AtlanConnectionCategory.ELT)
    VERTICA = ("vertica", AtlanConnectionCategory.WAREHOUSE)
    PRESET = ("preset", AtlanConnectionCategory.BI)
    API = ("api", AtlanConnectionCategory.API)
    DYNAMODB = ("dynamodb", AtlanConnectionCategory.WAREHOUSE)
    GCS = ("gcs", AtlanConnectionCategory.OBJECT_STORE)
    HIVE = ("hive", AtlanConnectionCategory.WAREHOUSE)
    SAPHANA = ("sap-hana", AtlanConnectionCategory.WAREHOUSE)
    ADLS = ("adls", AtlanConnectionCategory.OBJECT_STORE)
    SIGMA = ("sigma", AtlanConnectionCategory.BI)
    SYNAPSE = ("synapse", AtlanConnectionCategory.WAREHOUSE)
    AIRFLOW = ("airflow", AtlanConnectionCategory.ELT)
    OPENLINEAGE = ("openlineage", AtlanConnectionCategory.ELT)
    DATAFLOW = ("dataflow", AtlanConnectionCategory.ELT)
    QLIKSENSE = ("qlik-sense", AtlanConnectionCategory.BI)
    KAFKA = ("kafka", AtlanConnectionCategory.EVENT_BUS)
    QUICKSIGHT = ("quicksight", AtlanConnectionCategory.BI)
    SAP_IQ = ("sap-iq", AtlanConnectionCategory.WAREHOUSE)
    HEX = ("hex", AtlanConnectionCategory.ELT)
    TERADATA = ("teradata", AtlanConnectionCategory.WAREHOUSE)
    YUGABYTEDB = ("yugabytedb", AtlanConnectionCategory.DATABASE)
    IBM_INFORMIX = ("ibm-informix", AtlanConnectionCategory.DATABASE)
    SAP_SQL = ("sap-sql", AtlanConnectionCategory.DATABASE)
    ORACLE_TIMESTEN = ("oracle-timesten", AtlanConnectionCategory.DATABASE)
    PERCONA_SERVER = ("percona-server", AtlanConnectionCategory.DATABASE)
    AURORA = ("aurora", AtlanConnectionCategory.DATABASE)
    SAP_MAXDB = ("sap-maxdb", AtlanConnectionCategory.DATABASE)
    SQLITE = ("sqlite", AtlanConnectionCategory.DATABASE)
    ROCKSET = ("rockset", AtlanConnectionCategory.WAREHOUSE)
    MONGODB = ("mongodb", AtlanConnectionCategory.DATABASE)
    GREENPLUM = ("greenplum", AtlanConnectionCategory.WAREHOUSE)
    MONETDB = ("monetdb", AtlanConnectionCategory.WAREHOUSE)
    ALLOYDB = ("alloydb", AtlanConnectionCategory.DATABASE)
    COCKROACHDB = ("cockroachdb", AtlanConnectionCategory.DATABASE)
    AZURE_COSMOS_DB = ("azure-cosmos-db", AtlanConnectionCategory.DATABASE)
    AZURE_ANALYSIS_SERVICES = (
        "azure-analysis-services",
        AtlanConnectionCategory.WAREHOUSE,
    )
    SINGLESTORE = ("singlestore", AtlanConnectionCategory.WAREHOUSE)
    FIREBIRD = ("firebird", AtlanConnectionCategory.DATABASE)
    THOUGHTSPOT = ("thoughtspot", AtlanConnectionCategory.BI)
    CLICKHOUSE = ("clickhouse", AtlanConnectionCategory.WAREHOUSE)
    MULESOFT = ("mulesoft", AtlanConnectionCategory.API)
    CLARI = ("clari", AtlanConnectionCategory.SAAS)
    MARKETO = ("marketo", AtlanConnectionCategory.SAAS)
    AZURE_DATA_LAKE = ("azure-data-lake", AtlanConnectionCategory.LAKE)
    DELTA_LAKE = ("delta-lake", AtlanConnectionCategory.LAKE)
    MINISQL = ("minisql", AtlanConnectionCategory.DATABASE)
    ICEBERG = ("iceberg", AtlanConnectionCategory.WAREHOUSE)
    IMPALA = ("impala", AtlanConnectionCategory.WAREHOUSE)
    SPARK_SQL = ("spark-sql", AtlanConnectionCategory.LAKE)
    MARIADB = ("mariadb", AtlanConnectionCategory.DATABASE)
    FIREBOLT = ("firebolt", AtlanConnectionCategory.WAREHOUSE)
    CLOUDERA_DATA_WAREHOUSE = (
        "cloudera-data-warehouse",
        AtlanConnectionCategory.WAREHOUSE,
    )
    STARBURST_GALAXY = ("starburst-galaxy", AtlanConnectionCategory.WAREHOUSE)
    REDIS = ("redis", AtlanConnectionCategory.DATABASE)
    GRAPHQL = ("graphql", AtlanConnectionCategory.DATABASE)


class AtlanCustomAttributePrimitiveType(str, Enum):
    def __new__(cls, value: str) -> "AtlanCustomAttributePrimitiveType":
        obj = str.__new__(cls, value)
        obj._value_ = value
        return obj

    STRING = "string"
    INTEGER = "int"
    DECIMAL = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    OPTIONS = "enum"
    USERS = "users"
    GROUPS = "groups"
    URL = "url"
    SQL = "SQL"


class SortOrder(str, Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"


class LineageDirection(str, Enum):
    UPSTREAM = "INPUT"
    DOWNSTREAM = "OUTPUT"
    BOTH = "BOTH"


class AtlanComparisonOperator(str, Enum):
    CONTAINS = "contains"


class BadgeComparisonOperator(str, Enum):
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    EQ = "eq"
    NEQ = "neq"


class BadgeConditionColor(str, Enum):
    GREEN = "#047960"
    YELLOW = "#F7B43D"
    RED = "#BF1B1B"
    GREY = "#525C73"


class FileType(str, Enum):
    CSV = "csv"
    DOC = "doc"
    JSON = "json"
    PDF = "pdf"
    PPT = "ppt"
    TXT = "txt"
    XLS = "xls"
    XML = "xml"
    ZIP = "zip"


class AtlanClassificationColor(str, Enum):
    GREEN = "Green"
    YELLOW = "Yellow"
    RED = "Red"


class QueryParserSourceType(str, Enum):
    ANSI = "ansi"
    BIGQUERY = "bigquery"
    HANA = "hana"
    HIVE = "hive"
    MSSQL = "mssql"
    MYSQL = "mysql"
    ORACLE = "oracle"
    POSTGRESQL = "postgresql"
    REDSHIFT = "redshift"
    SNOWFLAKE = "snowflake"
    SPARKSQL = "sparksql"
    ATHENA = "athena"


class AuthPolicyType(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    ALLOWEXCEPTIONS = "allowExceptions"
    DENYEXCEPTIONS = "denyExceptions"
    DATAMASK = "dataMask"
    ROWFILTER = "rowFilter"


class AuthPolicyCategory(str, Enum):
    BOOTSTRAP = "bootstrap"
    PERSONA = "persona"
    PURPOSE = "purpose"


class AuthPolicyResourceCategory(str, Enum):
    ENTITY = "ENTITY"
    RELATIONSHIP = "RELATIONSHIP"
    TAG = "TAG"
    CUSTOM = "CUSTOM"
    TYPEDEFS = "TYPEDEFS"
    ADMIN = "ADMIN"
