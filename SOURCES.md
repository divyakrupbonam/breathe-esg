# ESG Ingestion System — Sources & Research Basis

## 1. SAP Data (Fuel & Procurement)

- Real SAP systems (S/4HANA, ECC) expose data via IDoc, OData APIs, and CSV exports.
- Common issues: inconsistent units, custom plant codes, and regional date formats.
- SAP data is not analysis-ready and requires transformation before ESG reporting.

### Key Challenges Observed:
- Non-standard column names (sometimes localized like German headers)
- Mixed units (liters, kg, MJ)
- Internal codes instead of readable categories

### Simplification Used:
- No IDoc parsing
- No SAP authentication
- No master data mapping (plants/materials)
- Used CSV-based ingestion for prototype

---

## 2. Utility Data (Electricity)

- Utility providers typically expose data through:
  - CSV exports from customer portals
  - Smart meter APIs
  - PDF electricity bills (OCR in real systems)

### Typical Fields:
- kWh consumption
- billing period (start/end dates)
- meter ID
- tariff type

### Key Challenges Observed:
- Billing cycles do not match calendar months
- Multiple meters per building
- Data often delayed or incomplete

### How It Is Modeled:
- Treated as `UTILITY` source_type
- Converted into Scope 2 emissions
- Standardized to kWh before CO2e calculation

### Simplification Used:
- No PDF/OCR parsing
- No tariff-based pricing logic
- No multi-meter aggregation

---

## 3. Corporate Travel Data (Concur / Navan / Amadeus)

- Travel platforms provide structured API data for:
  - Flights (airport codes)
  - Hotels (night stays)
  - Ground transport (distance or cost)

### References:
- https://developer.concur.com/
- https://developers.amadeus.com/

### Key Challenges Observed:
- Flight distance is often missing (requires estimation)
- Airport codes must be mapped to distances
- Emission factors vary by transport type

### How It Is Modeled:
- Stored as `TRAVEL` source_type
- Represented as Scope 3 emissions
- Categories like flight_km, hotel_nights, taxi_km

### Simplification Used:
- No IATA distance API integration
- No route optimization logic
- No hotel emission breakdown model

---

## 4. Emission Factor Standards

- Emission calculations are based on industry standards:

### References:
- GHG Protocol: https://ghgprotocol.org/
- IPCC Guidelines: https://www.ipcc.ch/
- DEFRA Conversion Factors (UK Government)

### Usage in System:
- CO2e calculated as:
  activity_value × emission_factor

---

## 5. Data Quality Understanding

Real ESG datasets often contain:
- Missing values
- Negative or incorrect emissions
- Unit mismatches
- Duplicate entries

### How this system handles it:
- Flagging system (`is_flagged`)
- Simple validation rules:
  - negative values → flagged
  - extreme values → flagged

---

## 6. System Design Inspiration

- ESG reporting standards (Scope 1 / 2 / 3)
- SaaS ingestion pipelines (ETL architecture)
- Enterprise audit workflows
- Data warehouse modeling patterns

---

## END OF SOURCES.md