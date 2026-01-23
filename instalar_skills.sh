#!/bin/bash

# Define the source of truth for your skills (Current Workspace)
SOURCE_DIR="/Users/tiagolau/.gemini/antigravity/scratch/criar skills/.agent"

# Target directory is the first argument, or current directory by default
TARGET_DIR="${1:-.}"

# Check if source exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "❌ Erro: Pasta de origem das skills não encontrada em: $SOURCE_DIR"
    exit 1
fi

echo "🚀 Instalando skills em: $TARGET_DIR/.agent ..."

# Create the target .agent folder if it doesn't exist
mkdir -p "$TARGET_DIR/.agent"

# Copy all contents from the .agent folder recursively
cp -a "$SOURCE_DIR/." "$TARGET_DIR/.agent/"

echo "✅ Sucesso! As skills foram copiadas."
echo "📂 Localização: $TARGET_DIR/.agent/skills"
echo "💡 Dica: Se não vir a pasta, lembre-se que ela começa com '.' (oculta)."
