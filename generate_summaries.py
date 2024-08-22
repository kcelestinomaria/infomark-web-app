import sqlite3
import pandas as pd
from datetime import datetime

'''
This is a CRON Job, used to generate summaries of the data
created and stored in the Infomark Web App
'''

def generate_summary():
    # Connect to the database
    conn = sqlite3.connect('app_database.db')
    cursor = conn.cursor()

    # Fetch summary data from different tables
    summaries = {}

    # Example summary for Users
    cursor.execute('SELECT COUNT(*) FROM Users')
    summaries['total_users'] = cursor.fetchone()[0]

    # Example summary for DataRequests
    cursor.execute('SELECT data_type, COUNT(*) FROM DataRequests GROUP BY data_type')
    data_requests = cursor.fetchall()
    summaries['data_requests'] = {row[0]: row[1] for row in data_requests}

    # Close the connection
    conn.close()

    # Save the summary to a file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    summary_file = f'./_{timestamp}.csv'
    pd.DataFrame([summaries]).to_csv(summary_file, index=False)

if __name__ == '__main__':
    generate_summary()
