#!/bin/python3
"""
The SQLite3_Statements class offers a library of pre-defined SQL statements,
indexed and stored as a human-readable dictionary.

The class object accepts a `database` string that should be a valid
filepath to an sqlite3.db file.  After initialization, member methods
can be called at-will in your code to provide a simple API for database
functionality.
"""


from sqlite3 import connect
from Lab93Cryptogram import CryptographyMethodsAPI as cryptogram




class databaseConnection:
    """
    The SQLite3.databaseConnection object is an internal class used by the
    functionality suite used for abstracting away overhead involved with using
    the built-in sqlite3 library.

    Given a `database` string, which is a valid filepath pointing to a .db file,
    the member objects databaseConnection.connection and
    databaseConnection.cursor are accessibile from a freshly created thread.
    """

    def __init__( self,
                  database: str="./.sqlite3.db" ) -> None:
        try:
            self.connection = connect(
                database
            ); self.cursor = self.connection\
                                 .cursor()
        except Exception as error:
            return error


class databaseInterface:
    def __init__(self):

        ''' Master dictionary of various sqlite3 statements. '''
        self.statements = {
            
            "help": self.listStatements(),


            'queryCompareColumns': {
                # Select a specific column from a row based on another column.
                'execute': self.queryCompareColumns,
                'syntax': "SELECT {} FROM {} WHERE  {}='{}';",
                'help': """SELECT $COLUMN FROM $TABLE WHERE $COMPARATOR = $VALUE;
                
                Returns the value of a specific column if another column equals
                an exact value.

                ARGUMENTS:
                    - database,
                    - column,
                    - table,
                    - comparator,
                    - value


                """
            },


            'createNewColumn': {
                # Add a new column to the database.
                'execute': self.createNewColumn,
                'syntax': "ALTER TABLE {} ADD {} {};",
                'help': """ALTER TABLE $TABLE ADD $COLUMN $TYPE;

                Adds a new $COLUMN of $TYPE to $TABLE.

                ARGUMENTS:
                    - database,
                    - table,
                    - column,
                    - column_type


                """
            },


            'createNewTable': {
                # Create a new new table within the database.
                'execute': self.createNewTable,
                'syntax': "CREATE TABLE IF NOT EXISTS {}({} {} PRIMARY KEY);",
                'help': """CREATE TABLE IF NOT EXISTS $TABLE( $COLUMN $TYPE PRIMARY KEY);

                Create a new table named $TABLE, with an initial compulsory column $COLUMN
                of type $TYPE, which is also a primary key.

                ARGUMENTS:
                    - database,
                    - table,
                    - column,
                    - column_type


                """
            },


            'queryTableData': {
                # Collect everything from a given table.
                'execute': self.queryTableData,
                'syntax': "SELECT * FROM {};",
                'help': """SELECT * FROM $TABLE;
                
                Pulls everything from a table in a form that can be accessed
                like an array.

                ARGUMENTS:
                    - database,
                    - table


                """
            },


            'queryTableExistence': {
                # Check if a specific table exists within the database.
                'execute': self.queryTableExistence,
                'syntax': "SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='{}';",
                'help': """SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name=$TABLE;
                
                Returns either 0 or 1, where 1 means that a $TABLE exists and 0 means
                it does not.

                ARGUMENTS:
                    - database,
                    - table


                """
            },


            # Check a given table for a specific column.
            'queryColumnExistence': {
                'execute': self.queryColumnExistence,
                'syntax': "SELECT COUNT(*) FROM pragma_table_info('{}') WHERE name='{}';",
                'help': """SELECT COUNT(*) FROM pragma_table_info('$COLUMN' WHERE name='$TABLE';)

                Returns either one or zero, where one means that a $COLUMN exists within $TABLE.

                ARGUMENTS:
                    - database,
                    - table,
                    -column


                """
            },
        

            # Enumerate a list of tables within the master record.
            'queryTableList': {
                'syntax': "SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;",
                'execute': self.queryTableList,
                'help': """SELECT name FROM sqlite_schema WHERE type='table ORDER BY name;"

                Curates a list of tables known to a specific $TABLE, alphabatized by name.

                ARGUMENTS:
                    - database


                """
            },
        

            # Curate a list of headers for a given table.
            'queryHeaderList': {
                'syntax': "SELECT name FROM sqlite_master WHERE type='table';",
                'execute': self.queryHeaderList,
                'help': """SELECT name FROM sqlite_master WHERE type='table';

                Curates a list of columns from a given $TABLE.

                ARGUMENTS:
                    - database,
                    - table


                """
            },
        

            # Add a new row to a specific table.
            'createNewUniqueRow': {
                'syntax': "INSERT OR IGNORE INTO {}({}) VALUES({});",
                'execute': self.createNewUniqueRow,
                'help': """INSERT OR IGNORE INTO $TABLE($COLUMNS) VALUES($VALUES);

                Creates a new row in the database, meant to be unique to every other row
                in the database.  In this case, $COLUMNS can be multiple comma separated 
                names, and $VALUES their positionally related data values.

                ARGUMENTS:
                    - database,
                    - table,
                    - columns,
                    - values


                """
            },

        }


    def listStatements():
        for statement in self.statements:
            print(self.statements[statement]["help"])


    def createNewColumn( self, database,
                         table: str="test_table_one",
                         column: str="test_column_one",
                         column_type: str="UNIQUE PRIMARY TEXT" ) -> None:
        """
        SQLite3_Statements.newColumn will create a new header within a table of your choosing.
        It accepts three strings; `table`, `column`, and `column_type`; where `table` is the
        target to be altered, `column` is the label applied to the header, and `column_type`
        are as many (supposedly valid) sQLite3 datatypes as you desire.
    
        Changes made are saved on a successful exit.
        """
        database = databaseConnection(database)
    
        database.cursor\
                .execute( statements['createNewColumn']\
                              .format( table.lower()\
                                            .replace(" ", "-"),
    
                                       column.lower()\
                                             .replace(" ", "-"),
    
                                       column_type.upper()       ) )
    
        return database.connection\
                       .commit()


    def queryCompareColumns( database,
                             column: str="test_column_one",
                             table: str="test_table_one",
                             comparator: str="test_column_two",
                             value: str="test_value_two") -> str:
        """
        SQLite3_Statements.compareColumns describes an easy method to pull a specific
        value from any given line based on a known value within said line.  The exact
        logic behind the query goes like: "SELECT column FROM table WHERE comparator=value".
    
        All arguments are to be given as strings; where `column` describes what to select
        from the `table`, based on a secondary column `comparator` containing the equivalent
        of `value`.
    
        The contents of the `column` search results are then returned to the caller
        as a string.
        """
        database = databaseConnection(database)
        return database.cursor\
                       .execute( statements['queryCompareColumns']\
                                     .format( column,
                                              table,
                                              comparator,
                                              value       )             )\
                       .fetchall()[0][0]
    

    def createNewTable( database,
                        table: str="test_table_one",
                        column: str="test_column_one",
                        column_type: str="UNIQUE TEXT" ) -> None:
        """
        SQLite3_Statements.newTable will create a new `table` initialized with a header
        labeled as `column`; any extra datatypes can be described by `column_type`, but
        the statement includes the PRIMARY KEY types by default.
    
        Changes made to the table are commited upon return.
    
    
        Usage Example:
    
            SQLite3.newTable( DATABASE,
                              table="credentials",
                              column="username",
                              column_type="TEXT"   )
        """
    
        ''' Format command string with argument input. '''
        database = databaseConnection(database)
        database.cursor\
                .execute( statements['createNewTable']\
                              .format ( table.lower()\
                                             .replace(" ", "_"),
    
                                        column.lower()\
                                              .replace(" ", "_"),
    
                                        column_type.upper()       ) )
    
        ''' Save your work. '''
        return database.connection\
                       .commit()


    def queryTableList( database ) -> list:
        """
        Enumerates a list of every table in the database.  Fairly straightforward;
        here's an example.
    
            SQLite3.listTables( SQLite3.databaseConnection("./sqlite.db") )
        """
        database = databaseConnection(database)
        return [
            item for item in database.cursor\
                                     .execute( statements['queryTableList'] )\
                                     .fetchall()
        ]


    def queryTableExistence( database,
                             table: str="test_table_one" ) -> int:
        """
        SQLite3_Statements.checkTable will query the master record for the existence of
        a `table` by the same name as the given argument.
    
        The search will return an integer; where anything over zero(0) describes a
        successful match.
        """
        database = databaseConnection(database)
        return database.cursor\
                       .execute( statements['queryTableExistence']\
                                     .format( table.lower() )          )\
                       .fetchall()[0][0]


    def queryColumnExistence( database,
                              table: str="test_table_one",
                              column: str="test_column_one" ) -> int:
        """
        SQLite3_Statements.checkColumn queries a given `table` for the presence of a header
        labeled `column`; where any return value over zero(0) indicates a match.
        """
        database = databaseConnection(database)
        return database.cursor\
                       .execute( statements['queryColumnExistence']\
                                     .format( table.lower(),
                                              column.lower() )            )\
                       .fetchall()[0][0]
    
    
    def querySelectRow( database,
                        table,
                        column,
                        header,
                        value ):
        """
        """
    
        database = databaseConnection(database)
        return database.cursor\
                       .execute( statements['querySelectRow']\
                                     .format( column.lower(),
                                              table.lower(),
                                              header.lower(),
                                              value         )     )\
                       .fetchall()


    def createNewUniqueRow( database,
                            table: str="test_table_one",
                            columns: str="test_column_one, test_column_two",
                            values: str="test_value_one, test_value_two" ):
        """
        """
    
        database = databaseConnection(database)
        database.cursor\
                .execute( statements['createNewUniqueRow']\
                              .format( table.lower(),
                                       columns.lower(),
                                       values.lower() )  )
    
        return database.connection\
                       .commit()


    def queryCredentials( database, 
                          keyfile:   str  = "./admin.key",
                          values:    str  = "alpaca_key, aplaca_secret",
                          username:  str  = "admin" ):
        """
        Retrieve the administrators Alpaca.Markets API key and secret using his
        credentials from the database.
        """

        # Re-Build the key.
        with open( self.keyfile, "r" ) as secretkey:
            EncryptionKey = cryptogram()\
                                .BuildKey( secretkey.read()\
                                .split("\n")[1] )

        # Select key and secret from credentials database.
        _creds = selectRow( self.database,
                            'credentials', values,
                            'username',    username       )[0]

        # Decrypt key and secret using the users ssh key.
        return ( cryptogram().Decryption( EncryptionKey, _creds[0] ),
                 cryptogram().Decryption( EncryptionKey, _creds[1] )  )
