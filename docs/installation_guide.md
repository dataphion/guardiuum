## Installation Guide
Installation of guardiuum is straight forward. Only dependecy is to have docker command installed on the host machine.

### Installation Command
```
    git clone https://github.com/dataphion/guardiuum.git
    cd guardiuum
    docker-compose up
```

### Next Steps

- Once the docker-compose commmand is successful, the application can be launched using URL: http://localhost:3000. This will launch the signup page. user can signup and proceed to create an admin user.

- Admin user can:

  - View Dashboard
  - Connect various different datasources
  - Configure Access Security Policy
  - User Management &
  - Settings


## Guardiuum Walkthrough

### Dashboard
The dashboard displays some of the key metrics regarding metadata of all the datasources configured. The details includes total number of Connections/Data Sources, Tables and Columns. It also includes details about recent queries used along with the end user details.

### Data Sources

#### Introduction
The interface enables users to connect their databases which is both on-prem and managed in cloud. It can also manage enterprise applications such as salesforce. All configured data sources can be interacted using standard PSQL clients.

#### Supported Connectors
Connectors supported as of now:
- Google BigQuery
- Databricks
- Object Storage such as S3 and ABFS (Datalake)
- Hive
- MariaDB
- MongoDB
- MySQL
- Postgres
- Presto
- Starburst
- Trino
- Redshift
- Snowflake
- Salesforce (Enterprise Products)

#### Upcoming Connectors
- Athena
- AzureSQL
- Clickhouse
- Couchbase
- DB2
- Delta Lake
- Druid
- DynamoDB
- Greenplum
- Impala
- Mssql
- Oracle
- PinotDB
- SAP HANA and many more.

You can also share with us the connectors that you would like to see in this list. Please raise an issue in the current github repository


##### Guardiuum is free to use. For enterprise support and clustered installation please share your requirements to support@dataphion.com