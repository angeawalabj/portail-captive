#!/bin/bash
# Script pour lancer le portail captif

if [ "$EUID" -ne 0 ]; then
  echo "❌ Lance ce script avec sudo."
  exit
fi

echo "📦 Installation dépendances..."
apt update && apt install -y hostapd dnsmasq nodogsplash php

echo "⚙️ Configuration interface..."
ip link set wlan0 down
ip addr flush dev wlan0
ip addr add 192.168.10.1/24 dev wlan0
ip link set wlan0 up

echo "🚀 Lancement services..."
systemctl stop hostapd dnsmasq nodogsplash
hostapd ./hostapd.conf -B
dnsmasq -C ./dnsmasq.conf
nodogsplash -c ./nodogsplash.conf

echo "✅ Portail captif démarré sur SSID: MonHotspot"
