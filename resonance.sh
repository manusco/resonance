#!/bin/bash
# resonance.sh - The "Wake Up" Call for Resonance v2.0

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🔮 Resonance v2.0 System Check:"
echo "================================================"

# 1. Check Memory (The Brain)
if [ ! -f .resonance/01_state.md ]; then
    echo -e "${RED}⚠️  CRITICAL: Memory corrupted. State file missing.${NC}"
    echo "   Run '@Resonance /init_project' to bootstrap."
    exit 1
fi
echo -e "${GREEN}✅ Memory Active (.resonance/)${NC}"

# 2. Check Skills (The Talent)
SKILL_COUNT=$(ls -1 .agent/skills/resonance-* 2>/dev/null | wc -l)
if [ "$SKILL_COUNT" -eq "0" ]; then
    echo -e "${RED}⚠️  CRITICAL: No Resonance Skills found in .agent/skills/.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Elite Skills Loaded ($SKILL_COUNT active)${NC}"

# 3. Check Workflows (The Protocol)
WORKFLOW_COUNT=$(ls -1 .agent/workflows/*.md 2>/dev/null | wc -l)
echo -e "${GREEN}✅ Workflows Ready ($WORKFLOW_COUNT protocols)${NC}"

# 4. Ensure Docs Structure
if [ ! -d docs ]; then
    mkdir -p docs/specs docs/architecture docs/reports
    echo "   Created docs/ directory structure."
fi

echo "================================================"
echo ""
echo "📖 Loading Soul (Vision):"
head -n 5 .resonance/00_soul.md
echo "..."
echo ""
echo "📊 Loading State (Status):"
head -n 10 .resonance/01_state.md
echo "..."
echo ""
echo "================================================"
echo -e "${GREEN}System Online. Ready for orders.${NC}"
echo ""
echo "Try: @Resonance /status"

