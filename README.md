# Azure 411

Azure resource naming generator following Microsoft Cloud Adoption Framework (CAF) best practices.

## Usage

```bash
./azure_411.py
# or
python3 azure_411.py
```

## Supported Resources

| Resource | Prefix | Scope | Example |
|----------|--------|-------|---------|
| Storage Account | `st` | Global | `stmyappprod001` |
| Blob Container | - | Storage Account | `myapp-prod-001` |
| VPN Gateway | `vpng` | Resource Group | `vpng-myapp-prod-eastus-001` |
| VPN Connection | `vcn` | VPN Gateway | `vcn-myapp-prod-eastus-001` |
| SQL Server | `sql` | Global | `sql-myapp-prod-eastus-001` |
| SQL Database | `sqldb` | SQL Server | `sqldb-myapp-prod-001` |
| Resource Group | `rg` | Subscription | `rg-myapp-prod-eastus-001` |
| Virtual Network | `vnet` | Resource Group | `vnet-myapp-prod-eastus-001` |

## Easter Egg

Type `drizzy` when prompted for a workload name to use a random Drake song title.

## Files

- `azure_411.py` - Main CLI tool
- `resource_rules.py` - CAF naming rules and validation

## References

- [Azure CAF Naming](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming)
- [Resource Abbreviations](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations)
