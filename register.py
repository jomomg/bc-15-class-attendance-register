"""Class Attendance Register

Usage:
    register.py student_add
    register.py student_remove <student_id>
    register.py student_list
    register.py class_add
    register.py class_remove <class_id>
    register.py class_list
    register.py class_students <class_id>
    register.py check_in <student_id> <class_id>
    register.py check_out <student_id> <class_id>
    register.py log_start <class_id>
    register.py log_end <class_id>
    register.py view_register
    register.py remove_entry <entry_id>

Options:
    -h --help    Show help

"""

from class_definitions import Class, Register, Student
from terminaltables import DoubleTable
from docopt import docopt, DocoptExit
from database import create_db
import cmd
import os


def docopt_cmd(func):
    def fn(self, args):
        try:
            opt = docopt(fn.__doc__, args)
        except DocoptExit as e:
            print(e)
            return
        except SystemExit:
            return
        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


def banner():
    print("       _   _   _                 _                        ____            _     _                 ")
    print("      / \ | |_| |_ ___ _ __   __| | __ _ _ __   ___ ___  |  _ \ ___  __ _(_)___| |_ ___ _ __      ")
    print("     / _ \| __| __/ _ \ '_ \ / _` |/ _` | '_ \ / __/ _ \ | |_) / _ \/ _` | / __| __/ _ \ '__|     ")
    print("    / ___ \ |_| ||  __/ | | | (_| | (_| | | | | (_|  __/ |  _ <  __/ (_| | \__ \ ||  __/ |        ")
    print("   /_/   \_\__|\__\___|_| |_|\__,_|\__,_|_| |_|\___\___| |_| \_\___|\__, |_|___/\__\___|_|        ")
    print("                                                                    |___/                         ")
    print("__________________________________________________________________________________________________")


class AttendanceRegister(cmd.Cmd):
    prompt = "register>>>"

    @docopt_cmd
    def do_student_add(self, args):
        """Usage: student_add"""
        print()
        first_name = input("Enter the first name: ")
        last_name = input("Enter the second name: ")
        other_name = input("Enter other name: ")
        Student().add(first_name, last_name, other_name)

    @docopt_cmd
    def do_student_remove(self, args):
        """Usage: student_remove <student_id>"""
        Student.remove(args["<student_id>"])

    @docopt_cmd
    def do_check_in(self, args):
        """Usage: check_in <student_id> <class_id>"""
        Student.check_in(args["<student_id>"], args["<class_id>"])

    @docopt_cmd
    def do_check_out(self, args):
        """Usage: check_out <student_id> <class_id>"""
        reason = input("Give a reason: ")
        Student.check_out(args["<student_id>"], args["<class_id>"],reason)

    @docopt_cmd
    def do_log_start(self, args):
        """Usage: log_start <class_id>"""
        Class.log_start(args["<class_id>"])

    @docopt_cmd
    def do_log_end(self, args):
        """Usage: log_end <class_id>"""
        Class.log_end(args["<class_id>"])

    @docopt_cmd
    def do_student_list(self, args):
        """Usage: student_list"""
        student_list = Student().view_all
        student_table_data = [
            ["Student ID", "First Name", "Other Name", "Last Name"]
        ]
        for student in student_list:
            student_table_data.append([student.id, student.first_name, student.other_name, student.last_name])

        student_table = DoubleTable(student_table_data, "Students")
        print()
        print(student_table.table)

    @docopt_cmd
    def do_class_add(self, args):
        """Usage: class_add"""
        class_name = input("Give the class a name: ")
        Class.add(class_name=class_name)

    @docopt_cmd
    def do_class_remove(self, args):
        """Usage: class_remove <class_id>"""
        Class.remove(args["<class_id>"])

    @docopt_cmd
    def do_class_list(self, args):
        """Usage: class_list"""
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
            print(class_table.table)

    @docopt_cmd
    def do_view_register(self, args):
        """Usage: view_register"""
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

    @docopt_cmd
    def do_remove_entry(self, args):
        """Usage: remove_entry"""
        Register.remove(args['<entry_id>'])

    @docopt_cmd
    def do_class_students(self, args):
        """Usage: class_students"""
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

if __name__ == "__main__":
    try:
        os.system("cls")
        create_db()
        banner()
        print()
        print(__doc__)
        AttendanceRegister().cmdloop()
    except KeyboardInterrupt:
        os.system("cls")
        print("Adios")
