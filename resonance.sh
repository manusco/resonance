#!/bin/bash
# resonance.sh - The "Wake Up" Call for Antigravity Agents

echo "🔮 Resonance System Check:"
echo "================================"

# Check for corrupted state
if [ ! -f .resonance/01_state.md ]; then
    echo "⚠️  CRITICAL: Memory corrupted. State file missing."
    echo "   Run 'Resonance Init' in Antigravity to rebuild."
    exit 1
fi

# Load consciousness
echo ""
echo "📖 Loading Soul (Vision):"
cat .resonance/00_soul.md
echo ""
echo "================================"
echo ""
echo "📊 Loading State (Current Status):"
cat .resonance/01_state.md
echo ""
echo "================================"
echo ""
echo "✅ Resonance System Online"
echo ""
echo "Available specialist roles:"
ls -1 .resonance/roles/ 2>/dev/null | sed 's/\.md$//' | sed 's/^/  - /' || echo "  (none found)"
