# hand-eye calibration (compatibility)

This folder name existed before the repo restructure. Active paths are now:

| Old | New |
|-----|-----|
| `hand-eye calibration/datamark/` | `data/experiments/hand_eye/datamark/` |
| `hand-eye calibration/data_tcp/` | `data/experiments/hand_eye/data_tcp/` |
| `HandEye_Calibration_Matrix.npz` (cwd-relative) | `data/calibration/HandEye_Calibration_Matrix.npz` |
| PBVS logs | `data/experiments/hand_eye/pbvs_experiment_data/` |

## Restore junction (Windows, optional)

If old scripts expect this directory to exist, run from repo root in an **Administrator** terminal:

```powershell
python scripts/create_legacy_links.py
```

That creates a junction from this folder to `data/experiments/hand_eye/`.

## Migrate data from an old tree

```powershell
python scripts/migrate_legacy_layout.py --dry-run
python scripts/migrate_legacy_layout.py
```
