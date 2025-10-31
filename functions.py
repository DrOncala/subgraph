

############################################################################

import io
import sys
import datetime

def print_info(info):
    # Redirect standard output to a string buffer
    #stdout = io.StringIO()
    #sys.stdout = stdout

    # Perform some prints
    captured_output=f"{info}\n"

    # Restore standard output and get captured output
    #sys.stdout = sys.__stdout__
    #captured_output = stdout.getvalue()

    # Write captured output to file
    with open("info.txt", "a") as f:
        f.write(captured_output)
    
    return  print(captured_output)
        


############################################################################


import pandas as pd
import psycopg2
from psycopg2 import extras
from sqlalchemy import create_engine

def download(database, table):
    """
    This function establishes a connection to a PostgreSQL database and downloads a specified table from the database
    as a pandas DataFrame.

    Args:
        database (str): The name of the PostgreSQL database where the data is stored.
        table (str): The name of the table within the database to be downloaded.

    Returns:
        df (pandas.DataFrame): A pandas DataFrame containing the data from the specified table.
    """
    try:
        # Create a connection to the database
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database=database,
            user="postgres",
            password="123"
        )

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Execute a query
        cur.execute(f"SELECT * FROM {table}")
        colnames = [desc[0] for desc in cur.description]

        # Fetch all the rows in the result set
        rows = cur.fetchall()

        # Close the cursor and the connection
        cur.close()
        conn.close()

        # Convert the rows to a pandas dataframe
        df = pd.DataFrame(rows, columns=colnames)

        return df

    except psycopg2.Error as e:
        print(e)


############################################################################


import pandas as pd
def slope(subGraph):
# Create an empty DataFrame
    df = pd.DataFrame(columns=['code', 'slope'])

    for node1, node2, data_arc in subGraph.edges(data=True):
        node_data1 = subGraph.nodes[node1]
        node_data2 = subGraph.nodes[node2]

        elev1 = node_data1['custom_top_elev'] - data_arc['custom_y1']
        elev2 = node_data2['custom_top_elev'] - data_arc['custom_y2']
        slope = (elev1 - elev2)# / data_arc['gis_length']
        
        if slope < 0:
            # Check if 'code' already exists in the DataFrame
            if data_arc['code'] in df['code'].values:
                # Update the corresponding row
                df.loc[df['code'] == data_arc['code'], 'slope'] = min(df.loc[df['code'] == data_arc['code'], 'slope'], slope)
            else:
                # Add a new row to the DataFrame
                df = df.append({'code': data_arc['code'], 'slope': slope}, ignore_index=True)

    # Print the DataFrame
    return df.sort_values(by='slope')
