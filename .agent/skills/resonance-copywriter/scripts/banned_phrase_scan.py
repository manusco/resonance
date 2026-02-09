import sys
import re

# Simple script to check for taboo phrases
# Usage: python banned_phrase_scan.py "text to check"

TABOO_PHRASES = [
    "delve", "leverage", "harness", "tapestry", "landscape", 
    "game-changer", "realm", "foster", "testament", "beacon",
    "seamless", "robust", "synergy", "paradigm", "unleash"
]

def scan(text):
    text_lower = text.lower()
    violations = []
    for phrase in TABOO_PHRASES:
        if phrase in text_lower:
            violations.append(phrase)
    return violations

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python banned_phrase_scan.py <text>")
        sys.exit(1)
    
    input_text = sys.argv[1]
    found = scan(input_text)
    
    if found:
        print(f"VIOLATIONS FOUND: {', '.join(found)}")
        sys.exit(1) # Return error code 1 if violations found
    else:
        print("CLEAN: No taboo phrases found.")
        sys.exit(0)
