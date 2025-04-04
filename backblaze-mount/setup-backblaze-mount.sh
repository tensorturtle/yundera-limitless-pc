#!/bin/bash
#
###############################################################################
# Backblaze B2 Rclone Auto-Mount Setup (Tested on Ubuntu 24.04)
#
# This script configures rclone with Backblaze B2 and sets up a persistent
# mount via systemd. It:
#   - Prompts for B2 credentials and bucket name
#   - Installs rclone if needed
#   - Sets up the rclone remote
#   - Mounts the bucket to /mnt/b2-mount
#   - Creates a systemd service to auto-mount on boot
#
# Run this script as root (use sudo).
###############################################################################

set -e

# Check for root privileges
if [[ $EUID -ne 0 ]]; then
  echo "⚠️  This script must be run as root. Try using: sudo $0"
  exit 1
fi

echo "Welcome to the Backblaze B2 rclone setup."

# Prompt user for input
read -p "Enter your Backblaze B2 Key ID: " B2_KEY_ID
read -s -p "Enter your Backblaze B2 Application Key (Secret Key): " B2_APP_KEY
echo ""
read -p "Enter your Backblaze B2 Bucket Name (e.g., b2-username-bucket): " B2_BUCKET
REMOTE_NAME="backblaze"
MOUNT_POINT="/DATA/Backblaze_B2"

# Ensure rclone is installed
if ! command -v rclone &> /dev/null; then
  echo "rclone is not installed. Installing..."
  sudo apt update && sudo apt install -y rclone
fi

# Configure rclone non-interactively
echo "Configuring rclone for Backblaze B2..."
rclone config create "$REMOTE_NAME" b2 \
  account "$B2_KEY_ID" \
  key "$B2_APP_KEY" \
  --obscure

# Create mount point
echo "Creating mount point at $MOUNT_POINT..."
sudo mkdir -p "$MOUNT_POINT"

# Mount the bucket now
echo "Mounting bucket $B2_BUCKET to $MOUNT_POINT..."
rclone mount "${REMOTE_NAME}:${B2_BUCKET}" "$MOUNT_POINT" --daemon --allow-non-empty

# Set up systemd service for automatic mounting
SERVICE_FILE="/etc/systemd/system/rclone-b2-mount.service"
echo "Creating systemd service for auto-mount..."

sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=Mount Backblaze B2 bucket using rclone
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/bin/rclone mount backblaze:tryout-yundera /mnt/b2-mount \
  --config=/root/.config/rclone/rclone.conf \
  --vfs-cache-mode writes \
  --daemon-timeout 5m \
  --allow-other \
  --allow-non-empty \
  --uid=1000 --gid=1000
ExecStop=/bin/fusermount -u ${MOUNT_POINT}
Restart=on-failure
Environment=PATH=/usr/bin:/bin:/usr/sbin:/sbin

[Install]
WantedBy=default.target
EOF

# Reload systemd and enable the service
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable rclone-b2-mount.service
sudo systemctl restart rclone-b2-mount.service

echo "Setup complete! Your Backblaze B2 bucket is mounted at $MOUNT_POINT and will auto-mount on startup."
