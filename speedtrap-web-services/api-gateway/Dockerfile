FROM nginx
COPY nginx.conf /etc/nginx/nginx.conf
COPY api_gateway.conf /etc/nginx/api_gateway.conf
COPY web_gateway.conf /etc/nginx/web_gateway.conf
COPY api_backends.conf /etc/nginx/api_backends.conf
COPY api_keys.conf /etc/nginx/api_keys.conf
COPY api_conf.d /etc/nginx/api_conf.d/
COPY www /var/www/api.speedtrap.io/
