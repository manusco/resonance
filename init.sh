#!/bin/bash
# init.sh
# Resonance Initialization Script (v1.0)

echo "Initializing Resonance Engine (v1.0)..."

# 1. Create the .resonance directory if it doesn't exist
mkdir -p .resonance

# 2. Copy templates to the .resonance directory
cp templates/*.md .resonance/

# 3. Install Pointers (Adapters)
cp adapters/.cursorrules .
cp adapters/.windsurfrules .

echo "✅ Resonance initialized."
echo " - Memory Bank: .resonance/ created"
echo " - Brain: AGENT.md (Root)"
echo " - Pointers: .cursorrules & .windsurfrules installed"
