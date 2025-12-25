#!/bin/bash
# resonance.sh - The "Wake Up" Call for Antigravity Agents

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check for update command
if [ "$1" == "update" ]; then
    echo -e "${YELLOW}📡 Checking for Resonance updates...${NC}"
    echo ""
    
    # Get local version from AGENT.md
    if [ -f "AGENT.md" ]; then
        LOCAL_VERSION=$(grep -m 1 "# RESONANCE v" AGENT.md | sed 's/.*v\([0-9.]*\).*/\1/')
        echo "   Local version: v$LOCAL_VERSION"
        
        # Fetch remote version
        REMOTE_VERSION=$(curl -s https://raw.githubusercontent.com/manusco/resonance/main/AGENT.md | grep -m 1 "# RESONANCE v" | sed 's/.*v\([0-9.]*\).*/\1/')
        
        if [ -n "$REMOTE_VERSION" ]; then
            echo "   Latest version: v$REMOTE_VERSION"
            echo ""
            
            if [ "$LOCAL_VERSION" != "$REMOTE_VERSION" ]; then
                echo -e "${YELLOW}✨ Update available!${NC}"
                echo ""
                echo "To update, run:"
                echo "  curl -o AGENT.md https://raw.githubusercontent.com/manusco/resonance/main/AGENT.md"
                echo ""
                echo "Note: Your .resonance/ folder will not be affected."
            else
                echo -e "${GREEN}✅ You're running the latest version!${NC}"
            fi
        else
            echo -e "${RED}❌ Unable to check for updates (network issue?)${NC}"
        fi
    else
        echo -e "${RED}❌ AGENT.md not found${NC}"
    fi
    
    exit 0
fi

echo "🔮 Resonance System Check:"
echo "================================"

# Check for corrupted state
if [ ! -f .resonance/01_state.md ]; then
    echo "⚠️  CRITICAL: Memory corrupted. State file missing."
    echo "   Run 'Resonance Init' in Antigravity to rebuild."
    exit 1
fi

# Check for knowledge directory
if [ ! -d .resonance/knowledge ]; then
    echo "   Creating knowledge directory..."
    mkdir -p .resonance/knowledge
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
echo ""
echo "💡 Tip: Run './resonance.sh update' to check for framework updates"
