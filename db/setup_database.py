from db.config import DB_CONFIG
import mysql.connector

def read_sql_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def execute_sql_script(script):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )

        cursor = conn.cursor()
        sql_commands = script.split(';')
        for command in sql_commands:
            command = command.strip()
            if command != '':
                cursor.execute(command)
        conn.commit()
        print("Khởi tạo database thành công!")
    except mysql.connector.Error as err:
        print(f"Lỗi khi khởi tạo database: {err}")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

def main():
    sql_script = read_sql_file('sql/init_db.sql')
    execute_sql_script(sql_script)

if __name__ == "__main__":
    main()