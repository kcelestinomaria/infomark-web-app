import sqlite3
import pandas as pd

def export_to_excel(filename="Business_Data_Reports.xlsx"):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('app_database.db')
        
        # Query data from the tables
        users_df = pd.read_sql_query("SELECT * FROM Users", conn)
        profile_pictures_df = pd.read_sql_query("SELECT * FROM ProfilePictures", conn)
        search_history_df = pd.read_sql_query("SELECT * FROM SearchHistory", conn)
        data_requests_df = pd.read_sql_query("SELECT * FROM DataRequests", conn)
        favorites_df = pd.read_sql_query("SELECT * FROM Favorites", conn)
        
        # Create a Pandas Excel writer using Openpyxl as the engine
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            users_df.to_excel(writer, sheet_name='Users', index=False)
            profile_pictures_df.to_excel(writer, sheet_name='ProfilePictures', index=False)
            search_history_df.to_excel(writer, sheet_name='SearchHistory', index=False)
            data_requests_df.to_excel(writer, sheet_name='DataRequests', index=False)
            favorites_df.to_excel(writer, sheet_name='Favorites', index=False)
        
        print(f"Data exported successfully to {filename}")
        return True
    
    except Exception as e:
        print(f"An error occurred while exporting data: {e}")
        return False
