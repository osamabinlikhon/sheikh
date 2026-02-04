#!/bin/bash
set -e

# Setup environment
export DISPLAY=:99
export HOME=/workspace

# Create workspace directory
mkdir -p /workspace

# Start virtual display
echo "Starting virtual display..."
Xvfb :99 -screen 0 1920x1080x24 &
sleep 2

# Start VNC server
echo "Starting VNC server..."
x11vnc -display :99 -forever -shared -rfbport 5900 -passwd "" &
sleep 2

# Start websockify for VNC over WebSocket
echo "Starting WebSocket VNC bridge..."
websockify --web /usr/share/novnc 6080 localhost:5900 &
sleep 2

# Start Chrome in headless mode with remote debugging
echo "Starting Chrome browser..."
google-chrome-stable \
    --headless \
    --disable-gpu \
    --remote-debugging-port=9222 \
    --no-sandbox \
    --disable-dev-shm-usage \
    --disable-software-rasterizer \
    --disable-background-timer-throttling \
    --disable-backgrounding-occluded-windows \
    --disable-renderer-backgrounding \
    --disable-features=TranslateUI \
    --disable-ipc-flooding-protection \
    --disable-background-media-suspend \
    --disable-extensions \
    --disable-default-apps \
    --disable-component-extensions-with-background-pages \
    --disable-breakpad \
    --disable-crash-reporter \
    --disable-features=ImprovedCookieControls,LazyImageLoading,GlobalMediaControls,DestroyProfileOnBrowserClose,MediaRouter \
    --disable-background-networking &
sleep 3

# Start sandbox API server
echo "Starting sandbox API server..."
cd /app
uvicorn main:app --host 0.0.0.0 --port 8080 --reload