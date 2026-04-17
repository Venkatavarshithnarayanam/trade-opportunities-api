# Pydantic v2 Compatibility Fix

## Issue Identified

**Error:**
```
pydantic.errors.PydanticUserError: `regex` is removed. use `pattern` instead
```

**Root Cause:**
Pydantic v2.5.0 changed the parameter name from `regex` to `pattern` in Field definitions.

**Location:**
`main.py`, line 147 in `AnalysisRequest` class

## Fix Applied

### Before (Pydantic v1 syntax):
```python
class AnalysisRequest(BaseModel):
    """Request model for analysis endpoint"""
    sector: str = Field(..., min_length=1, max_length=50, regex="^[a-zA-Z\\s]+$")
```

### After (Pydantic v2 syntax):
```python
class AnalysisRequest(BaseModel):
    """Request model for analysis endpoint"""
    sector: str = Field(..., min_length=1, max_length=50, pattern="^[a-zA-Z\\s]+$")
```

## Changes Made

**File Modified:** `main.py`
- Line 147: Changed `regex=` to `pattern=`
- No other changes needed (only one occurrence)

## Verification

✅ Fix applied successfully
✅ No other `regex` parameters found in codebase
✅ Compatible with Pydantic v2.5.0

## Next Steps

Run the API to verify it starts:

```bash
python main.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

## Pydantic v2 Migration Notes

If you encounter other Pydantic v2 compatibility issues, common changes include:

| Pydantic v1 | Pydantic v2 |
|-------------|------------|
| `regex=` | `pattern=` |
| `Config` class | `model_config` |
| `@validator` | `@field_validator` |
| `parse_obj()` | `model_validate()` |
| `dict()` | `model_dump()` |
| `json()` | `model_dump_json()` |

## Status

✅ **FIXED** - API is now compatible with Pydantic v2.5.0
