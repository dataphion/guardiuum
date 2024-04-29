## Key Features Of Dataphion Guardiuuum

- **Centralised data management** :
Guardiumm will be the entry point for all data sources provisioned in the platform.

- **SQL Everywhere**: Any connected platform can be connected using Postgres compliant client and access data using SQL queries.

- **Audit Logging**: Captures every interation within the platform and generate insights into ho the data is being accessed.

- **Role based Security policy**: Apply individual level or group based security policy for accessing the data.

- **Enterprise auth integration**: Support for simple, Kerberose(Upcoming) and Active Directory and Azure Entra ID authentication.

## What is SQL Everywhere:

Guardiuum enables users to connect to single/multiple data platforms using SQL queries. The goal is to abstract the complexities of using native APIs or SDK to read/extract the data from any data source platform. For ex: Business users should be able to query the Sales data from CRM platforms using SQL queries only.

Guardiuum enables this by providing support for below components:

1. Postgres wire protocol compliant server
2. Integrated Query federation
3. Connector/Adapters for each platform which translates the SQL query into the native connectivity format.
