import pickle

from Repository.student_repository import StudentRepository


class StudentRepositoryBinaryFile(StudentRepository):
    """
    Here is the StudentRepositoryBinaryFile class.
    """
    def __init__(self, file_name):
        """
        This is the constructor of StudentRepositoryBinaryFile class.
        :param file_name: the name of the file we're working with
        """
        super().__init__()
        self._file_name = file_name
        self._students_list = self._load()

    def add_student(self, student):
        """
        Here we use the functionalities from StudentRepository class to add a student in the file and also in memory.
        We also save the change.
        :param student: the student that will be added, Student() type
        """
        super().add_student(student)
        self._save(self._students_list)

    def remove(self, filter_function):
        """
        Here we use the functionalities from StudentRepository class to remove a student by its id from the file and
        also from memory.
        We also save the change.
        :param filter_function: a general remove function, we use remove by id
        """
        super().remove(filter_function)
        self._save(self._students_list)

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
        self._save(self._students_list)

    def _load(self):
        """
        Here we read the txt file and we add the student.
        We raise EOError or IOError if it is the case.
        """
        try:
            file = open(self._file_name, 'rb')
            lines = pickle.load(file)
            file.close()
            return lines
        except EOFError:
            return []
        except IOError as error:
            raise error

    def _save(self, students):
        """
        Here we write the students from our students_list.
        """
        file = open(self._file_name, "wb")
        pickle.dump(students, file)
        file.close()

