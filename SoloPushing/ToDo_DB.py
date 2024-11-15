import mysql.connector
from mysql.connector import Error


def Data_Base():
    return mysql.connector.connect(host="localhost",
                                   user="root",
                                   password="1234",
                                   database="todo_db")


try:
    data_base = Data_Base()
    if data_base.is_connected():
        cursor = data_base.cursor()

        # Specify columns in the create table query
        query_tasks = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task_name VARCHAR(255),
            due_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        query_completed_tasks = """
        CREATE TABLE IF NOT EXISTS completed_tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task_name VARCHAR(255),
            due_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        cursor.execute(query_tasks)
        cursor.execute(query_completed_tasks)
        data_base.commit()

        # Close cursor and connection
        cursor.close()
        data_base.close()

        # print('Executed')

except Error as e:
    print(f'Error: {e}')


#insert into tasks (task_name) values ('test1');
def create_task(input_task, status=None):
    if status == "create":
        query = f"INSERT INTO tasks (task_name) VALUES ('{input_task}');"
    elif status == "uncheck":
        query = f"INSERT INTO completed_tasks (task_name) VALUES ('{input_task}');"
    data_base = Data_Base()
    cursor = data_base.cursor()
    cursor.execute(query)
    data_base.commit()
    data_base.close()
    # print(f'Created :{input_task}')


# UC means User Choice :D
def read_tasks(
    type_UC=None,
    status=None,
):
    if status == "A-Z":
        query = f"SELECT task_name from {type_UC} ORDER BY task_name ASC;"
    elif status == "Z-A":
        query = f"SELECT task_name from {type_UC} ORDER BY task_name DESC;"
    elif status == "New-Old":
        query = f"SELECT task_name from {type_UC} ORDER BY due_date DESC"
    elif status == "Old-New":
        query = f"SELECT task_name from {type_UC} ORDER BY due_date ASC"
    else:
        query = f"SELECT task_name from {type_UC};"
    data_base = Data_Base()
    cursor = data_base.cursor()

    cursor.execute(query)
    output = cursor.fetchall()
    final_output = []
    for row in output:
        for neat in row:
            final_output.append(neat)
    return final_output


def delete_tasks(input_task, status=None):
    if status == "create":
        query = f"DELETE FROM tasks WHERE task_name = '{input_task}';"
    elif status == "completed":
        query = f"DELETE FROM completed_tasks WHERE task_name = '{input_task}';"
    data_base = Data_Base()
    cursor = data_base.cursor()

    # Disable safe updates
    cursor.execute("SET SQL_SAFE_UPDATES = 0;")

    # Delete the task

    cursor.execute(query)

    # Commit changes and close the connection
    data_base.commit()
    data_base.close()
    # print(f"Deleted: {input_task}")


def return_active_status(task_name):
    query = f"SELECT active_status FROM tasks WHERE task_name = '{task_name}';"
    data_base = Data_Base()
    cursor = data_base.cursor()
    cursor.execute("SET SQL_SAFE_UPDATES = 0;")
    cursor.execute(query)
    output = cursor.fetchall()

    for row in output:
        for neat in row:
            return neat


def return_remaining_time(task_name):
    query = f"SELECT remaining_time FROM tasks WHERE task_name = '{task_name}';"
    data_base = Data_Base()
    cursor = data_base.cursor()
    cursor.execute("SET SQL_SAFE_UPDATES = 0;")
    cursor.execute(query)
    output = cursor.fetchall()

    for row in output:
        for neat in row:
            return neat


def update_remaining_time(task_name, remaining_time):
    query = f"UPDATE tasks SET remaining_time = '{remaining_time}' WHERE task_name = '{task_name}';"
    data_base = Data_Base()
    cursor = data_base.cursor()
    cursor.execute("SET SQL_SAFE_UPDATES = 0;")
    cursor.execute(query)
    data_base.commit()
    data_base.close()
    # print(f"Updated remaining_time: {remaining_time} for {task_name}")


def update_active_status(task_name, active_status):
    query = f"UPDATE tasks SET active_status = '{active_status}' WHERE task_name = '{task_name}';"
    data_base = Data_Base()
    cursor = data_base.cursor()
    cursor.execute("SET SQL_SAFE_UPDATES = 0;")
    cursor.execute(query)
    data_base.commit()
    data_base.close()
    # print(f"Updated active_status: {active_status} for {task_name}")
