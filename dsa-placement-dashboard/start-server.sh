#!/bin/bash
echo "Starting Placement Preparation Dashboard on http://localhost:8080 ..."
echo "Press Ctrl+C to stop the server."
which open > /dev/null && (sleep 1 && open "http://localhost:8080/index.html") &
python3 -m http.server 8080
