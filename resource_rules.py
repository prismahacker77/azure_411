"""
Azure Resource Naming Rules following Microsoft Cloud Adoption Framework (CAF)
https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming
"""

import re

AZURE_REGIONS = [
    "eastus", "eastus2", "westus", "westus2", "westus3",
    "centralus", "northcentralus", "southcentralus", "westcentralus",
    "canadacentral", "canadaeast",
    "brazilsouth",
    "northeurope", "westeurope", "uksouth", "ukwest",
    "francecentral", "germanywestcentral", "norwayeast", "swedencentral", "switzerlandnorth",
    "australiaeast", "australiasoutheast", "australiacentral",
    "eastasia", "southeastasia", "japaneast", "japanwest", "koreacentral",
    "centralindia", "southindia", "westindia",
    "uaenorth", "southafricanorth",
]

ENVIRONMENTS = ["dev", "test", "stg", "prod", "uat", "qa", "sandbox"]


class ResourceType:
    """Defines naming rules for an Azure resource type."""

    def __init__(self, name, prefix, min_len, max_len, pattern, scope, requires_region=True, lowercase_only=False, no_hyphens=False):
        self.name = name
        self.prefix = prefix
        self.min_len = min_len
        self.max_len = max_len
        self.pattern = pattern
        self.scope = scope
        self.requires_region = requires_region
        self.lowercase_only = lowercase_only
        self.no_hyphens = no_hyphens

        if requires_region:
            self.pattern_template = f"{prefix}-<workload>-<env>-<region>-<instance>"
        else:
            self.pattern_template = f"{prefix}<workload><env><instance>" if no_hyphens else f"{prefix}-<workload>-<env>-<instance>"

    def validate(self, name):
        """Validate a resource name. Returns (is_valid, error_message)."""
        if len(name) < self.min_len:
            return False, f"Name too short. Minimum {self.min_len} characters, got {len(name)}."
        if len(name) > self.max_len:
            return False, f"Name too long. Maximum {self.max_len} characters, got {len(name)}."
        if not re.match(self.pattern, name):
            return False, f"Name contains invalid characters or format."
        if self.lowercase_only and name != name.lower():
            return False, "Name must be lowercase only."
        return True, ""


def _clean_name(name):
    """Clean a name by removing invalid characters and converting to lowercase."""
    return re.sub(r'[^a-z0-9]', '', name.lower())


def _clean_name_with_hyphens(name):
    """Clean a name, allowing hyphens but converting spaces to hyphens."""
    name = name.lower().replace(' ', '')
    return re.sub(r'[^a-z0-9-]', '', name)


def generate_name(resource_key, workload, environment, region, instance):
    """Generate a resource name following CAF conventions."""
    resource = RESOURCE_TYPES[resource_key]
    workload_clean = _clean_name(workload)
    env_clean = _clean_name(environment)
    region_clean = _clean_name(region) if region else ""
    instance_clean = instance.zfill(3) if instance.isdigit() else instance

    if resource.no_hyphens:
        if resource.requires_region:
            return f"{resource.prefix}{workload_clean}{env_clean}{region_clean}{instance_clean}"
        return f"{resource.prefix}{workload_clean}{env_clean}{instance_clean}"
    else:
        # Build name parts, filtering out empty components
        if resource.requires_region:
            parts = [resource.prefix, workload_clean, env_clean, region_clean, instance_clean]
        else:
            parts = [resource.prefix, workload_clean, env_clean, instance_clean]
        # Filter out empty parts and join with hyphens
        return "-".join(part for part in parts if part)


RESOURCE_TYPES = {
    "storage_account": ResourceType(
        name="Storage Account",
        prefix="st",
        min_len=3,
        max_len=24,
        pattern=r'^[a-z0-9]{3,24}$',
        scope="Global",
        requires_region=False,
        lowercase_only=True,
        no_hyphens=True
    ),
    "blob_container": ResourceType(
        name="Blob Container",
        prefix="",
        min_len=3,
        max_len=63,
        pattern=r'^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$',
        scope="Storage Account",
        requires_region=False,
        lowercase_only=True
    ),
    "vpn_gateway": ResourceType(
        name="VPN Gateway",
        prefix="vpng",
        min_len=1,
        max_len=80,
        pattern=r'^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,78}[a-zA-Z0-9_]$',
        scope="Resource Group",
        requires_region=True
    ),
    "vpn_connection": ResourceType(
        name="VPN Connection",
        prefix="vcn",
        min_len=1,
        max_len=80,
        pattern=r'^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,78}[a-zA-Z0-9_]$',
        scope="VPN Gateway",
        requires_region=True
    ),
    "sql_server": ResourceType(
        name="SQL Server",
        prefix="sql",
        min_len=1,
        max_len=63,
        pattern=r'^[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$',
        scope="Global",
        requires_region=True,
        lowercase_only=True
    ),
    "sql_database": ResourceType(
        name="SQL Database",
        prefix="sqldb",
        min_len=1,
        max_len=128,
        pattern=r'^[^<>*%&:\\/?]{1,128}$',
        scope="SQL Server",
        requires_region=False
    ),
    "resource_group": ResourceType(
        name="Resource Group",
        prefix="rg",
        min_len=1,
        max_len=90,
        pattern=r'^[a-zA-Z0-9._-]+$',
        scope="Subscription",
        requires_region=True
    ),
    "virtual_network": ResourceType(
        name="Virtual Network",
        prefix="vnet",
        min_len=2,
        max_len=64,
        pattern=r'^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,62}[a-zA-Z0-9_]$',
        scope="Resource Group",
        requires_region=True
    ),
}
