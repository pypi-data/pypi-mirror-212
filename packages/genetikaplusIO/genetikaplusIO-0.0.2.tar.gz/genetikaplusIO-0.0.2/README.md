# **GPIO Package**

The GPIO package is a Python package that provides functionality for managing input/output operations related to
Postgres databases and file storage.
It consists of two modules: db and storage.

## **Installation**

To install the genetikaplusIO package, you can use pip:

`pip install genetikaplusIO`

To install 
## Modules

### gp_db_io

The gp_db_io module provides functions for interacting with Postgres databases.

#### Usage
```
import gp_db_io

# Read sqlQuery to a pandas dataframe
df = db.dbReadQuery(query: str, database: str = "gbase", **kwargs)

# Execute query
db.dbExecuteQuery(query, database)

db.dbExecuteReturn(query, database)

# Get list of schemas
schemas = db.dbListSchemas(database)

# Get list of tables in a specific schema
tables_list = db.dbListTables(schema, database)

# Read table
table = db.dbReadTable(tableName, schema, database, index_col)

db.dbExistsTable(tableName,schema,database)

# Creating a new schema
db.dbCreateSchema(newSchemaName, database)

# Delete an existing schema
db.dbDeleteSchema(schema, database)

# Delete an existing table
db.dbRemoveTable(tableName, schema, database)

# Creating a new table/Appending to an existing table 
db.dbWriteTable(df,
                tableName,
                override,
                schema,
                append,
                database,
                **kwargs
                )

# Append partial columns to a table
db.dbAppendTablePartialColumns(df,
                               tableName,
                               schema,
                               database,
                               append,
                               row_names,
                               row_names_label,
                               **kwargs)

# Disconnect sqlconnection
db.dbDisconnect(connection)
```
## gp_storage_io
The gp_storage_io module provides functions for interacting with file storage.
## Usage
```
import gp_storage_io

# Check existent of a file
bool = storage.is_file_exist(filname: str)

# Reformat path so it will fit the loacal computer
format = storage.format_file_path(filename: str)
 
 # Read csv file to a pandas data frame 
df = storage.read_csv(filename: str, header=True, **kwargs)

# Read xlsx file to a pandas data frame
df = storage.read_excel(filename, **kwargs)

# List all files in a givven directory path
list = storage.list_files(path: str)

# Save a figure
storage.ggsave(fig: matplotlib.figure.Figure, path: str, format: str = "png", **kwargs)

# Write the data frame as an xlsx file 
storage.write_xlsx(df: pd.DataFrame, path: str, **kwargs)

# Right the data frame as a csv file
storage.write_csv(df: pd.DataFrame, path: str, **kwargs)

```
### gp_sqlconnection

The gp_sqlconnection module provides direct connection with sql to perform more specific queries that db does not provide.

#### Usage
```
# Returns a new connection object
connection = make_connection(database)

# Returns a nwe connection for using pandas specifically
pandas_connection = make_pandas_connection(database)

# Execute query and return a value if return_value=True
optional_value = execute_query(connection, query, return_value)

# Creates engine object for some functions that needs it, like pd.to_sql()
engine = create_engine_for_pd(database)
```

## Contributing

Contributions to the GPIO package are welcome! If you find any issues or have suggestions for improvements,
please contact through the email below

## License

The GPIO package is released under the MIT License. See the LICENSE file for more details.

## Contact

alon@genetikaplus.com

