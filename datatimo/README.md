# datatimo (compatibility)

Tool CSV output moved to:

`data/outputs/aimooe_tool_data/`

Run migration if you still have files here:

```powershell
python scripts/migrate_legacy_layout.py
```

Optional junction back to this folder name:

```powershell
python scripts/create_legacy_links.py
```

(Requires Administrator on Windows.)
