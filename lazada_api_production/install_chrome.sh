#!/bin/bash

# Install Chrome and ChromeDriver for Render.com
# This script downloads and installs Chrome and ChromeDriver in the Render cache directory

set -e

echo "🚀 Installing Chrome and ChromeDriver for Render..."

# Create cache directories
mkdir -p /opt/render/.cache/chrome
mkdir -p /opt/render/.cache/chromedriver

# Chrome version to install
CHROME_VERSION="131.0.6778.85"

# Download and install Chrome
echo "📦 Downloading Chrome ${CHROME_VERSION}..."
cd /opt/render/.cache/chrome
wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-linux64.zip"
unzip -q chrome-linux64.zip
rm chrome-linux64.zip
chmod +x chrome-linux64/chrome

# Download and install ChromeDriver
echo "📦 Downloading ChromeDriver ${CHROME_VERSION}..."
cd /opt/render/.cache/chromedriver
wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip"
unzip -q chromedriver-linux64.zip
rm chromedriver-linux64.zip
chmod +x chromedriver-linux64/chromedriver

echo "✅ Chrome and ChromeDriver installed successfully!"
echo "Chrome: /opt/render/.cache/chrome/chrome-linux64/chrome"
echo "ChromeDriver: /opt/render/.cache/chromedriver/chromedriver-linux64/chromedriver"
