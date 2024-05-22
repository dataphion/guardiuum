#  Copyright 2021 Collate
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from abc import abstractmethod
from pydantic import BaseModel, ValidationError, validator
from pathlib import Path
from typing import Iterable, Optional, List, Dict, Any,Tuple
from pyhive import hive
from metadata.ingestion.api.common import Entity
from metadata.ingestion.api.models import Either, StackTraceError
from metadata.ingestion.api.steps import Source, InvalidSourceException
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    OpenMetadataConnection,
)
from urllib.parse import quote_plus
from pydantic import SecretStr
from sqlalchemy.engine import Engine
from metadata.generated.schema.entity.services.connections.database.customDatabaseConnection import (
    CustomDatabaseConnection,
)
from metadata.generated.schema.entity.data.database import Database
from metadata.generated.schema.entity.data.databaseSchema import DatabaseSchema
from metadata.generated.schema.api.data.createDatabaseSchema import (
    CreateDatabaseSchemaRequest,
)
from metadata.generated.schema.entity.services.connections.database.hiveConnection import (
    HiveConnection,
    HiveScheme,
)
from metadata.generated.schema.api.data.createDatabase import CreateDatabaseRequest
from metadata.generated.schema.entity.services.databaseService import (
    DatabaseService,
)
from metadata.generated.schema.entity.data.table import (
    Column,
)
from metadata.generated.schema.metadataIngestion.workflow import (
    Source as WorkflowSource,
)
from metadata.generated.schema.api.data.createTable import CreateTableRequest
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.utils.logger import ingestion_logger

logger = ingestion_logger()


class InvalidHiveConnectorException(Exception):
    """
    hive data is not valid to be ingested
    """

class HiveConnector(Source):

    def __init__(self, config: WorkflowSource, metadata: OpenMetadata):
        self.config = config
        self.metadata = metadata

        self.service_connection = config.serviceConnection.__root__.config

        self.username: str = (
            self.service_connection.connectionOptions.__root__.get("username")
        )
        self.password: str = (
            self.service_connection.connectionOptions.__root__.get("password")
        )
        self.hostPort: str = (
            self.service_connection.connectionOptions.__root__.get("hostPort")
        )
        self.auth: str = (
            self.service_connection.connectionOptions.__root__.get("auth")
        )
        self.scheme: str = (
            self.service_connection.connectionOptions.__root__.get("scheme")
        )
        self.httpPath: str = (
            self.service_connection.connectionOptions.__root__.get("httpPath")
        )
        self.transportMode: str = (
            self.service_connection.connectionOptions.__root__.get("transportMode")
        )
        self.database: str = (
            self.service_connection.connectionOptions.__root__.get("database")
        )
        hostNo, portNo = self.hostPort.split(':')
        self.data: Optional[List[Any]] = []

        print("username=========>>>>>>>>>>>:",self.username)
        print("password=========>>>>>>>>>>>:",self.password)
        print("hostPort=========>>>>>>>>>>>:",self.hostPort)
        print("auth=========>>>>>>>>>>>:",self.auth)
        print("scheme=========>>>>>>>>>>>:",self.scheme)
        print("httpPath=========>>>>>>>>>>>:",self.httpPath)
        print("transportMode=========>>>>>>>>>>>:",self.transportMode)
        print("database=========>>>>>>>>>>>:",self.database)

        
        # Establish connection
        self.connection = hive.Connection(host=hostNo, 
                       port=portNo,
                       username=self.username,
                       password=self.password,
                       database=self.database,
                       auth=self.auth,
                       scheme=self.scheme,
                       configuration={"httpPath": self.httpPath,"transportMode": self.transportMode})
        super().__init__()

    @classmethod
    def create(
        cls, config_dict: dict, metadata_config: OpenMetadataConnection
    ) -> "HiveConnector":
        config: WorkflowSource = WorkflowSource.parse_obj(config_dict)
        connection: CustomDatabaseConnection = config.serviceConnection.__root__.config
        if not isinstance(connection, CustomDatabaseConnection):
            raise InvalidSourceException(
                f"Expected CustomDatabaseConnection, but got {connection}"
            )
        return cls(config, metadata_config)

    def prepare(self):
        pass

    def get_schemas(self) -> List[Tuple[str, List[str], Dict[str, List[Column]]]]: # type: ignore
        print("inside schemas")
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SHOW DATABASES")
                schemas = [row[0] for row in cursor.fetchall()]
                print("schemasss------------------------>",schemas)
            
            for schema in schemas:
                database_entity: Database = self.metadata.get_by_name(
                    entity=Database, fqn=f"{self.config.serviceName}.{self.database}"
                )
                print("database_entity.fullyQualifiedName=========>>>>",database_entity.fullyQualifiedName)
                yield Either(
                    right=CreateDatabaseSchemaRequest(
                        name=schema,
                        database=database_entity.fullyQualifiedName,
                    )
                )
                with self.connection.cursor() as cursor:
                    cursor.execute(f"USE {schema}")
                    cursor.execute(f"SHOW tables FROM {self.database}.{schema}")
                    tables_data = cursor.fetchall()
                    tables = [row[1] for row in tables_data]
                    print("tabless------------------------->",tables)
                    

                database_schema: DatabaseSchema = self.metadata.get_by_name(
                    entity=DatabaseSchema,
                    fqn=f"{self.config.serviceName}.{self.database}.{schema}",
                )
                for table in tables:
                    with self.connection.cursor() as cursor:
                        print("inside columns----->")
                        cursor.execute(f"describe table {self.database}.{schema}.{table}")
                        column_data = [(row[0], row[1]) for row in cursor.fetchall()]
                        # for column, data_type in column_data:
                        yield Either(
                            right=CreateTableRequest(
                                name=table,
                                databaseSchema=database_schema.fullyQualifiedName,
                                columns=[
                                    Column(
                                        name=column,
                                        dataType=data_type.upper(),
                                    )
                                    for column, data_type in column_data
                                ],
                            )
                        )

        
        except Exception as e:
            print(f"Error occurred while  fetching schemas data: {e}")
            raise e

    # def get_tables(self, schema: str) -> List[str]:
    #     print("inside tables")
    #     try:
    #         with self.connection.cursor() as cursor:
    #             cursor.execute(f"USE {schema}")
    #             cursor.execute("SHOW TABLES")
    #             print("tabless--------->",[row[0] for row in cursor.fetchall()])
    #             return [row[0] for row in cursor.fetchall()]
    #     except Exception as e:
    #         print(f"Error occurred while  fetching tables data: {e}")
    #         raise e

    # def get_columns(self, schema: str, table: str) -> List[Column]:
    #     print("inside columns")
    #     try:
    #         with self.connection.cursor() as cursor:
    #             cursor.execute(f"DESCRIBE {schema}.{table}")
    #             return [Column(name=row[0], type=row[1]) for row in cursor.fetchall()]
    #     except Exception as e:
    #         print(f"Error occurred while  fetching columns data: {e}")
    #         raise e


    def yield_create_request_database_service(self):
        yield Either(
            right=self.metadata.get_create_service_from_source(
                entity=DatabaseService, config=self.config
            )
        )

    def yield_creation_db(self):
        # Pick up the service we just created (if not UI)
        service_entity: DatabaseService = self.metadata.get_by_name(
            entity=DatabaseService, fqn=self.config.serviceName
        )
        yield Either(
            right=CreateDatabaseRequest(
                name=self.database,
                service=service_entity.fullyQualifiedName,
            )
        )
        print("serviceName==============>>>>>>:",self.config.serviceName)
        print("fullyQualifiedName===========>>>>>>:",service_entity.fullyQualifiedName)

    # def yield_default_schema(self):
    #     # Pick up the service we just created (if not UI)
    #     database_entity: Database = self.metadata.get_by_name(
    #         entity=Database, fqn=f"{self.config.serviceName}.{self.database}"
    #     )
    #     print("database_entity.fullyQualifiedName=========>>>>",database_entity.fullyQualifiedName)
    #     yield Either(
    #         right=CreateDatabaseSchemaRequest(
    #             name="default",
    #             database=database_entity.fullyQualifiedName,
    #         )
    #     )

    # def yield_data(self):
    #     print("inside fetch records.")
    #     try:
    #         for schema in self.get_schemas():
    #             print(f"Schema: {schema}")
    #             database_entity: Database = self.metadata.get_by_name(
    #                 entity=Database, fqn=f"{self.config.serviceName}.{self.database}"
    #             )
    #             print("database_entity.fullyQualifiedName=========>>>>",database_entity.fullyQualifiedName)
    #             yield Either(
    #                 right=CreateDatabaseSchemaRequest(
    #                     name=schema,
    #                     database=database_entity.fullyQualifiedName,
    #                 )
    #             )

    #             for table in self.get_tables(schema):
    #                 print(f"Table: {table}")
    #                 columns = self.get_columns(schema, table)
    #                 for column in columns:
    #                     print(f"Column: {column.name}, Data Type: {column.type}")
         
    #     except Exception as e:
    #         print(f"Error occurred while  fetching hive data: {e}")
    #         raise e

    
    def test_connection(self) -> None:
        pass

    def _iter(self) -> Iterable[Entity]:
        yield from self.yield_create_request_database_service()
        yield from self.yield_creation_db()
        yield from self.get_schemas()
        # yield from self.yield_default_schema()
        # yield from self.yield_data()
       

    def close(self):
        pass
