import sqlite3

def get_distance(origin, destination):
    # Create a connection to the SQLite database
    conn = sqlite3.connect('FlightData.db')
    # Create a cursor
    cur = conn.cursor()
    # Execute a query
    cur.execute('SELECT DISTANCE FROM flight_data WHERE ORIGIN = ? AND DEST = ?', (origin, destination))
    # Fetch the results
    data = cur.fetchone()
    # Close the connection
    conn.close()

    if data is not None:
        return data[0]
    else:
        return 'No data found for route from {origin} to {destination}.'.format(origin=origin, destination=destination)

print(get_distance('GNV', 'ATL'))

