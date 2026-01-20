import sys
import os

def check_structure():
    required_files = ["task_plan.md", "findings.md", "progress.md"]
    workspace_root = os.getcwd()
    
    print(f"🔍 Resonance System Integrity Check: {workspace_root}")
    print("================================================")
    
    missing = []
    for f in required_files:
        path = os.path.join(workspace_root, f)
        if os.path.exists(path):
            print(f"✅ {f} detected.")
        else:
            print(f"❌ {f} MISSING.")
            missing.append(f)
            
    print("================================================")
    if missing:
        print(f"⚠️  Incomplete Manus Pattern. Missing: {', '.join(missing)}")
        print("Protocol: Use `@resonance-core` to initialize planning.")
        return 1
    else:
        print("💎 Manus Pattern Fully Synchronized. Ready for Elite execution.")
        return 0

if __name__ == "__main__":
    sys.exit(check_structure())
