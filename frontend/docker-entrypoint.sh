#!/bin/sh
set -e

# Sync dependencies if package.json changed
HASH_FILE="/app/node_modules/.package-hash"
CURRENT_HASH=$(md5sum /app/package.json | cut -d' ' -f1)

if [ ! -f "$HASH_FILE" ] || [ "$(cat $HASH_FILE)" != "$CURRENT_HASH" ]; then
    echo "Package.json changed, installing dependencies..."
    npm install --legacy-peer-deps
    echo "$CURRENT_HASH" > "$HASH_FILE"
else
    echo "Dependencies up to date"
fi

exec "$@"
