# Testing & Validation Suite

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Set Gemini API key
export GEMINI_API_KEY="your_api_key"

# 3. Run validation
python run_validation.py

# 4. Review report
cat validation_reports/validation_report_*.md
```

---

## What You Get

### Automated Testing
- ✅ API starts automatically
- ✅ Sequential tests (3 sectors)
- ✅ Concurrent tests (5 parallel requests)
- ✅ Full response capture
- ✅ Performance metrics
- ✅ Gemini API verification

### Detailed Report
- ✅ Response times
- ✅ Success rates
- ✅ Gemini API status
- ✅ Sample responses
- ✅ Performance analysis
- ✅ Deployment recommendations

### Easy Troubleshooting
- ✅ Clear error messages
- ✅ Helpful suggestions
- ✅ Performance insights
- ✅ Deployment checklist

---

## Files

| File | Purpose |
|------|---------|
| `run_validation.py` | Main validation script |
| `VALIDATION_GUIDE.md` | Detailed guide |
| `VALIDATION_QUICK_START.txt` | Quick reference |
| `VALIDATION_COMPLETE.md` | Complete overview |
| `TESTING_README.md` | This file |

---

## Expected Results

### Success Indicators
- ✓ Success Rate: 100%
- ✓ Response Times: 5-12 seconds
- ✓ Concurrent Speedup: ~2.5x
- ✓ Gemini API: Working or fallback acceptable

### Deployment Ready
- ✓ All tests pass
- ✓ No errors in logs
- ✓ Performance acceptable
- ✓ Gemini API verified

---

## Troubleshooting

**API won't start?**
```bash
lsof -i :8000
kill -9 <PID>
```

**Gemini API not working?**
```bash
export GEMINI_API_KEY="your_key"
```

**Slow responses?**
- Check network connectivity
- Verify DuckDuckGo is accessible
- Monitor system resources

---

## Next Steps

1. ✅ Run validation script
2. ✅ Review report
3. ✅ Check deployment checklist
4. ✅ Deploy to Render or Railway

---

## Documentation

- `VALIDATION_GUIDE.md` - Full guide
- `VALIDATION_QUICK_START.txt` - Quick reference
- `DEPLOYMENT.md` - Deployment instructions
- `README.md` - Complete documentation

---

**Ready? Run: `python run_validation.py`**

