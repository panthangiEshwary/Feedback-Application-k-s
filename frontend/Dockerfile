FROM nginx:alpine

# Copy static frontend files
COPY index.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/

# Copy custom Nginx config
COPY default.conf /etc/nginx/conf.d/default.conf
