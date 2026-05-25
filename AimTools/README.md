# AimTools

Place Aimooe tool definition files here before running hardware scripts.

## Required files

| File | Purpose |
|------|---------|
| `PTM-4.aimtool` | Needle tool (L1 tip registration, hand-eye TCP sync) |
| `PTM-99.aimtool` | Membrane phantom tool (PBVS / multi-marker tracking) |

## How to obtain `.aimtool` files

1. Open the Aimooe positioning software on the workstation connected to the tracker.
2. Export or copy the registered tool files for **PTM-4** and **PTM-99**.
3. Paste them into this directory: `aimooe_ur5e/AimTools/`.

Typical vendor install folders (adjust for your PC):

- `C:\Program Files\AimPos\AimToolBox\Config\AimTools\`
- `D:\AimPosAppSolutionAPI\AimToolBox\Config\AimTools\`

## Legacy folder name

Pre-restructure builds used `Aimtools/` (lowercase “t”). The code checks **both** `AimTools/` and `Aimtools/` and uses whichever already contains `.aimtool` files.

## Verify

```powershell
conda activate aimooe-ur5e
python scripts/check_env.py
```

Scripts resolve tools via `src/project_paths.resolve_aimtools_dir()`.
