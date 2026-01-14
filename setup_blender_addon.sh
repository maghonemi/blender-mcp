#!/bin/bash
# Script to set up Blender MCP as directory addon

echo "=========================================="
echo "Blender MCP Directory Addon Setup"
echo "=========================================="
echo ""

# Find Blender version directories
BLENDER_SUPPORT="$HOME/Library/Application Support/Blender"
echo "Looking for Blender installations in: $BLENDER_SUPPORT"
echo ""

# List available Blender versions
VERSIONS=$(find "$BLENDER_SUPPORT" -maxdepth 1 -type d -name "[0-9]*" 2>/dev/null | sort -V)

if [ -z "$VERSIONS" ]; then
    echo "❌ No Blender installations found!"
    echo "   Make sure Blender is installed and has been run at least once."
    exit 1
fi

echo "Found Blender versions:"
echo "$VERSIONS" | while read version_dir; do
    version=$(basename "$version_dir")
    echo "  - $version"
done
echo ""

# Ask user which version
echo "Which Blender version do you want to install to?"
echo "Enter version number (e.g., 4.0, 4.1, 3.6) or 'all' for all versions:"
read -r SELECTED_VERSION

if [ "$SELECTED_VERSION" = "all" ]; then
    VERSIONS_TO_INSTALL="$VERSIONS"
else
    VERSION_DIR="$BLENDER_SUPPORT/$SELECTED_VERSION"
    if [ ! -d "$VERSION_DIR" ]; then
        echo "❌ Version $SELECTED_VERSION not found!"
        exit 1
    fi
    VERSIONS_TO_INSTALL="$VERSION_DIR"
fi

# Get source directory
SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"
echo ""
echo "Source directory: $SOURCE_DIR"
echo ""

# Install to each version
echo "$VERSIONS_TO_INSTALL" | while read version_dir; do
    version=$(basename "$version_dir")
    ADDON_DIR="$version_dir/scripts/addons/blender_mcp"
    
    echo "Installing to Blender $version..."
    
    # Create addon directory
    mkdir -p "$ADDON_DIR"
    
    # Copy files
    echo "  Copying files..."
    cp "$SOURCE_DIR/addon_new.py" "$ADDON_DIR/__init__.py"
    cp -r "$SOURCE_DIR/core" "$ADDON_DIR/"
    cp -r "$SOURCE_DIR/handlers" "$ADDON_DIR/"
    cp -r "$SOURCE_DIR/utils" "$ADDON_DIR/"
    
    # Copy ui directory if it exists
    if [ -d "$SOURCE_DIR/ui" ]; then
        cp -r "$SOURCE_DIR/ui" "$ADDON_DIR/"
    fi
    
    echo "  ✓ Installed to: $ADDON_DIR"
    echo ""
done

echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Open Blender"
echo "2. Go to Edit > Preferences > Add-ons"
echo "3. Search for 'Blender MCP'"
echo "4. Enable it (check the box)"
echo "5. Restart Blender completely"
echo "6. Check console for: 'Registered X handlers' (should be 80+ with all features)"
echo ""
