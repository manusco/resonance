import json
import sys
import os
from datetime import datetime

def log_learning(data_str, file_path):
    try:
        data = json.loads(data_str)
        data['timestamp'] = datetime.utcnow().isoformat() + 'Z'
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data) + '\n')
        print(f"Successfully logged learning to {file_path}")
    except Exception as e:
        print(f"Error logging learning: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python log_learning.py '<json_data>' <file_path>")
        sys.exit(1)
    log_learning(sys.argv[1], sys.argv[2])
