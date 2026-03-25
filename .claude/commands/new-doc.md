Create a new JDS document following all procedures.

## Input

The user will describe what document they need: $ARGUMENTS

## Steps (JDS-PRO-001 Document Creation Procedure)

1. **Determine the document category** from the description:
   - QMS = Quality manual/standards
   - PRO = Procedures
   - RPT = Reports
   - MAN = Manuals
   - DWG = Drawings/models
   - PRJ = Project documents
   - TSH = Timesheets
   - EXP = Expenses
   - LOG = Logs/records
   - COR = Correspondence/letters
   - BLG = Blog posts

2. **Determine the domain code** (if technical):
   MEC, MAR, AUT, ELE, PIP, STR, TST, FAB, THR, SFW, GEN

3. **Assign the next available number** by checking the document register:
   `jds/registry/document-register.md`

4. **Select the correct template** from `jds/templates/`

5. **Create the document** in the correct directory with proper naming:
   `JDS-[CAT]-[DOM]-[NNN]_descriptive-name.md`

6. **Register the document** in `jds/registry/document-register.md`

7. **Update the CHANGELOG** if this is a system-level addition

8. **Run validation** to confirm compliance:
   ```bash
   python3 scripts/jds-validate.py --quick
   ```

9. **Report** the new document path and JDS number to the user

## Important

- NEVER skip registration. Every document gets registered.
- NEVER skip the metadata header. Use the template.
- ALWAYS include a revision history table.
- Commit the new document with a clear message referencing the JDS number.
