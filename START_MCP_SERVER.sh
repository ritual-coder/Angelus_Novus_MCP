#!/bin/bash

# Angelus Novus Migration Folder - MCP Server Startup Script
# This script starts the MCP server from the clean migration directory

echo "🔮 Starting Angelus Novus MCP Server (Migrated Version)..."

# Navigate to the migration directory
cd "$(dirname "$0")"

# Activate the fresh 3.12 virtual environment
source venv/bin/activate

# Start the MCP server using the direct path
# The script itself handles adding its directory to the Python path
python3 Core_MCP_Server/server.py

echo "✨ Migrated MCP Server is running and ready for Perplexity connection"
