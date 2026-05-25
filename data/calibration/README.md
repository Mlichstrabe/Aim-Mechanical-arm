# Calibration artifacts

Store registration outputs here. Override location with environment variable `AIMOOE_CALIB_DIR`.

## Expected files

| File | Chain | Produced by |
|------|-------|-------------|
| `HandEye_Calibration_Matrix.npz` | L2 optical → robot | Hand-eye calibration pipeline (restore from `data/experiments/hand_eye/` or re-run when scripts are re-added) |
| `space_reg.npz` | L3 CT → optical | `src/aimooe_sdk/demo1.py` menu case **62**, or `collect_space_reg.py` |
| `calibration_chain.json` | Offline teaching copy | Same layout as `data/sample/calibration_chain.json` |

## NPZ keys (convention)

**HandEye_Calibration_Matrix.npz**

- `R_opt2rob` (3×3)
- `t_opt2rob` (3,) in **mm**

**space_reg.npz**

- `R_ct2opt` (3×3)
- `t_ct2opt` (3,) in **mm**

## Usage in code

```python
from src.offline_bridge.coord_bridge import load_calibration_chain, transform_ct_point_to_robot

chain = load_calibration_chain()
p_rob = transform_ct_point_to_robot(chain, [x, y, z])
```

Or run the executor:

```powershell
python src/ur5e_control/execute_ct_puncture.py --dry-run
```
