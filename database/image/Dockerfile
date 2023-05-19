FROM postgres:15-alpine

COPY init-movies.sql /docker-entrypoint-initdb.d/

CMD ["postgres"]