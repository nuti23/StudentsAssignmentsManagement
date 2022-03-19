from Domain.student import Student
from Repository.student_repository import StudentRepository


class StudentRepositoryTextFile(StudentRepository):
    """
    Here is the StudentRepositoryTextFile class.
    """
    def __init__(self, file_name="student.txt"):
        """
        This is the constructor of StudentRepositoryTextFile class.
        :param file_name: the name of the file we're working with
        """
        super().__init__()
        self._file_name = file_name
        self._load()

    def add_student(self, student):
        """
        Here we use the functionalities from StudentRepository class to add a student in the file and also in memory.
        We also save the change.
        :param student: the student that will be added, Student() type
        """
        super().add_student(student)
        self._save()

    def remove(self, filter_function):
        """
        Here we use the functionalities from StudentRepository class to remove a student by its id from the file and
        also from memory.
        We also save the change.
        :param filter_function: a general remove function, we use remove by id
        """
        super().remove(filter_function)
        self._save()

    def update(self, student_id, name, group):
        """
        Here we use the functionalities from StudentRepository class to update an existent student in the file and
        also in memory.
        We also save the change.
        :param student_id: an integer representing the id of an existent student which we'll be updated
        :param name: a string representing the new name
        :param group: an integer representing the new group
        """
        super().update(student_id, name, group)
        self._save()

    def _load(self):
        """
        Here we read the txt file and we add the student.
        """
        file = open(self._file_name, 'rt')
        lines = file.readlines()
        file.close()

        for line in lines:
            line = line.split(";")
            super().add_student(Student(int(line[0]), line[1], int(line[2])))

    def _save(self):
        """
        Here we write the students from our students_list.
        """
        file = open(self._file_name, 'wt')
        for student in self.get_students_list():
            line = str(student.student_id) + ";" + student.name + ";" + str(student.group)
            file.write(line)
            file.write("\n")
        file.close()



