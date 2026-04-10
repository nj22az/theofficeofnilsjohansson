# Supervision Program — Gothenburg Workshop

| | |
|---|---|
| **Document No.** | JDS-LOG-MEC-007 |
| **Revision** | A |
| **Date** | 2026-04-10 |
| **Status** | CURRENT |
| **Author** | N. Johansson |
| **Project** | JDS-PRJ-MEC-002 |
| **Client** | Example Workshop AB |
| **Site** | Gothenburg Workshop |
| **Program ID** | SP-[NNN] |
| **Source** | JDS-LOG-MEC-006_example-inventory.md |

---

## 1. Document Chain

```
INVENTORY  →  [PROGRAM]  →  ROUND  →  REVIEW
(Step 1)       (you are      (next)
                here)
```

**Source document:** JDS-LOG-MEC-006_example-inventory.md

This supervision program was **auto-generated** from the equipment inventory. All vessels, classifications, and check schedules have been pre-filled based on the inventory data.

---

## 2. Purpose and Scope

This document is the ongoing supervision program for all pressurised vessels at Gothenburg Workshop. It defines what checks are performed, how often, by whom, and how results are documented. It satisfies AFS 2017:3 Chapter 2, Section 3.

**Equipment in scope:** 7 vessels

---

## 3. Equipment Register Summary

| Vessel ID | Description | Location | Class | Medium | Inspector |
|-----------|-------------|----------|-------|--------|-----------|
| PV-001 | Main air receiver | Compressor room | **A** | compressed air | Accredited body |
| PV-002 | Workshop air receiver | Workshop B | **B** | compressed air | Accredited body (int.) / Own (ext.) |
| PV-003 | Steam boiler | Boiler house | **A** | steam | Accredited body |
| PV-004 | Refrigeration receiver | Engine room | **A** | ammonia | Accredited body |
| PV-005 | Hydraulic accumulator | Workshop A | **B** | hydraulic oil | Accredited body (int.) / Own (ext.) |
| PV-006 | Expansion vessel | Heating system | **Simple PV** | water | N/A |
| PV-007 | Sandblast receiver | Yard | **A** | compressed air | Accredited body |

---

## 4. Supervision Schedule

### 4.1 Daily / Per-Shift Checks

**Applies to:** PV-001, PV-002, PV-003, PV-004, PV-005, PV-007

| # | Check | Method |
|---|-------|--------|
| 1 | Pressure gauge within normal range | Visual reading |
| 2 | Temperature within design limits | Visual reading |
| 3 | No audible leaks or unusual noise | Listening |
| 4 | Control system: no standing alarms | Control panel check |

**Performed by:** [Name / role]
**Record method:** Shift log entry

### 4.2 Weekly Checks

**Applies to:** PV-001, PV-002, PV-003, PV-004, PV-005, PV-007

| # | Check | Method |
|---|-------|--------|
| 1 | No visible leaks at flanges, valves, fittings | Walk-around visual |
| 2 | Safety valves not gagged or blocked | Visual check |
| 3 | Drain valves functional (operate drain) | Manual operation |
| 4 | Condensate drainage working | Visual / operate trap |

**Performed by:** [Name / role]
**Record method:** Weekly check sheet

### 4.3 Monthly Checks

**Applies to:** PV-001, PV-002, PV-003, PV-004, PV-005, PV-006, PV-007

| # | Check | Method |
|---|-------|--------|
| 1 | External surface: no corrosion, dents, cracks | Close visual |
| 2 | Insulation intact, no moisture indicators | Visual check |
| 3 | Support and foundation integrity | Visual check |
| 4 | Safety valve seal intact | Visual check |
| 5 | Vessel access clear and safe | Visual check |

**Performed by:** [Name / role]
**Record method:** Supervision round record (JDS-TMP-LOG-006)

### 4.4 Quarterly Checks

**Applies to:** PV-001, PV-002, PV-003, PV-004, PV-005, PV-007

| # | Check | Method |
|---|-------|--------|
| 1 | Nameplate legible and not obscured | Visual check |
| 2 | Pressure switch function test | Simulate / trip test |
| 3 | Paint / coating condition | Visual check |
| 4 | Review open findings from previous rounds | Register review |

**Performed by:** [Name / role]
**Record method:** Supervision round record (JDS-TMP-LOG-006)

### 4.5 Annual Checks

**Applies to:** PV-001, PV-002, PV-003, PV-004, PV-005, PV-006, PV-007

| # | Check | Method |
|---|-------|--------|
| 1 | Safety valve function test (lift test) | On-line or bench test |
| 2 | Equipment register accuracy verification | Compare to physical |
| 3 | Competence records current | Record review |
| 4 | Formal inspection schedule review | Inspection plan review |

**Performed by:** [Program manager / competent person]
**Record method:** Annual review record (JDS-TMP-LOG-007)

---

## 5. Per-Vessel Check Assignment

| Vessel ID | Class | Daily | Weekly | Monthly | Quarterly | Annual |
|-----------|-------|-------|--------|---------|-----------|--------|
| PV-001 | **A** | Yes | Yes | Yes | Yes | Yes |
| PV-002 | **B** | Yes | Yes | Yes | Yes | Yes |
| PV-003 | **A** | Yes | Yes | Yes | Yes | Yes |
| PV-004 | **A** | Yes | Yes | Yes | Yes | Yes |
| PV-005 | **B** | Yes | Yes | Yes | Yes | Yes |
| PV-006 | **Simple PV** | — | — | Yes | — | Yes |
| PV-007 | **A** | Yes | Yes | Yes | Yes | Yes |

---

## 6. Annual Round Summary

- **Daily checks:** ~250 per year (working days)
- **Weekly checks:** 52 per year
- **Monthly rounds:** 12 per year (formal supervision records)
- **Quarterly reviews:** 4 per year
- **Annual review:** 1 per year

**Total documented check events:** ~319 per year

---

## 7. Personnel and Competence

| Role | Name | Checks Assigned | Competence Ref |
|------|------|----------------|---------------|
| Daily/weekly supervisor | [Name] | Daily, weekly | JDS-PRO-009 record |
| Monthly/quarterly supervisor | [Name] | Monthly, quarterly rounds | JDS-PRO-009 record |
| Program manager | [Name] | Annual review, findings, updates | JDS-PRO-009 record |

All personnel must meet competence requirements per JDS-MAN-MEC-002, Section 7.

---

## 8. Findings Management

| Severity | Definition | Action | Timeline |
|----------|-----------|--------|----------|
| **Critical** | Immediate safety risk | Out of service, escalate | Immediate |
| **Major** | Will deteriorate to critical | Plan repair, close monitoring | Within 30 days |
| **Minor** | Noted, no immediate risk | Monitor, plan maintenance | Within 90 days |
| **Observation** | Worth monitoring | Note, observe trend | Next round |

All findings Major or above managed per **JDS-PRO-008** (Corrective Action Procedure).

---

## 9. Program Review Schedule

This program shall be reviewed at least **annually** or sooner if:
- Equipment is added, removed, or modified
- Operating conditions change significantly
- Regulatory requirements change
- A significant finding or incident occurs

**Next review due:** 2027-01-31

---

## 10. Approval

| | |
|---|---|
| **Prepared by** | [Name, role] |
| **Reviewed by** | [Name, role] |
| **Approved by** | [Operator representative, role] |
| **Approval date** | 2026-04-10 |
| **Next review due** | 2027-01-31 |

---

## 11. Next Step

This program is **Step 2** of the Vessel Supervision System.

```
INVENTORY  →  [PROGRAM]  →  ROUND  →  REVIEW
                (done)      (next)
```

To generate a supervision round record from this program, run:

```
python3 scripts/jds-classify.py --round --from [this-file.md] --output [round-YYYY-MM-DD.md]
```

To generate the annual review, run:

```
python3 scripts/jds-classify.py --review --from [this-file.md] --output [review-YYYY.md]
```

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-04-10 | N. Johansson | Initial program — 7 vessels, auto-generated from JDS-LOG-MEC-006_example-inventory.md |
