Run the JDS 5S audit (per JDS-PRO-005) to check system health.

## Steps

1. Run the automated validation script:

```bash
python3 scripts/jds-validate.py
```

2. Review the output carefully. For each ERROR or WARNING:
   - Determine whether it's a real issue or a false positive
   - If real: fix it immediately following JDS procedures
   - If false positive: note it for validator improvement

3. After fixing all issues, re-run the validator to confirm a clean pass.

4. Check for stale content:
   - Are there any DRAFT documents that should be APPROVED?
   - Are there any documents that haven't been updated in the current quarter?
   - Is the corrective action log (`jds/registry/corrective-action-log.md`) up to date?

5. Check the CHANGELOG:
   - Does the latest version entry reflect all recent changes?
   - Is the JDS README version consistent with the CHANGELOG?

6. Report findings to the user with:
   - Number of checks passed/failed
   - What was fixed
   - Any items needing human decision

## After the audit

If changes were made, commit with message format:
```
JDS 5S Audit [YYYY-MM-DD]: [summary of findings and fixes]
```

This follows JDS-PRO-005 §5.1 audit recording.
