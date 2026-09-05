"""Shared domain enumerations used by ORM models and Pydantic schemas."""

from enum import StrEnum


class Criticality(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class EnvironmentName(StrEnum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"
    TEST = "test"
    DR = "dr"


class DeploymentModel(StrEnum):
    ON_PREM = "on_prem"
    CLOUD = "cloud"
    HYBRID = "hybrid"
    MAINFRAME = "mainframe"
    SAAS = "saas"


class AssetType(StrEnum):
    """Types that can appear as dependency endpoints."""

    APPLICATION = "application"
    SERVICE = "service"
    DATABASE = "database"
    API = "api"
    INFRASTRUCTURE = "infrastructure"


class DependencyType(StrEnum):
    CALLS = "calls"
    READS_FROM = "reads_from"
    WRITES_TO = "writes_to"
    DEPENDS_ON = "depends_on"
    PUBLISHES_TO = "publishes_to"
    CONSUMES_FROM = "consumes_from"


class ModernizationStrategy(StrEnum):
    REHOST = "rehost"
    REPLATFORM = "replatform"
    REFACTOR = "refactor"
    REPURCHASE = "repurchase"
    RETIRE = "retire"
    RETAIN = "retain"
    REPLACE = "replace"


class RiskCategory(StrEnum):
    TECHNICAL = "technical"
    OPERATIONAL = "operational"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    DATA = "data"
    DEPENDENCY = "dependency"
    BUSINESS = "business"
    MIGRATION_COMPLEXITY = "migration_complexity"


class RiskSeverity(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecommendationStatus(StrEnum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"


class ApprovalDecision(StrEnum):
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"


class AuditAction(StrEnum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    IMPORT = "import"
    ANALYZE = "analyze"
    RECOMMEND = "recommend"
    APPROVE = "approve"
    REJECT = "reject"
    MODIFY = "modify"
