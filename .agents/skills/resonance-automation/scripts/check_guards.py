import json
import sys
import os
import re

def check_guards(target_file, guards_path):
    if not os.path.exists(guards_path):
        return # No guards defined

    try:
        with open(guards_path, 'r', encoding='utf-8') as f:
            guards = json.load(f)
            
        target_file = os.path.abspath(target_file)
        
        # Check Freezes (Absolute Lock)
        for pattern in guards.get('freeze', []):
            if re.search(pattern, target_file):
                print(f"GUARD_VIOLATION: File '{target_file}' is FROZEN. No changes allowed.")
                sys.exit(1)
                
        # Check Guards (Warning/Verification Required)
        for pattern in guards.get('guard', []):
            if re.search(pattern, target_file):
                print(f"GUARD_WARNING: File '{target_file}' is GUARDED. Proceed with extreme caution and verification.")
                # We don't exit 1 here, just warn. The agent should note this.
                
    except Exception as e:
        print(f"Error checking guards: {e}", file=sys.stderr)
        # On error, we default to safe (exit 1) if we suspect a guard might be missed
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python check_guards.py <target_file> <guards_path>")
        sys.exit(1)
    check_guards(sys.argv[1], sys.argv[2])
