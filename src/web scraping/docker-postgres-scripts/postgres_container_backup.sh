psql -U postgres -p 4321 -d realestate -c "COPY properties to stdout DELIMITER ',' CSV HEADER" > backup.csv