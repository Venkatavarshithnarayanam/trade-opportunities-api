#!/usr/bin/env python3
"""
Simple startup test - Just runs the API with minimal overhead
Use this to test if the API starts at all
"""

import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print("\n" + "="*80)
print("STARTING TRADE OPPORTUNITIES API")
print("="*80 + "\n")

try:
    print("Importing main module...")
    import main
    print("✓ Main module imported\n")
    
    print("Starting uvicorn server...")
    print("API will be available at: http://localhost:8001")
    print("API Docs at: http://localhost:8001/docs")
    print("Health check: curl http://localhost:8001/health -H 'X-API-Key: trade-api-key-2024'")
    print("\nPress Ctrl+C to stop\n")
    
    import uvicorn
    uvicorn.run(main.app, host="0.0.0.0", port=8001, log_level="info")
    
except KeyboardInterrupt:
    print("\n\nAPI stopped by user")
    sys.exit(0)
except Exception as e:
    print(f"\n✗ Error starting API: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
