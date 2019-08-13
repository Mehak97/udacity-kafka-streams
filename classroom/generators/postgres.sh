echo 'schema.registry.url=http://localhost:8081' >> /etc/kafka/connect-distributed.properties
systemctl start confluent-zookeeper
systemctl start confluent-kafka
systemctl start confluent-schema-registry
systemctl start confluent-kafka-rest
systemctl start confluent-kafka-connect
systemctl start confluent-ksql
sed -i 's/md5/trust/g' /etc/postgresql/10/main/pg_hba.conf
/etc/init.d/postgresql start
su postgres -c "createuser root -s"
createdb classroom
psql -d classroom -c "CREATE TABLE purchases(id INT PRIMARY KEY, username VARCHAR(100), currency VARCHAR(10), amount INT);"
psql -d classroom -c "CREATE TABLE clicks(id INT PRIMARY KEY, email VARCHAR(100), timestamp VARCHAR(100), uri VARCHAR(512), number INT);"
psql -d classroom -c "CREATE TABLE connect_purchases(id INT PRIMARY KEY, username VARCHAR(100), currency VARCHAR(10), amount INT);"
psql -d classroom -c "CREATE TABLE connect_clicks(id INT PRIMARY KEY, email VARCHAR(100), timestamp VARCHAR(100), uri VARCHAR(512), number INT);"
psql -d classroom -c "COPY purchases(id,username,currency,amount)  FROM '/tmp/purchases.csv' DELIMITER ',' CSV HEADER;"
psql -d classroom -c "COPY clicks(id,email,timestamp,uri,number)  FROM '/tmp/clicks.csv' DELIMITER ',' CSV HEADER;"