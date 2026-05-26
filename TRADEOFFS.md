# ESG Ingestion System — Tradeoffs

## 1. CSV Ingestion Instead of Real Enterprise APIs

### Decision:
Used CSV-based upload instead of direct SAP / Utility / Travel APIs.

### Why:
- Faster to build within 4-day constraint
- Easier to simulate all three data sources
- Avoids complex authentication (SAP/Concur APIs)

### Tradeoff:
- No real-time data ingestion
- Less production realism

---

## 2. Unified Emission Model

### Decision:
Used a single `EmissionRecord` table for all sources.

### Why:
- Simplifies analytics and dashboard queries
- Easier aggregation for charts and reporting
- Matches ESG reporting requirement (Scope-based structure)

### Tradeoff:
- Loss of source-specific schema richness
- Some redundancy in fields across different sources

---

## 3. No Message Queue / Async Processing

### Decision:
Processing is done synchronously during file upload.

### Why:
- Simpler architecture
- Faster debugging and development
- Suitable for prototype scope

### Tradeoff:
- Not scalable for large datasets
- No background processing pipeline (Celery/Kafka)

---

## 4. Static Emission Factors

### Decision:
Used fixed emission factor mapping in backend logic.

### Why:
- Ensures consistent and predictable results
- Simplifies calculation logic

### Tradeoff:
- No dynamic updates from real ESG databases
- Less accurate for real-world regional variations

---

## 5. No PDF/OCR Processing for Utility Data

### Decision:
Assumed structured CSV input for utility data.

### Why:
- OCR pipelines are complex and time-consuming
- Focus kept on normalization and ingestion logic

### Tradeoff:
- Does not simulate real utility bill parsing
- Limited realism for enterprise ingestion

---

## 6. JWT Authentication (LocalStorage-based)

### Decision:
Used JWT stored in browser localStorage.

### Why:
- Simple frontend integration with React
- Stateless backend design
- Easy session persistence

### Tradeoff:
- Vulnerable to XSS attacks
- No refresh token mechanism
- Not production-grade security

---

## 7. No Role-Based Access Control (RBAC)

### Decision:
Single user role (analyst view only).

### Why:
- Focus on ingestion + dashboard logic
- Time constraint (prototype build)

### Tradeoff:
- No admin/analyst/user separation
- No permission-based workflows

---

## 8. Simple Rule-Based Flagging System

### Decision:
Used basic validation rules instead of ML-based anomaly detection.

### Why:
- Easy to implement and explain
- Transparent decision logic

### Tradeoff:
- Cannot detect complex anomalies
- No predictive data quality system

---

## 9. Frontend Simplicity (React + Recharts)

### Decision:
Used basic React UI with Recharts for visualization.

### Why:
- Fast development
- Easy integration with API
- Sufficient for ESG KPI dashboard

### Tradeoff:
- Not enterprise-grade UI/UX design
- Limited scalability for large dashboards

---

## END OF TRADEOFFS.md