# Document Retention Schedule

| | |
|---|---|
| **Document No.** | JDS-QMS-002 |
| **Revision** | A |
| **Date** | 2026-03-25 |
| **Status** | APPROVED |
| **Author** | Nils Johansson |

---

## 1. Purpose

This standard defines how long each category of document is retained and the rationale for each retention period. It satisfies ISO 15489-1:2016 (Records Management) and ISO 9001:2015 clause 7.5.3 (Control of documented information).

## 2. General Principle

All documents in JDS are stored in a Git repository. Git retains full history indefinitely by default. This means no document is ever truly deleted — superseded and retired versions remain accessible through version history.

This schedule defines the **minimum retention period** for each document category. After this period, documents *may* be archived or removed at the owner's discretion. In practice, the Git-based system means most records are retained permanently at negligible cost.

## 3. Retention Schedule

| Category | Document type | Minimum retention | Rationale |
|----------|--------------|-------------------|-----------|
| **QMS** | Quality Manual, Standards | Permanent | Governs the system; needed for audit trail |
| **PRO** | Procedures | Permanent (current + all superseded) | Demonstrates system evolution; audit evidence |
| **TMP** | Templates | Current version + 1 superseded | Only current templates need to be usable |
| **RPT** | Reports (technical, inspection) | 10 years after project close | Client obligations, liability, regulatory |
| **RPT** | Reports (internal) | 5 years | Internal reference |
| **MAN** | Manuals | Life of equipment/system described | Required while equipment is in service |
| **DWG** | Drawings & Models | Life of equipment + 5 years | Design records needed for maintenance, modification, decommissioning |
| **PRJ** | Project Documents | 10 years after project close | Client obligations, liability |
| **TSH** | Timesheets | 7 years | Tax and accounting requirements (Swedish Bokföringslag) |
| **EXP** | Expenses | 7 years | Tax and accounting requirements (Swedish Bokföringslag) |
| **LOG** | Logs & Records | Life of equipment + 5 years | Regulatory; maintenance history |
| **COR** | Correspondence | 10 years | Contractual; liability |
| **BLG** | Blog Posts | Permanent | Published content; reputational asset |

## 4. Retention of Supporting Files

| File type | Retention | Notes |
|-----------|-----------|-------|
| Source CAD files (.blend, .shapr, .py) | Same as parent DWG record | Needed to reproduce or modify designs |
| Export files (.step, .3mf, .stl) | Same as parent DWG record | Interoperable formats; primary deliverable |
| Reference materials (datasheets, standards excerpts) | Same as parent project | Context for engineering decisions |
| Renders and screenshots | Same as parent project | Visual record of design intent |
| Git history | Permanent | Inherent to the storage system |

## 5. Retention Triggers

Retention periods begin from:

| Document type | Retention starts when... |
|--------------|--------------------------|
| Project documents (RPT, PRJ, DWG) | Project is formally closed or equipment decommissioned |
| Financial records (TSH, EXP) | End of the financial year in which the record was created |
| System documents (QMS, PRO, TMP) | Document is superseded or retired |
| Correspondence (COR) | Date of final communication in the thread |
| Equipment records (LOG, MAN) | Equipment is decommissioned and removed from service |

## 6. Disposal

When a document reaches the end of its retention period:

1. Confirm it is not referenced by any active document
2. Confirm it is not subject to ongoing legal, contractual, or regulatory obligation
3. Move to `jds/archive/retired/` with a note recording the disposal decision
4. The Git history retains the full content permanently regardless

**Documents are never hard-deleted from Git.** Disposal means moving to archive and removing from the active registry.

## 7. Legal and Regulatory Basis

| Requirement | Source | Impact |
|-------------|--------|--------|
| Accounting records: 7 years | Swedish Bokföringslag (1999:1078) | TSH, EXP minimum retention |
| Technical records: life of equipment | Classification societies (DNV, Lloyd's) | LOG, DWG, MAN retention |
| Client deliverables: per contract | Individual client contracts | RPT, PRJ, COR retention |
| Quality records: duration of QMS | ISO 9001:2015 clause 7.5.3 | QMS, PRO permanent retention |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Initial release — ISO 15489 and ISO 9001:2015 clause 7.5.3 alignment |
