#!/usr/bin/env python

"""
A simple database that stores tasks to along with their status

Table in database
+----+------+------+--------+
| ID | Date | Task | Status |     
+----+------+------+--------+
"""

import MySQLdb
import getpass, sys
from datetime import date


def show_submenu(db, tasks):
	
	while (True):
		cmd = raw_input("Press 1 to change task status or any other key to return ")
		if (cmd != "1"):
			break
		else:
			match_found = False
			task_id = raw_input("Enter task ID to change: ")
			for task in tasks:
				if (task[0] == int(task_id)):
					match_found = True
					# reverse task status
					if (task[3] == "Pending"):
						state = "Done"
					else:
						state = "Pending"

					sql = """Update Tasks set Status = \"%s\" where ID = %s""" \
					% (state, task_id)

					try:
						db.cursor().execute(sql)
						db.commit()
					except:
						db.rollback()
						print "Failed to update task state"
						sys.exit(1)

			# Task ID not matched
			if (not match_found):
				print "Invalid Task ID entered"	


""" Create a table in database """
def create_table(db):
	sql = \
"""CREATE TABLE Tasks (
	ID INT AUTO_INCREMENT,
	Date VARCHAR(100),
	Task VARCHAR(200),
	Status VARCHAR(50),
	PRIMARY KEY ( ID )
)"""
	try :
		db.cursor().execute(sql)
	except:
		print "Error in executing SQL query"


""" Add task to database table """
def add_to_table(db, Date, Task, Status):
	sql = \
"""
INSERT INTO Tasks (
	Date, Task, Status)
VALUES ( \"%s\", \"%s\", \"%s\")""" \
	% (Date, Task, Status)

	print sql
	
	try:
		db.cursor().execute(sql)
		db.commit()
	except:
		print "Failed to add task to database"
		db.rollback()
		sys.exit(1)


""" Create task from user input """
def create_task(current_date = True):
	task = {}
	task["Date"] = date.today()
	task["Task"] = raw_input("Enter task description: ")
	done = raw_input("Mark task done? [y/N]: ")
	if (done == "y" or done == "Y"):
		task["Status"] = "Done"
	else:
		task["Status"] = "Pending"

	return task


def show_tasks(db, task_date):
	sql = \
""" SELECT * from Tasks where Date = \"%s\"""" % task_date

	try:
		cursor = db.cursor()
		cursor.execute(sql);
	except:
		print "Failed to get data from database"
		sys.exit(1)

	tasks = cursor.fetchall()
	
	print """ID\tTask Description\tTask Date\tTask Status"""
	for task in tasks:
		print "%d. %s\t%s\t%s" % (task[0], task[2], task[1], task[3])	
	show_submenu(db, tasks)


username = raw_input("Enter a username: ");
password = getpass.getpass("Enter database password: ");

try:
	db = MySQLdb.connect("localhost", username, password, db = "MYTASKS");
except:
	print "Failed to load database"
	sys.exit(1);

create_table(db)

def show_menu():
	print  \
"""Please Select an option:
1. Show today's tasks (press key to update task status )
2. Show last 7 days tasks
3. Show tasks by date
4. Enter a task
5. Quit
"""

show_menu()

while (True):
	option = raw_input()
	
	if (option == "5"):
		print "Bye Bye. Don't forget to check again later"
		sys.exit(0)
	elif (option == "4"):
		task = create_task()
		add_to_table(db, **task)
	elif (option == "1"):
		show_tasks(db, date.today())
	
	show_menu()
