import os
import sqlite3

# HIGH RISK: Hardcoded AWS Credentials
AWS_ACCESS_KEY_ID = "AKIAEXAMPLE123456789"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def get_user_info(user_id):
    # HIGH RISK: SQL Injection
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    cursor.execute(query)
    return cursor.fetchone()

def run_command(command):
    # HIGH RISK: Command Injection
    os.system(command)

if __name__ == "__main__":
    print("Vulnerable service is running...")
