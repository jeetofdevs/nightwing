# Serves the static site. Railway sets $PORT; Caddy listens on it.
FROM caddy:2.8-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY index.html style.css script.js /srv/
COPY assets /srv/assets
