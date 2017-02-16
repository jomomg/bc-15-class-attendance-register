"""Class Attendance Register

       _   _   _                 _                        ____            _     _
      / \ | |_| |_ ___ _ __   __| | __ _ _ __   ___ ___  |  _ \ ___  __ _(_)___| |_ ___ _ __
     / _ \| __| __/ _ \ '_ \ / _` |/ _` | '_ \ / __/ _ \ | |_) / _ \/ _` | / __| __/ _ \ '__|
    / ___ \ |_| ||  __/ | | | (_| | (_| | | | | (_|  __/ |  _ <  __/ (_| | \__ \ ||  __/ |
   /_/   \_\__|\__\___|_| |_|\__,_|\__,_|_| |_|\___\___| |_| \_\___|\__, |_|___/\__\___|_|
                                                                    |___/

Usage:
    register.py student add
    register.py student remove <student_id>
    register.py student list
    register.py class add
    register.py class remove <class_id>
    register.py class list
    register.py class_students <class_id>
    register.py check in <student_id> <class_id>
    register.py check out <student_id> <class_id> <reason>
    register.py log start <class_id>
    register.py log end <class_id>
    register.py view register
    register.py remove entry <entry_id>

Options:
    -h --help    Show help

"""

from class_definitions import Class, Register, Student
from terminaltables import DoubleTable
from docopt import docopt


args = docopt(__doc__)

if args['check'] and args['in']:
    Student().check_in(args['<student_id>'], args['<class_id>'])

if args['check'] and args['out']:
    Student().check_out(args['<student_id>'], args['<class_id>'], args['<reason>'])

if args['log'] and args['start']:
    Class().log_start(args['<class_id>'])

if args['log'] and args['end']:
    Class().log_end(args['<class_id>'])

if args['student'] and args['add']:
    print()
    first_name = input("Enter the first name: ")
    last_name = input("Enter the second name: ")
    other_name = input("Enter other name: ")

    Student().add(first_name, last_name, other_name)

if args['student'] and args['remove']:
    Student().remove(args['<student_id>'])

if args['student'] and args['list']:
    student_list = Student().view_all
    student_table_data = [
        ["Student ID", "First Name", "Other Name", "Last Name"]
    ]
    for student in student_list:
        student_table_data.append([student.id, student.first_name, student.other_name, student.last_name])

    student_table = DoubleTable(student_table_data, "Students")
    print()
    print(student_table.table)

if args['class'] and args['add']:
    class_name = input("Give the class a name: ")
    Class().add(class_name=class_name)

if args['class'] and args['remove']:
    Class().remove(args['<class_id>'])

if args['class'] and args['list']:
    class_list = Class().view_all
    if class_list is None:
        print("No classes were found")
    else:
        class_table_data = [
            ["Class ID", "Class Name","Start Time", "End time"]
        ]
        for elem in class_list:
            class_table_data.append([elem.id, elem.name, elem.start, elem.end])

        class_table = DoubleTable(class_table_data, "Classes")
        print()
        print(class_table.table)

if args['view'] and args['register']:
    entries_list = Register().view_entries
    entries_table_data = [
        ["Entry No.", "Class ID", "Student ID", "Date", "Checked in", "Reason"],
    ]
    for entry in entries_list:
        entries_table_data.append([entry.entry_id,
                                   entry.class_id,
                                   entry.student_id,
                                   entry.current_date,
                                   entry.checked_in,
                                   entry.reason])

    entries_table = DoubleTable(entries_table_data, "Register Entries")
    print()
    print(entries_table.table)

if args['remove'] and args['entry']:
    Register().remove(args['<entry_id>'])

if args['class_students']:
    class_students = Class().view_students(args['<class_id>'])
    if class_students is None:
        print("No students were found in the class")
    else:
        class_students_table_data = [
            ["Student ID:", "First Name", "Other Name", "Last Name"]
        ]
        for student in class_students:
            class_students_table_data.append([student.id, student.first_name, student.other_name, student.last_name])
        class_students_table = DoubleTable(class_students_table_data, "Class ID: {}".format(args['<class_id>']))
        print()
        print(class_students_table.table)
