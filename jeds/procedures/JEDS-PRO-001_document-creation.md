# Document Creation Procedure

| | |
|---|---|
| **Document No.** | JEDS-PRO-001 |
| **Revision** | A |
| **Date** | 2026-03-25 |
| **Status** | APPROVED |
| **Author** | Nils Johansson |

---

## 1. Purpose

This procedure describes how to create a new document in the JEDS system, from initial idea to approved release.

## 2. When to Create a Document

Create a new JEDS document when:
- You need to record work that was performed (reports, logs)
- You need to track time or expenses (timesheets, expenses)
- You're creating a deliverable for a project (drawings, manuals)
- You need to define how something is done (procedures)
- You're writing to a client formally (correspondence)

**Rule of thumb:** If you'd regret not having it written down in 6 months, document it.

## 3. Step-by-Step Process

### Step 1: Determine the Category

Refer to the category table in [JEDS-QMS-001](../quality-manual/JEDS-QMS-001_document-numbering.md) and pick the appropriate code (RPT, PRO, TSH, etc.).

### Step 2: Get the Next Number

1. Open the [Document Registry](../registry/document-register.md)
2. Find the last number used in your category
3. Your document gets the next sequential number

**Example:** Last report was JEDS-RPT-003, so your new one is JEDS-RPT-004.

### Step 3: Copy the Template

Go to the [templates folder](../templates/) and copy the appropriate template for your document type. Rename it following the file naming convention:

```
JEDS-[CAT]-[NNN]_short-description.md
```

### Step 4: Fill In the Header

Every JEDS document starts with a header block:

```markdown
| | |
|---|---|
| **Document No.** | JEDS-RPT-004 |
| **Revision** | DRAFT |
| **Date** | 2026-03-25 |
| **Status** | DRAFT |
| **Author** | Nils Johansson |
```

### Step 5: Write the Content

Fill in the document body using the template structure. Write clearly and concisely. Remember: write for someone who wasn't there.

### Step 6: Review

For solo work:
- Re-read the document after a break (even 10 minutes helps)
- Check: Are all facts correct? Could someone else understand this?
- Check: Are all references and numbers accurate?

For collaborative work:
- Send to the designated reviewer
- Reviewer checks technical accuracy and completeness
- Reviewer provides comments or approves

### Step 7: Approve and Release

1. Change the status from `DRAFT` to `APPROVED`
2. Set the revision to `Rev A` (first release)
3. Update the date to the approval date
4. Update the [Document Registry](../registry/document-register.md)
5. Commit the document to the repository

### Step 8: Register

Add an entry to the Document Registry with:
- Document number
- Title
- Category
- Current revision
- Date
- Status
- Author

## 4. Checklist

Use this checklist before approving any document:

- [ ] Document number assigned and unique
- [ ] Correct template used
- [ ] Header block complete (number, revision, date, status, author)
- [ ] Content is clear and complete
- [ ] No spelling or technical errors
- [ ] Revision history table includes this revision
- [ ] Document registry updated
- [ ] File committed to repository

## 5. Common Mistakes to Avoid

| Mistake | Why it matters | Fix |
|---------|---------------|-----|
| Skipping the registry | Documents become unfindable | Always update the registry when creating a document |
| Reusing a retired number | Creates ambiguity in references | Check registry; use the next available number |
| Leaving status as DRAFT | Others won't know if it's reliable | Always update status when the document is approved |
| Vague file names | Hard to browse the folder | Use descriptive, consistent names |
| No revision history | Can't trace changes | Always include the revision history table |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Initial release |
