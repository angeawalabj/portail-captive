# Utiliser l'image officielle Nginx stable
FROM nginx:stable-alpine

# Copier la configuration nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Copier le frontend (web) dans le dossier public
COPY ../web /usr/share/nginx/html

# Exposer le port 80 pour HTTP
EXPOSE 80

# Lancer nginx au premier plan
CMD ["nginx", "-g", "daemon off;"]
