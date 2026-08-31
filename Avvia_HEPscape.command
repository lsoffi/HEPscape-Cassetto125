#!/bin/bash
cd "$(dirname "$0")" || exit 1
echo "Avvio HEPscape! Cassetto 125..."
echo "Lascia aperta questa finestra durante l'utilizzo."
echo
exec python3 relay_server.py
