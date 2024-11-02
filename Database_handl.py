import sqlite3

# Function to create a SQLite database
def create_database(db_name):
    conn = sqlite3.connect(f"{db_name}.db")
    conn.close()

# Function to connect to an existing SQLite database
def connect_database(db_name):
    conn = sqlite3.connect(f"{db_name}.db")
    return conn

# Function to create a table with dynamic columns
def create_table(conn, table_name, columns):
    cur = conn.cursor()
    # Creating column definitions
    columns_definition = ", ".join([f"{col} TEXT" for col in columns])
    # Creating table query
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})")
    conn.commit()

# Function to insert data into a table
def insert_data(conn, table_name, columns, data):
    cur = conn.cursor()
    # Creating placeholder string for values
    placeholders = ", ".join("?" * len(columns))
    # Insert query
    cur.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})", data)
    conn.commit()

# Function to insert data into a table using a dictionary
def insert_data_dict(conn, table_name, columns, data_dict):
    cur = conn.cursor()
    # Filter out columns that are not in the dictionary (i.e., missing data)
    valid_columns = [col for col in columns if col in data_dict]
    # Prepare the placeholder string for valid columns
    placeholders = ", ".join("?" for _ in valid_columns)
    # Get the corresponding values from the dictionary for the valid columns
    values = [data_dict[col] for col in valid_columns]
    
    # Insert query based on valid columns and values
    cur.execute(f"INSERT INTO {table_name} ({', '.join(valid_columns)}) VALUES ({placeholders})", values)
    conn.commit()

# Function to read and print all data from a table
def read_data(conn, table_name):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    # Print each row of data
    for row in rows:
        print(row)

# Example usage
if __name__ == "__main__":
    db_name = "test_db"
    table_name = "test_table"
    columns = ["name", "age", "city"]
    
    # Data with potentially missing or unordered columns
    data_dict = {
        "city": "New York",
        "name": "John",
        # "age" is missing
    }

    # Create database
    create_database(db_name)

    # Connect to the database
    conn = connect_database(db_name)

    # Create a table (if not already exists)
    create_table(conn, table_name, columns)

    # Insert data using the dictionary
    insert_data_dict(conn, table_name, columns, data_dict)

    # Read and print the data
    read_data(conn, table_name)

    # Close the connection
    conn.close()