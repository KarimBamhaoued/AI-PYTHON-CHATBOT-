# Connect to the database
import pymysql

mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="employees",
)
print("Database connection object:", mydb)

# Prepare a cursor object
mycursor = mydb.cursor()

# Execute a SELECT statement to retrieve data from the employees table
try:
    mycursor.execute("SELECT first_name FROM employees.employees WHERE emp_no = 10001")
except Exception as e:
    print("Error executing SELECT statement:", e)
    # Close the cursor and database connections
    mycursor.close()
    mydb.close()
    exit()

# Fetch all rows and store them in a list
try:
    employee_data = mycursor.fetchall()
except Exception as e:
    print("Error fetching data from SELECT statement:", e)
    # Close the cursor and database connections
    mycursor.close()
    mydb.close()
    exit()

# Iterate through the employee_data list and print each row
for row in employee_data:
    print(row)

# Close the cursor and database connections
mycursor.close()
mydb.close()
