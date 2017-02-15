"""Class Attendance Register

Usage:
    register.py check in <student_id> <class_id>
    register.py check out <student_id> <class_id> <reason>
    register.py log start <class_id>
    register.py log end <class_id>
    register.py student add
    register.py student remove <student_id>
    register.py student list
    register.py class add
    register.py class remove <class_id>
    register.py class list
    register.py view register
    register.py remove entry <entry_id>

Options:
    -h --help    Show help

"""

from class_definitions import Class, Register, Student
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
    student_id = input("Enter the student id: ")
    first_name = input("Enter the first name: ")
    last_name = input("Enter the second name: ")
    other_name = input("Enter other name: ")

    new_student = Student()
    new_student.add(student_id, first_name, last_name, other_name)

if args['student'] and args['remove']:
    Student().remove(args['<student_id>'])

if args['student'] and args['list']:
    student_list = Student().view_all()
    for student in student_list:
        print("ID: {} Student Name: {} {} {}".format(student.id,
                                                     student.first_name,
                                                     student.other_name,
                                                     student.last_name))

if args['class'] and args['add']:
    class_id = input("Give the class a unique numerical ID: ")
    class_name = input("Give the class a name: ")
    Class().add(class_id=class_id, class_name=class_name)

if args['class'] and args['remove']:
    Class().remove(args['<class_id>'])

if args['class'] and args['list']:
    class_list = Class().view_all()
    for elem in class_list:
        print("ID: {} Class name: {}".format(elem.id, elem.name))

if args['view'] and args['register']:
    entries_list = Register().view_entries()
    for entry in entries_list:
        print("entry_no: {} "
              "class_id: {}, "
              "student_id: {}, "
              "date: {}, "
              "checked_in: {}, "
              "reason: {}".format(entry.entry_id,
                                  entry.class_id,
                                  entry.student_id,
                                  entry.current_date,
                                  entry.checked_in,
                                  entry.reason))

if args['remove'] and args['entry']:
    Register().remove(args['<entry_id>'])





