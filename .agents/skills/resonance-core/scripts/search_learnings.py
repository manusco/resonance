import json
import sys
import os

def search_learnings(query, file_path, limit=5):
    if not os.path.exists(file_path):
        print(f"No learnings file found at {file_path}")
        return

    query = query.lower()
    results = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    # Simple keyword match across all values
                    content = json.dumps(entry).lower()
                    if query in content:
                        results.append(entry)
                except json.JSONDecodeError:
                    continue
        
        # Return most recent first
        results.reverse()
        for r in results[:limit]:
            print(json.dumps(r, indent=2))
            print("-" * 20)
    except Exception as e:
        print(f"Error searching learnings: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python search_learnings.py <query> <file_path> [limit]")
        sys.exit(1)
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    search_learnings(sys.argv[1], sys.argv[2], limit)
