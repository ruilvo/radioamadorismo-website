FROM postgres:15

# Select a PostGIS version
ENV POSTGIS_MAJOR 3

# Update the system
RUN apt-get update && apt-get upgrade -y

# Install PostGIS
RUN apt-get install -y \
    postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR \
    postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts

# Do whatever PostGIS does
# https://github.com/postgis/docker-postgis/blob/master/15-3.4
RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./initdb-postgis.sh /docker-entrypoint-initdb.d/10_postgis.sh
RUN chmod +x /docker-entrypoint-initdb.d/10_postgis.sh
COPY ./update-postgis.sh /usr/local/bin
RUN chmod +x /usr/local/bin/update-postgis.sh
