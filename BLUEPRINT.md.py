# PointStreetNexus_V2 - Project State
**Date:** April 2026
**Hardware:** iPhone 17 Pro Max + Nano 300 Thermal Sensor
**Database:** SQL Server (PointStreetNexusDB) on Port 37630
**Auth Mode:** SQL Authentication (sa)

## Current Status
- [x] PyCharm environment configured.
- [x] Database connection verified (Port 37630, sa login).
- [x] Master `models.py` updated with Supply Chain, IoT, and Botanical Registry.
- [x] Initial SQL Server table generation logic ready.

## Next Steps
1. Execute `Base.metadata.create_all()` to materialize all tables.
2. Build the "Watcher" script for iPhone 17 photo ingestion.
3. Integrate Nano 300 thermal data parsing into `MediaAsset` records.
