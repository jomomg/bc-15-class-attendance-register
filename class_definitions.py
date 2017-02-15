from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import database
from datetime import datetime

engine = create_engine('sqlite:///attendance_register.db')
database.Base.metadata.create_all(engine)
database.Base.metadata.bind = engine
DB_session = sessionmaker(bind=engine)
session = DB_session()


class Class:

    def __init__(self):
        self.class_id = None
        self.class_name = None
        self.start_time = None
        self.end_time = None

    def add(self, class_id, class_name):
        self.class_id = class_id
        self.class_name = class_name
        new_class = database.ClassTable(id=self.class_id, name=self.class_name)
        session.add(new_class)
        session.commit()

    def remove(self, class_id):
        self.class_id = class_id
        class_to_remove = session.query(database.ClassTable).get(self.class_id)
        if class_to_remove is None:
            print("The specified class id does not exist")
        else:
            session.delete(class_to_remove)
            session.commit()

    def log_start(self, class_id):
        self.class_id = class_id
        self.start_time = datetime.now()
        class_to_log = session.query(database.ClassTable).get(self.class_id)
        if class_to_log is None:
            print("The specified class id does not exist")
        else:
            class_to_log.start = self.start_time
            session.commit()

    def log_end(self, class_id):
        self.class_id = class_id
        self.end_time = datetime.now()
        class_to_log = session.query(database.ClassTable).get(self.class_id)
        if class_to_log.start is None:
            print("You must log start before you can log end")
        else:
            class_to_log.end = self.end_time
            session.commit()

    def view_all(self):
        all_classes = session.query(database.ClassTable).all()
        if all_classes is None:
            print("There are no classes in the database")
        else:
            return all_classes


class Register:
    def __init__(self):
        self.entry_id = None
        self.class_id = None
        self.student_id = None
        self.current_date = None
        self.checked_in = False
        self.reason = None

    def update(self, class_id, student_id):
        self.class_id = class_id
        self.student_id = student_id
        new_entry = database.Register(class_id=self.class_id,
                                      student_id=self.student_id,
                                      current_date=datetime.now(),
                                      checked_in=True)
        session.add(new_entry)
        session.commit()

    def remove(self, entry_id):  # remove entries from the register
        self.entry_id = entry_id
        entry_to_remove = session.query(database.Register).get(entry_id)
        if entry_to_remove is None:
            print("The entry id specified was not found. Use [view register] to see available entries")
        else:
            session.delete(entry_to_remove)
            session.commit()
            print("Successfully removed entry no. {}".format(entry_to_remove.entry_id))

    def view_entries(self):   # view by class or student
        all_entries = session.query(database.Register).all()
        if all_entries is None:
            print("There are no entries in the register")
        else:
            return all_entries


class Student:
    def __init__(self):
        self.student_id = None
        self.first_name = None
        self.last_name = None
        self.other_name = None
        self.class_id = None

    def add(self, student_id, first_name, last_name, other_name):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.other_name = other_name

        new_student = database.Student(id=self.student_id,
                                       first_name=self.first_name,
                                       last_name=self.last_name,
                                       other_name=self.other_name)
        if new_student is None:
            print("Failed to add new student")
        else:
            session.add(new_student)
            session.commit()
            print("Successfully added {} {} {}".format(new_student.first_name,
                                                       new_student.other_name,
                                                       new_student.last_name))

    def remove(self, student_id):
        self.student_id = student_id
        student_to_remove = session.query(database.Student).get(student_id)
        if student_to_remove is None:
            print("The student id specified was not found")
        else:
            session.delete(student_to_remove)
            session.commit()
            print("Successfully removed {} {} {}".format(student_to_remove.first_name,
                                                         student_to_remove.other_name,
                                                         student_to_remove.last_name))

    def check_in(self, student_id, class_id):
        # todo: make sure that a student cannot check in to more than one class at a time
        self.student_id = student_id
        self.class_id = class_id
        student_to_check = session.query(database.Student).get(self.student_id)
        class_to_check = session.query(database.ClassTable).get(self.class_id)
        if student_to_check or class_to_check is None:
            print("You entered a class id or student id that does not exist")
        else:
            Register().update(self.class_id, self.student_id)

    def check_out(self, student_id, class_id, reason):
        # todo: make sure that a student can only check out only if he/she has checked in
        self.student_id = student_id
        self.class_id = class_id
        student_to_check_out = session.query(database.Register).\
            filter(database.Register.student_id == student_id,
                   database.Register.class_id == self.class_id)
        if student_to_check_out is None:
            print("The specified student was not found")
        else:
            student_to_check_out.checked_in = False
            student_to_check_out.reason = reason

    def view_all(self):
        all_students = session.query(database.Student).all()
        return all_students
