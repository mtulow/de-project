-- Use a role that can create and manage roles and privileges.
USE ROLE securityadmin;

-- Create a Snowflake role with the privileges to work with the connector.
CREATE ROLE crypto_kafka_connector_role;

-- Grant privileges on the database.
GRANT USAGE ON DATABASE kafka_db TO ROLE crypto_kafka_connector_role;

-- Grant privileges on the schema.
GRANT USAGE ON SCHEMA kafka_schema TO ROLE crypto_kafka_connector_role;
GRANT CREATE TABLE ON SCHEMA kafka_schema TO ROLE crypto_kafka_connector_role;
GRANT CREATE STAGE ON SCHEMA kafka_schema TO ROLE crypto_kafka_connector_role;
GRANT CREATE PIPE ON SCHEMA kafka_schema TO ROLE crypto_kafka_connector_role;

-- Only required if the Kafka connector will load data into an existing table.
GRANT OWNERSHIP ON TABLE existing_table1 TO ROLE crypto_kafka_connector_role;

-- Only required if the Kafka connector will stage data files in an existing internal stage: (not recommended).
GRANT READ, WRITE ON STAGE existing_stage1 TO ROLE crypto_kafka_connector_role;

-- Grant the custom role to an existing user.
GRANT ROLE crypto_kafka_connector_role TO USER kafka_connector_user_1;

-- Set the custom role as the default role for the user.
-- If you encounter an 'Insufficient privileges' error, verify the role that has the OWNERSHIP privilege on the user.
ALTER USER kafka_connector_user_1 SET DEFAULT_ROLE = crypto_kafka_connector_role;