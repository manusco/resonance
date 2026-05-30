#!/bin/bash
# resonance.sh - System check for Resonance v2.2.0

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "🔮 Resonance v2.2.0 — System Check"
echo "========================================"

# 1. Check Memory (project brain)
if [ ! -f .resonance/01_state.md ]; then
    echo ""
    echo "🧠 Resonance skills loaded. Project memory not found."
    echo "👉 Next step: type '/init' in your AI chat to configure this project."
    echo "   The agent will ask what you're building and scaffold .resonance/ for you."
    exit 0
fi
echo -e "${GREEN}✅ Project memory active (.resonance/)${NC}"

# 2. Check Skills
SKILL_COUNT=$(find .agents/skills -name "SKILL.md" 2>/dev/null | wc -l)
if [ "$SKILL_COUNT" -eq "0" ]; then
    echo -e "${RED}⚠️  No compiled skills found in .agents/skills/.${NC}"
    echo "   Run: py .forge/forge.py build --all"
    exit 1
fi
echo -e "${GREEN}✅ Skill library loaded ($SKILL_COUNT skills active)${NC}"

# 3. Ensure docs structure exists
if [ ! -d docs ]; then
    mkdir -p docs/prd docs/architecture docs/features docs/rfcs
    echo "   Created docs/ directory structure."
fi
echo -e "${GREEN}✅ Docs structure ready${NC}"

echo ""
echo "📖 Soul (Vision):"
head -n 5 .resonance/00_soul.md
echo "..."
echo ""
echo "📊 State (Current task):"
head -n 10 .resonance/01_state.md
echo "..."
echo ""
echo "========================================"
echo -e "${GREEN}System online. Ready.${NC}"
echo ""
echo "Slash commands: /plan  /build  /debug  /audit  /ship"
