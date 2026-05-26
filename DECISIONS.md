# ESG Ingestion System — Design Decisions

## 1. Why CSV-based ingestion for SAP, Utility, and Travel?

Real enterprise systems expose data in multiple formats:
- SAP: IDoc / CSV exports / OData APIs
- Utility: CSV or PDF bills from portals
- Travel: APIs (Concur / Navan)

For this implementation, CSV ingestion was chosen because:
- fastest to prototype within constraints
- consistent structure for normalization logic
- allows simulation of all three sources

---

## 2. Why a unified EmissionRecord model?

Instead of separate tables per source, a unified schema was used because:
- ESG reporting requires consolidated emissions view
- Scope 1/2/3 classification standardizes reporting
- simplifies analyst review workflow

Tradeoff:
- loses source-specific schema richness

---

## 3. Why store both raw and normalized values?

Each record stores:
- raw activity_value + unit
- normalized_value + unit

Reason:
- ensures auditability
- allows recalculation if emission factors change
- supports regulatory compliance

---

## 4. Why flagging system exists?

Flagging is used to simulate real ESG data quality issues.

Rules used:
- negative CO2e values → invalid measurement
- extreme outliers → potential ingestion errors

This mimics real-world data validation pipelines.

---

## 5. Why JWT authentication?

JWT was selected because:
- stateless authentication
- suitable for API + React architecture
- scalable for SaaS systems

---

## 6. Why React + Django architecture?

- Django: handles ingestion, normalization, and audit logic
- React: provides analyst dashboard UI

This separation follows:
> backend = data intelligence layer  
> frontend = visualization + workflow layer

---

## 7. Why Recharts for visualization?

Recharts was used because:
- lightweight
- fast integration with React
- sufficient for ESG KPI visualization

Alternative (not used):
- D3.js (too complex for prototype scope)

---

## 8. What was intentionally simplified?

- No real SAP API integration
- No external utility API ingestion
- No persistent message queue (Kafka, Celery)
- No role-based access control
- No production-grade logging system

---

## 9. What assumptions were made?

- CSV structure is consistent per source
- emission factors are pre-defined
- company onboarding already exists
- analyst is the primary user

---

## 10. Key Tradeoffs

| Area | Decision | Reason |
|------|----------|--------|
| Ingestion | CSV upload | fast prototyping |
| Storage | single model | simplified analytics |
| Auth | JWT | frontend compatibility |
| Visualization | Recharts | simplicity |

---

END OF DESIGN DECISIONS