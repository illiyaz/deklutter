#!/bin/bash
# Auto-update RESILIENCE.md with provider configurations
# Run this whenever you add a new provider to provider_config.py

echo "🔄 Updating RESILIENCE.md with provider configurations..."

# Generate provider docs
python3 services/connectors/provider_config.py > /tmp/provider_docs.txt

# Check if generation was successful
if [ $? -ne 0 ]; then
    echo "❌ Failed to generate provider docs"
    exit 1
fi

# Find the line where provider configs should be inserted
# (after the "## 📊 Provider-Specific Configurations" section)

# For now, just append to the end
# TODO: Replace existing provider section if it exists

echo "✅ Provider documentation generated"
echo "📝 Please manually add the generated content to RESILIENCE.md"
echo ""
cat /tmp/provider_docs.txt

rm /tmp/provider_docs.txt
