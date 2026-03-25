# Centrifugal Pump Inspection — Cooling Water System

| | |
|---|---|
| **Document No.** | JEDS-RPT-001 |
| **Revision** | A |
| **Date** | 2026-03-25 |
| **Status** | EXAMPLE |
| **Author** | Nils Johansson |
| **Project** | N/A — Example document |
| **Client** | Internal |

> **Note:** This is an example document to demonstrate how a JEDS report looks when completed. The content is fictional but representative of a real field service report.

---

## 1. Summary

Inspection of the No. 2 cooling water pump at Facility X revealed excessive bearing wear and seal degradation. The pump is functional but requires bearing replacement and mechanical seal overhaul within the next 30 days to prevent unplanned failure.

## 2. Background

The No. 2 cooling water pump (CW-P-002) was reported as showing increased vibration levels during routine monitoring. A visual inspection and basic measurements were requested to determine the cause and recommend corrective action.

## 3. Scope

- Visual inspection of pump and motor assembly
- Vibration measurement (handheld)
- Bearing temperature check
- Seal leakage assessment
- Review of maintenance history

**Excluded:** Internal disassembly, alignment check (requires pump isolation).

## 4. Findings

### 4.1 General Condition

The pump exterior is in acceptable condition. No visible corrosion on the casing. Foundation bolts are tight. Coupling guard is in place.

### 4.2 Vibration Measurements

| Location | Direction | Value (mm/s RMS) | Limit | Status |
|----------|-----------|-------------------|-------|--------|
| Drive end bearing | Horizontal | 4.2 | 4.5 | Warning |
| Drive end bearing | Vertical | 3.8 | 4.5 | OK |
| Non-drive end bearing | Horizontal | 6.1 | 4.5 | **Alert** |
| Non-drive end bearing | Vertical | 5.4 | 4.5 | **Alert** |

The non-drive end bearing shows vibration levels above the alert threshold per ISO 10816-3 for Class II machines.

### 4.3 Temperature

| Location | Measured | Limit | Status |
|----------|----------|-------|--------|
| Drive end bearing | 62°C | 80°C | OK |
| Non-drive end bearing | 74°C | 80°C | Warning |

### 4.4 Seal Condition

Visible drip rate from the mechanical seal: approximately 2 drops per second. This exceeds acceptable leakage for this seal type. Fluid observed is clear (cooling water, no oil contamination).

### 4.5 Maintenance History

Last bearing replacement: 2023-11-15 (approx. 28 months ago).
Recommended interval: 24 months.
The pump is overdue for scheduled bearing maintenance.

## 5. Conclusions

1. The non-drive end bearing is showing early-stage failure symptoms (elevated vibration and temperature).
2. The mechanical seal is degraded and leaking beyond acceptable limits.
3. The pump is currently operational but at increased risk of unplanned failure.

## 6. Recommendations

| # | Recommendation | Priority | Deadline |
|---|---|---|---|
| 1 | Replace non-drive end bearing | High | Within 30 days |
| 2 | Inspect and replace mechanical seal | High | During bearing replacement |
| 3 | Check shaft alignment after bearing replacement | Medium | At reassembly |
| 4 | Review and update preventive maintenance schedule | Medium | Within 60 days |
| 5 | Repeat vibration measurement after repair to confirm | Low | After repair |

## 7. Attachments

- [ ] Vibration measurement data (raw)
- [ ] Thermal image of bearing housing
- [ ] Maintenance history extract

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Initial release (example document) |
