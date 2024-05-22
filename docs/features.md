## Key Features Of Dataphion Guardiuuum

- **Centralised data management** :
Guardiumm will be the entry point for all data sources provisioned in the platform.

- **SQL Everywhere**: Any connected platform can be connected using Postgres compliant client and access data using SQL queries.

- **Query Federation**: Run queries directly on the database without moving the data across. Queries can be written to perform complicated join across various different data sources.

- **Zero Data Copy**: With in-built query federation, data is not moved between platforms instead, it is directly queried against the source platform where data resides. For end user Guardiuum is the data provider but in the backend Guardiuum identifies the right source, executes the query on the right platform and returns the results back to the users. This will be very helpful in building a unified analytics dashboard, exporting enriched data for consumers etc.,

- **Inherently Support Data Mesh and Data Fabric**: With Guardiuum, Data Mesh architecture

- **Audit Logging**: Captures every interation within the platform and generate insights into ho the data is being accessed.

- **Role based Security policy**: Apply individual level or group based security policy for accessing the data.

- **Enterprise auth integration**: Support for simple, Kerberose(Upcoming) and Active Directory and Azure Entra ID authentication.

## What is SQL Everywhere:

Guardiuum enables users to connect to single/multiple data platforms using SQL queries. The goal is to abstract the complexities of using native APIs or SDK to read/extract the data from any data source platform. For ex: Business users should be able to query the Sales data from CRM platforms using SQL queries only.

Guardiuum enables by providing support for below components:

1. Postgres wire protocol compliant server
2. Integrated Query federation
3. Connector/Adapters for each platform which translates the SQL query into the native connectivity format.
