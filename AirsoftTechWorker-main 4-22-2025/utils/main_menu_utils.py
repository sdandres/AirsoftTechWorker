import pyodbc
from utils.path_utils import get_database_conn_str

def read_active_tickets_from_access():
    """
    Returns a list of dictionaries representing active labor tickets.
    A ticket is considered active if its LaborStatus is not 'Completed' or 'Canceled'.
    Each dictionary contains keys: LaborID, FirstName, LastName, GunModel, and LaborStatus.
    """
    active_tickets = []
    conn = None
    cursor = None
    try:
        conn = pyodbc.connect(get_database_conn_str())
        cursor = conn.cursor()

        query = """
            SELECT l.[LaborID], c.[FirstName], c.[LastName], g.[GunModel], l.[LaborStatus]
            FROM ([Labor] AS l 
            INNER JOIN [Guns] AS g ON l.[GunID] = g.[GunID])
            INNER JOIN [Customer] AS c ON g.[CustomerID] = c.[CustomerID]
            WHERE l.[LaborStatus] NOT IN ('Completed', 'Canceled')
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        for row in rows:
            ticket = dict(zip(columns, row))
            active_tickets.append(ticket)
    except Exception as e:
        print(f"Error reading active tickets: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return active_tickets