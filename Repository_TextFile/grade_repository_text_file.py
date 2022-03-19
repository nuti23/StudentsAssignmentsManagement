
from Domain.grade import Grade
from Repository.grade_repository import GradeRepository


class GradeRepositoryTextFile(GradeRepository):
    """
    Here is the GradeRepositoryTextFile class.
    """
    def __init__(self, file_name="grade.txt"):
        """
        This is the constructor of GradeRepositoryTextFile class.
        :param file_name: the name of the file we're working with
        """
        super().__init__()
        self._file_name = file_name
        self._load()

    def add_grade_student(self, grade):
        """
        Here we use the functionalities from GradeRepository class to add a grade in the file and also in memory.
        We also save the change.
        :param grade: the grade that will be added, Grade() type
        """
        super().add_grade_student(grade)
        self._save()

    def remove(self, filter_function):
        """
        Here we use the functionalities from GradeRepository class to remove a grade by its id from the file and
        also from memory.
        We also save the change.
        :param filter_function: a general remove function, we use remove by ids
        """
        super().remove(filter_function)
        self._save()

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
        self._save()

    def _load(self):
        """
        Here we read the txt file and we add the grade.
        """
        file = open(self._file_name, 'rt')
        lines = file.readlines()
        file.close()

        for line in lines:
            line = line.split(";")
            super().add_grade_student(Grade(int(line[0]), int(line[1]), float(line[2])))

    def _save(self):
        """
        Here we write the garde from our grades_list.
        """
        file = open(self._file_name, 'wt')
        for grade in self.get_grades_list_repository():
            line = str(grade._student_id) + ";" + str(grade.assignment_id) + ";" + str(grade.grade_value)
            file.write(line)
            file.write("\n")
        file.close()



