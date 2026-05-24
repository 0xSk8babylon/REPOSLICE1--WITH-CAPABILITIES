# Data Model

## Core Entities

- `Home`: persistent property record
- `BuildingStructure`: house, workshop, ADU, garage, barn, or other structure
- `ElectricalPanel`: service and downstream electrical distribution context
- `Load`: backed-up and non-backed-up consumption model
- `EnergySystemDesign`: candidate architecture tied to a home
- `EquipmentProduct`: structured product record with placeholder specs
- `DesignEquipment`: equipment assignments inside a design
- `EquipmentLocation`: siting record tied to building context
- `CompatibilityIssue`: structured rule output with explanation fields
- `Scenario`: comparison-ready design framing
- `TakeoffRequest` and `TakeoffLineItem`: future estimating pipeline seed objects

## Modeling Intent

The current model intentionally separates property facts, design facts, product facts, rule outputs, and estimate artifacts so each layer can mature independently.

