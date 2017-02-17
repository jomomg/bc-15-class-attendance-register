from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import database
from datetime import datetime

engine = create_engine("sqlite:///attendance_register.db")
database.Base.metadata.bind = engine
DB_session = sessionmaker(bind=engine)
session = DB_session()


class Class:
    """Encapsulates methods used to interface with the class table

       Attributes:
           class_id (int): the numerical id of a given class
           class_name (str): the name of a given class
           start_time (tuple): the start time of a given class
           end_time (tuple): the end time of a given class
    """

    def __init__(self):
        self.class_id = None
        self.class_name = None
        self.start_time = None
        self.end_time = None

    @classmethod
    def add(cls, class_name):
        """Add a new class to the class table

           Args:
               class_name (str): the name of a given class
        """

        cls.class_name = class_name
        new_class = database.ClassTable(name=cls.class_name)
        session.add(new_class)
        session.commit()
        print("Successfully added '{}'".format(cls.class_name))

    @classmethod
    def remove(cls, class_id):
        """Removes a class from the class table

           Args:
               class_id (int): the id of a given class
        """

        cls.class_id = class_id
        class_to_remove = session.query(database.ClassTable).get(cls.class_id)
        if class_to_remove is None:
            print("The specified class id does not exist")
        else:
            session.delete(class_to_remove)
            session.commit()
            print("Successfully removed '{}'".format(class_to_remove.name))

    @classmethod
    def log_start(cls, class_id):
        """Logs the start time of a specified class id

           Args:
               class_id (int): the id of a given class
        """

        cls.class_id = class_id
        cls.start_time = datetime.now()
        class_to_log = session.query(database.ClassTable).get(cls.class_id)
        if class_to_log is None:
            print("The specified class id does not exist")
        else:
            class_to_log.start = cls.start_time
            session.commit()
            print("Started the log for the {} class".format(class_to_log.name))

    @classmethod
    def log_end(cls, class_id):
        """Logs the end time of a specified class id that has already been started

           Args:
               class_id (int): the id of a given class
        """

        cls.class_id = class_id
        cls.end_time = datetime.now()
        class_to_log = session.query(database.ClassTable).get(cls.class_id)
        if class_to_log.start is None:
            print("You must log start before you can log end")
        else:
            class_to_log.end = cls.end_time
            session.commit()
            print("Ended the log for the '{}' class".format(class_to_log.name))

    @property
    def view_all(self):

        """View all the classes in the class table

           Returns:
               None: if no classes are found
               all_classes: all the classes found
        """

        all_classes = session.query(database.ClassTable).all()
        if all_classes is None:
            return None
        else:
            return all_classes

    @classmethod
    def view_students(cls, class_id):

        """View all students with a given class id

           Args:
               class_id (int): the id of a given class

            Returns:
                None: if no students found
                students_to_view: all the students found
        """

        cls.class_id = class_id
        students_to_view = session.query(database.Student).filter(database.Student.class_id == cls.class_id).all()
        if students_to_view is None:
            return None
        else:
            return students_to_view

class Register:
    """Encapsulates the methods and attributes and methods used to interface with the register table

       Attributes:
           entry_id (int): unique id for each register entry in the register table
           class_id (int): id of the class in the register entry
           student_id (int): the id of the student in the register entry
           current_date (tuple): the date the register entry was made
           checked_in (boolean): is a student checked in or not
           reason (str): if the student is checked out of a class, the supplied reason
    """
    def __init__(self):
        self.entry_id = None
        self.class_id = None
        self.student_id = None
        self.current_date = None
        self.checked_in = False
        self.reason = None

    @classmethod
    def update(cls, class_id, student_id):

        """Update the register table with a new student id and class id

           Args:
               class_id (int): the id of the class to be checked in to the register table
               student_id (int): the id of the student to be checked in to the register table
        """

        cls.class_id = class_id
        cls.student_id = student_id
        new_entry = database.Register(class_id=cls.class_id,
                                      student_id=cls.student_id,
                                      current_date=datetime.now(),
                                      checked_in=True)
        session.add(new_entry)
        session.commit()

    @classmethod
    def remove(cls, entry_id):

        """Remove an entry from the register table

           Args:
               entry_id (int): the id of the entry to be removed from the register table
        """

        cls.entry_id = entry_id
        entry_to_remove = session.query(database.Register).get(entry_id)
        if entry_to_remove is None:
            print("The entry id specified was not found. Use [view register] to see available entries")
        else:
            session.delete(entry_to_remove)
            session.commit()
            print("Successfully removed entry no. {}".format(entry_to_remove.entry_id))

    @property
    def view_entries(self):
        """View all entries in the register table"""

        all_entries = session.query(database.Register).all()
        if all_entries is None:
            print("There are no entries in the register")
        else:
            return all_entries


class Student:
    """Encapsulates the methods and attributes used to interface with the student table

       Attributes:
           student_id (int): id of the student
           first_name (str): first name of the student
           last_name (str): last name of the student
           other_name (str): any other name the student might have
    """
    def __init__(self):
        self.student_id = None
        self.first_name = None
        self.last_name = None
        self.other_name = None
        self.class_id = None

    @classmethod
    def add(cls, first_name, last_name, other_name):

        """Add a new student to the student table

           Args:
                first_name (str): first name of the student
                last_name (str): last name of the student
                other_name (str): any other name the student might have

        """

        cls.first_name = first_name
        cls.last_name = last_name
        cls.other_name = other_name

        new_student = database.Student(first_name=cls.first_name,
                                       last_name=cls.last_name,
                                       other_name=cls.other_name)
        if new_student is None:
            print("Failed to add new student")
        else:
            session.add(new_student)
            session.commit()
            print("Successfully added {} {} {}".format(new_student.first_name,
                                                       new_student.other_name,
                                                       new_student.last_name))

    @classmethod
    def remove(cls, student_id):

        """Remove a student from the register table

           Args:
               student_id (int): id of student to be removed
        """

        cls.student_id = student_id
        student_to_remove = session.query(database.Student).get(student_id)
        if student_to_remove is None:
            print("The student id specified was not found")
        else:
            session.delete(student_to_remove)
            session.commit()
            print("Successfully removed {} {} {}".format(student_to_remove.first_name,
                                                         student_to_remove.other_name,
                                                         student_to_remove.last_name))

    @classmethod
    def check_in(cls, student_id, class_id):

        """Check in a given student to a given class by updating the register table

           Args:
               student_id (int): id of the student
               class_id (int): id of the class
        """

        cls.student_id = student_id
        cls.class_id = class_id

        student_to_check = session.query(database.Student).get(cls.student_id)
        class_to_check = session.query(database.ClassTable).get(cls.class_id)
        if student_to_check is None or class_to_check is None:
            print("You entered a class id or student id that does not exist")
        elif student_to_check.class_id is not None:
            print("you cannot check in into this class")
        else:
            student_to_check.class_id = cls.class_id
            Register().update(cls.class_id, cls.student_id)
            print("Checked in '{} {}' in class '{}'".format(student_to_check.first_name,
                                                            student_to_check.last_name,
                                                            class_to_check.name))

    @classmethod
    def check_out(cls, student_id, class_id, reason):

        """Check out a given student from a given class and supply a reason

           Args:
               student_id (int): id of the student
               class_id (int): id of the class
               reason (str): reason for checking out
        """

        cls.student_id = student_id
        cls.class_id = class_id

        student_to_check_out = session.query(database.Register). \
            filter(database.Register.student_id == student_id,
                   database.Register.class_id == cls.class_id).all()[-1]
        class_to_check_out = session.query(database.ClassTable).get(cls.class_id)

        if student_to_check_out is None or class_to_check_out is None:
            print("The specified student or class was not found")
        elif not student_to_check_out.checked_in:
            print("The student specified is not checked in")
        else:
            student_to_check_out.checked_in = False
            student_to_check_out.reason = reason
            print("You have checked out '{}' from the '{}' class".format(student_to_check_out.student_id,
                                                                         class_to_check_out.name))
            session.commit()

    @property
    def view_all(self):

        """Return all students in the student table"""

        all_students = session.query(database.Student).all()
        return all_students
