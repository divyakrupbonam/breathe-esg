# ESG Ingestion System — Data Model Design

## 1. Overview

This system is designed to simulate an enterprise ESG (Environmental, Social, Governance) data ingestion platform. The core challenge is handling heterogeneous data sources (SAP, Utility, and Travel systems), normalizing them into a unified emissions model, and enabling audit-ready approval workflows.

The data model is designed with:
- Multi-tenancy support (company-based isolation)
- Source traceability (audit requirements)
- Normalized emissions representation
- Review and approval workflow
- Data quality tracking (flagging anomalies)

---

## 2. Core Entities

### 2.1 Company
Represents a tenant organization onboarding ESG data.

**Fields:**
- id
- name
- industry

**Purpose:**
Ensures multi-tenant isolation so each company's ESG data is independent.

---

### 2.2 DataSource (Ingestion Layer)

Represents an uploaded dataset from a specific external system.

**Fields:**
- id
- company (FK → Company)
- source_type (SAP / UTILITY / TRAVEL)
- uploaded_file
- status (PROCESSING / COMPLETED / FAILED)
- created_at

**Purpose:**
Tracks provenance of every ingestion batch.

This is critical for:
- audit traceability
- debugging ingestion failures
- regulatory compliance

---

### 2.3 EmissionRecord (Core Fact Table)

Represents normalized ESG emission entries.

**Fields:**
- id
- company (FK)
- source (FK → DataSource)
- scope (Scope 1 / 2 / 3)
- category (diesel, electricity, flight, etc.)
- activity_date
- activity_value (raw input)
- activity_unit (raw unit)
- normalized_value
- normalized_unit
- emission_factor
- co2e_emission
- is_flagged (data quality flag)
- status (PENDING / APPROVED)
- raw_data (JSON snapshot for audit)

**Purpose:**
This is the **central analytical dataset** used for reporting and approval.

---

### 2.4 Audit Trail (Implicit via DataSource + EmissionRecord)

Instead of a separate audit table, auditability is achieved using:
- DataSource (batch-level tracking)
- EmissionRecord.raw_data (row-level traceability)
- status field (approval lifecycle)

---

## 3. Data Flow Architecture

### Step 1: Ingestion
File uploaded → DataSource created → raw CSV parsed

### Step 2: Normalization
Each row:
- unit conversion (normalize_unit)
- CO2e calculation (calculate_emission)

### Step 3: Storage
Stored as EmissionRecord with:
- raw + normalized values
- emission factor applied
- computed CO2e

### Step 4: Review Workflow
Analyst:
- reviews records
- approves valid data
- flagged records reviewed separately

---

## 4. Scope Classification

| Scope | Meaning |
|------|--------|
| Scope 1 | Direct fuel combustion (diesel, gas) |
| Scope 2 | Purchased electricity |
| Scope 3 | Travel, indirect emissions |

---

## 5. Multi-Tenancy Strategy

All tables include:
- company foreign key

Ensures:
- strict data isolation
- scalable SaaS architecture

---

## 6. Data Quality & Flagging Logic

Records are flagged when:
- negative CO2e values appear
- extreme outliers exist
- inconsistent unit conversion detected

This simulates real-world ESG data uncertainty.

---

## 7. Design Philosophy

- Prefer traceability over abstraction
- Store raw + normalized data together
- Keep ingestion separate from analytics
- Optimize for audit compliance over performance

---

## 8. Tradeoff Summary

- No separate audit log table (simplified via JSON + source tracking)
- No external SAP/Concur integration (mock ingestion)
- Simplified emission factor model

---

END OF MODEL DESIGN