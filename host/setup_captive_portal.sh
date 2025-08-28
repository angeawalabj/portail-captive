#!/bin/bash
# Script pour lancer le hotspot et le portail captif

set -e

echo ">> Lancement du hotspot CaptivePortal..."

# Arrêt des services existants
systemctl stop hostapd || true
systemctl stop dnsmasq || true
killall nodogsplash || true

# Démarrage du Wi-Fi
hostapd /etc/hostapd/hostapd.conf -B

# Démarrage du serveur DHCP/DNS
dnsmasq -C /etc/dnsmasq.conf

# Démarrage du portail captif
nodogsplash -c /etc/nodogsplash/nodogsplash.conf

echo ">> Portail captif actif sur wlan0"
