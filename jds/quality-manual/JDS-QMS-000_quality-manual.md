# JDS Quality Manual

| | |
|---|---|
| **Document No.** | JDS-QMS-000 |
| **Revision** | A |
| **Date** | 2026-03-25 |
| **Status** | APPROVED |
| **Author** | Nils Johansson |
| **Approved by** | Nils Johansson |

---

## 1. Purpose

This Quality Manual defines the quality management system (QMS) for The Office of Nils Johansson. It establishes the policies, standards, and responsibilities that govern all engineering documentation and deliverables.

## 2. Scope

This system applies to all work produced under The Office of Nils Johansson, including but not limited to:

- Engineering reports and technical documents
- 3D models and engineering drawings
- Software projects and source code documentation
- Field service records
- Project management documents
- Financial records (timesheets, expenses)
- Client correspondence and proposals

## 3. Organisation

### 3.1 Roles

| Role | Responsibility |
|------|---------------|
| **Document Owner** | The person who creates and maintains a document. Responsible for accuracy and timely updates. |
| **Reviewer** | Checks a document for technical accuracy and completeness before approval. |
| **Approver** | Authorises the document for use. For sole-proprietor operations, this is the owner. |

### 3.2 Authority

As a sole-proprietor engineering practice, Nils Johansson holds all three roles by default. When collaborators are involved, review and approval responsibilities should be explicitly assigned and recorded on the document.

## 4. Quality Policy

> We produce engineering work that is accurate, traceable, and professionally documented. Every document is written clearly enough for someone unfamiliar with the project to understand. We maintain our documentation system not because it's required, but because good documentation is good engineering.

## 5. Documentation Hierarchy

The JDS documentation is organised in four tiers:

```
Tier 1: Quality Manual (this document)
   ↓    Defines the overall system, policies, and principles

Tier 2: Procedures (JDS-PRO series)
   ↓    Step-by-step instructions for system processes

Tier 3: Templates (JDS-TMP series)
   ↓    Standardised forms and document formats

Tier 4: Records (RPT, TSH, EXP, LOG, etc.)
         Completed documents — the actual work output
```

## 6. Document Control

### 6.1 Numbering

All documents are assigned a unique number following the JDS numbering standard (JDS-QMS-001). Numbers are never reused, even if a document is retired.

### 6.2 Revision Control

Documents follow a controlled revision process (JDS-PRO-002):

- **Rev A** = First approved release
- **Rev B, C, D...** = Subsequent approved revisions
- **DRAFT** = Not yet approved for use
- **SUPERSEDED** = Replaced by a newer revision
- **RETIRED** = No longer in use

### 6.3 Storage

All current documents are stored in this Git repository under the `jeds/` directory. Git provides:
- Full version history of every change
- Traceability of who changed what and when
- Ability to recover any previous version
- Branching for draft work before approval

### 6.4 Backup

The repository is hosted on GitHub, providing remote backup. Local copies should also be maintained.

## 7. Document Lifecycle

```
DRAFT → REVIEW → APPROVED → [IN USE] → REVISION → APPROVED
                                    ↓
                              SUPERSEDED / RETIRED
```

| Stage | Description |
|-------|-------------|
| **DRAFT** | Document is being written. Not for official use. |
| **REVIEW** | Document is complete and being checked for accuracy. |
| **APPROVED** | Document is authorised for use. This is the "live" version. |
| **SUPERSEDED** | A newer revision exists. Kept for reference only. |
| **RETIRED** | Document is no longer relevant. Kept in archive. |

## 8. Quality Objectives

| Objective | Measure |
|-----------|---------|
| All deliverables are documented | Every project has a corresponding document trail |
| Documents are findable | Any document can be located in under 60 seconds via the registry |
| Revisions are traceable | Every change has a recorded reason, date, and author |
| Templates are used consistently | All recurring document types use the standard template |
| System is reviewed regularly | Annual review of QMS procedures and effectiveness |

## 9. Management Review

The documentation system itself shall be reviewed annually (or after significant changes to the business) to ensure it remains:

- Practical and not overly bureaucratic
- Aligned with the type of work being produced
- Up to date with current tools and workflows

Review findings are recorded in a Management Review Report (JDS-RPT series).

## 10. Continuous Improvement

Improvements to the system can come from:

- Lessons learned during projects
- Document errors or near-misses
- Feedback from clients or collaborators
- Annual management review

All improvement actions are tracked and implemented through the revision control process.

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Initial release |
