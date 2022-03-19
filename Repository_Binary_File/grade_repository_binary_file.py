import pickle

from Repository.grade_repository import GradeRepository


class GradeRepositoryBinaryFile(GradeRepository):
    """
    Here is the GradeRepositoryBinaryFile class.
    """
    def __init__(self, file_name):
        """
        This is the constructor of GradeRepositoryBinaryFile class.
        :param file_name: the name of the file we're working with
        """
        super().__init__()
        self._file_name = file_name
        self._grades_list = self._load()

    def add_grade_student(self, grade):
        """
        Here we use the functionalities from GradeRepository class to add a grade in the file and also in memory.
        We also save the change.
        :param grade: the grade that will be added, Grade() type
        """
        super().add_grade_student(grade)
        self._save(self._grades_list)

    def remove(self, filter_function):
        """
        Here we use the functionalities from GradeRepository class to remove a grade by its id from the file and
        also from memory.
        We also save the change.
        :param filter_function: a general remove function, we use remove by ids
        """
        super().remove(filter_function)
        self._save(self._grades_list)

    def give_a_mark(self, student_id, assignment_id, grade_value):
        """
        Here we use the functionalities from GradeRepository class to grade (give a mark to) a grade by its ids
        from the file and also from memory.
        We also save the change.
        :param student_id: an integer representing the id of an existent student which we'll be graded
        :param assignment_id: an integer representing the id of an existent assignment which we'll be graded
        :param grade_value: an integer representing the mark
        """
        super().give_a_mark(student_id, assignment_id, grade_value)
        self._save(self._grades_list)

    def _load(self):
        """
        Here we read the txt file and we add the grade.
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

    def _save(self, grades):
        """
        Here we write the garde from our grades_list.
        """
        file = open(self._file_name, "wb")
        pickle.dump(grades, file)
        file.close()

