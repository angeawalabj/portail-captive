#!/bin/bash
# Script pour déconnecter un client du hotspot
# Usage: ./ndsctl_deauth.sh <MAC_ADDRESS>

if [ -z "$1" ]; then
    echo "Usage: $0 <MAC_ADDRESS>"
    exit 1
fi

MAC="$1"
echo ">> Déconnexion du client $MAC"
ndsctl deauth "$MAC"
