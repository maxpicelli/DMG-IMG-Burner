#!/bin/bash

################################################################################
# DMG Burner Bundle Creator
# Creates a macOS .app bundle from DMG-terminal.py
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         DMG Burner - Bundle Creator for macOS                  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Configuration
APP_NAME="DMG Burner"
APP_BUNDLE="${APP_NAME}.app"
IDENTIFIER="com.m4pro.dmgburner"
VERSION="1.0"
PYTHON_SCRIPT="DMG-terminal.py"
ICON_FILE="dmg-burner-icon.icns"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Validate required files
echo -e "${YELLOW}[1/7]${NC} Validating required files..."
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo -e "${RED}✗ Error: $PYTHON_SCRIPT not found!${NC}"
    exit 1
fi

if [ ! -f "$ICON_FILE" ]; then
    echo -e "${RED}✗ Error: $ICON_FILE not found!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ All required files found${NC}"

# Clean existing bundle
if [ -d "$APP_BUNDLE" ]; then
    echo -e "${YELLOW}[2/7]${NC} Removing existing bundle..."
    rm -rf "$APP_BUNDLE"
    echo -e "${GREEN}✓ Existing bundle removed${NC}"
else
    echo -e "${YELLOW}[2/7]${NC} No existing bundle to remove"
fi

# Create app bundle structure
echo -e "${YELLOW}[3/7]${NC} Creating bundle structure..."
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"
echo -e "${GREEN}✓ Bundle structure created${NC}"

# Copy Python script
echo -e "${YELLOW}[4/7]${NC} Copying Python script..."
cp "$PYTHON_SCRIPT" "$APP_BUNDLE/Contents/MacOS/$PYTHON_SCRIPT"
chmod +x "$APP_BUNDLE/Contents/MacOS/$PYTHON_SCRIPT"
echo -e "${GREEN}✓ Python script copied${NC}"

# Create launcher script
echo -e "${YELLOW}[5/7]${NC} Creating launcher script..."
cat > "$APP_BUNDLE/Contents/MacOS/$APP_NAME" << 'EOF'
#!/bin/bash

# Get the directory where the app bundle is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    osascript -e 'display dialog "Python 3 is required but not installed.\n\nPlease install Python 3 from:\nhttps://www.python.org/downloads/" buttons {"OK"} default button "OK" with icon stop with title "DMG Burner - Error"'
    exit 1
fi

# Open Terminal and run the Python script
osascript <<APPLESCRIPT
tell application "Terminal"
    activate
    do script "cd '$DIR' && python3 DMG-terminal.py; exit"
end tell
APPLESCRIPT
EOF

chmod +x "$APP_BUNDLE/Contents/MacOS/$APP_NAME"
echo -e "${GREEN}✓ Launcher script created${NC}"

# Copy icon
echo -e "${YELLOW}[6/7]${NC} Copying icon..."
cp "$ICON_FILE" "$APP_BUNDLE/Contents/Resources/$ICON_FILE"
echo -e "${GREEN}✓ Icon copied${NC}"

# Create Info.plist
echo -e "${YELLOW}[7/7]${NC} Creating Info.plist..."
cat > "$APP_BUNDLE/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>${APP_NAME}</string>
    <key>CFBundleIconFile</key>
    <string>${ICON_FILE}</string>
    <key>CFBundleIdentifier</key>
    <string>${IDENTIFIER}</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>${APP_NAME}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>${VERSION}</string>
    <key>CFBundleVersion</key>
    <string>${VERSION}</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
    <key>NSHumanReadableCopyright</key>
    <string>Copyright © 2025 M4Pro. All rights reserved.</string>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>img</string>
                <string>dmg</string>
            </array>
            <key>CFBundleTypeName</key>
            <string>Disk Image</string>
            <key>CFBundleTypeRole</key>
            <string>Viewer</string>
            <key>LSHandlerRank</key>
            <string>Alternate</string>
        </dict>
    </array>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.utilities</string>
    <key>NSAppleScriptEnabled</key>
    <true/>
</dict>
</plist>
EOF
echo -e "${GREEN}✓ Info.plist created${NC}"

# Set proper permissions
echo ""
echo -e "${BLUE}Setting permissions...${NC}"
chmod -R 755 "$APP_BUNDLE"
chmod +x "$APP_BUNDLE/Contents/MacOS/$APP_NAME"
chmod +x "$APP_BUNDLE/Contents/MacOS/$PYTHON_SCRIPT"

# Update icon cache (optional, helps macOS recognize the new icon)
touch "$APP_BUNDLE"
killall Finder 2>/dev/null || true

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                   ✓ BUILD SUCCESSFUL!                          ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Application created:${NC} ${APP_BUNDLE}"
echo -e "${BLUE}Location:${NC} ${SCRIPT_DIR}/${APP_BUNDLE}"
echo ""
echo -e "${YELLOW}Usage:${NC}"
echo -e "  • Double-click '${APP_BUNDLE}' to launch"
echo -e "  • The app will open Terminal and run the DMG Burner tool"
echo -e "  • Python 3 is required (built-in on macOS 10.15+)"
echo ""
echo -e "${YELLOW}Note:${NC}"
echo -e "  • First launch may require right-click > Open (Gatekeeper)"
echo -e "  • The app requires administrator privileges to burn images"
echo ""
echo -e "${GREEN}Done!${NC}"

