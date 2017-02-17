# Class Attendance Register App

The class attendance register app provides a register which can be used to log attendance of students in various classes.

The App provides the following functionality:
* Add a student to the student database using `student add` 
* Remove a student using `student remove <student id>` 
* View all the students in the database using the `student list` 
* Add a class to the class database using `class add`
* View all the classes in the database using `class list`
* View all the students checked in to a certain class using `class_students <class_id>`
* Remove a class from the database using `class remove <class_id>`
* Check in a student to a class using `check in <student_id> <class_id>`
* Check out a student using from a class and provide a reason using `check out <student_id> <class_id> <reason>`
* Log the start and end of a class using `log start <class_id>` and `log end <class_id>`
* View register using `view register`
