# PLAN-flexible-mapping

## Task Breakdown
- [ ] **Phase 1: Backend Analysis**
    - [ ] Create `/analyze` endpoint to read Excel headers
    - [ ] Save temporary file for subsequent processing
- [ ] **Phase 2: Frontend Wizard**
    - [ ] Update `index.html` to handle 2-step process
    - [ ] Step 1: Upload & Analyze (AJAX)
    - [ ] Step 2: Display Mapping Form (Select Name, Checkbox Phones)
    - [ ] Step 3: Submit Mapping & Process
- [ ] **Phase 3: Backend Processing**
    - [ ] Update `process_dataframe` to accept `mapping` configuration
    - [ ] Implement `pd.melt` logic for row explosion
    - [ ] Apply normalization to all exploded phone numbers
- [ ] **Phase 4: Cleanup**
    - [ ] Auto-delete temporary files after processing

## Agent Assignments
- `processor.py`: Update logic for `melt` and dynamic renaming.
- `app.py`: Add `/analyze` route and update `/upload` (or create `/process`) to handle JSON payload + filename.
- `templates/index.html`: Refactor into a wizard (State 1: Drop, State 2: Map, State 3: Download).

## Verification Checklist (Phase X)
### Automated Tests
- [ ] Create `test_flexible_processing.py` to test `process_dataframe` with:
    - [ ] Single phone column (backwards compatibility logic or new logic)
    - [ ] Multiple phone columns (row explosion)
    - [ ] Empty optional phone columns
    - [ ] Custom column names

### Manual Verification
1. Open web interface
2. Upload `Relatorio Pós Vendas.xlsx` (or a mock with "Whatsapp", "Celular")
3. Confirm Wizard appears with correct column names
4. Select "Nome" and check "Whatsapp" + "Celular"
5. Click Process
6. Download and open Excel
7. Verify:
    - User with 2 numbers has 2 rows
    - Numbers are 9-digit normalized
    - Columns are strictly `Numero`, `Nome`, `Email`

## Open Questions / Trade-offs
- **Temp Files**: We will save files to `uploads/` temporarily. We need a cron or logic to clean them up? *Decision: For MVP, overwrite or use simple unique IDs and cleanup on next upload? Let's use `tempfile` or a dedicated `uploads` folder and clean immediately after processing?* -> **Plan**: Since `/process` is a separate request, we need persistence. We'll save with UUID and delete after successful `/process`.
- **Validation**: What if user selects NO phone column? -> Prevent submit.
