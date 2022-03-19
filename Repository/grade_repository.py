

class GradeRepositoryException(Exception):
    """
    Here we create GradeRepository exceptions that may occur.
    """

    def __init__(self, message=''):
        self.message = message

    # def __str__(self):
    #     return self.message


class GradeRepository:
    """
    Here is GradeRepository class. Here we link students to their assignments.
    """
    def __init__(self, grades_list=None):
        """
        This constructor creates a list with all linked students-assignments.
        :param grades_list: the proper linked students-assignments list
        """

        self._grades_list = []
        if grades_list is not None:
            self._grades_list = grades_list

    @property
    def grades_list(self):
        return self._grades_list

    def add_grade_student(self, new_grade):
        """
        Here we add a new link between a student and an assignment.
        :param new_grade: the new link that will be added
        We also check if there isn't already a 'connection' between the given student and the given assignment
        """
        for grade in self._grades_list:
            if grade.student_id == new_grade.student_id and grade.assignment_id == new_grade.assignment_id:
                raise GradeRepositoryException("WARNING: the given student already has the assignment given!")
        self._grades_list.append(new_grade)

    def get_grades_list_repository(self):
        """
        Here we return the grades_list so that we can use it to display grades in UI module.
        :return: grades list
        """
        return self._grades_list

    def find_by_ids(self, student_id, assignment_id):
        """
        Here we are looking for a certain grade.
        :param student_id: student id
        :param assignment_id: assignment id
        :return: the grade with student id == student_id and assignment id == assignment_id
        """

        for grade in self._grades_list:
            if grade.student_id == student_id and grade.assignment_id == assignment_id:
                return grade
        raise GradeRepositoryException('INVALID student_id or assignment_id')

    def remove(self, filter_function):
        """
        This function removes a grade with a specific property given.
        :param filter_function: is the specific property given
                for example: remove by id, remove by name, remove by group
        """
        self._grades_list = list(filter(filter_function, self._grades_list))

    def give_a_mark(self, student_id, assignment_id, grade_value):
        grade = self.find_by_ids(student_id, assignment_id)
        if grade.grade_value == 0:
            grade.grade_value = grade_value
        else:
            raise ValueError("Already graded!")
        return grade


