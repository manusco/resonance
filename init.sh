#!/bin/bash
# init.sh
# Resonance Initialization Script

echo "Initializing Resonance Engine..."

# Create the .resonance directory if it doesn't exist
mkdir -p .resonance

# Copy templates to the .resonance directory
cp templates/*.md .resonance/

echo "✅ Resonance initialized. Memory bank created at .resonance/"
echo "Next step: Install the adapter for your IDE from the adapters/ folder."
