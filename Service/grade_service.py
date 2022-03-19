from Domain.grade import Grade
from Undo.undo_service import FunctionCall, Operation


class GradeService:
    """
    This is GradeService class. Here we perform specific functionalities and validate the input.
    We raise value errors if something is wrong.
    """
    def __init__(self, grade_repository, grade_validator, undo_service):
        """
        This is the constructor for GradeService class. Here we have the grade repository and grade validators.
        :param grade_repository: it is a GradeRepository type where we have the list of grades and
                some functionalities (add, remove)
        :param grade_validator: it is a GradeValidator type where are methods responsible with validation
        """
        self.repository = grade_repository
        self.validator = grade_validator
        self.undo_service = undo_service

    def create_grade(self, student_id, assignment_id, grade_value):
        """
        Here we 'create' and validate the new grade.
        :param student_id: natural number representing the unique code of a Student
        :param assignment_id: natural number representing the unique code of an Assignment
        :param grade_value: integer in [0,10], representing the mark of a student-assignment connection
        """

        new_grade = Grade(student_id, assignment_id, grade_value)
        self.validator.validate(new_grade)
        self.repository.add_grade_student(new_grade)

        undo = FunctionCall(self.remove_grade_function, student_id, assignment_id)
        redo = FunctionCall(self.repository.add_grade_student, new_grade)
        operation = Operation(undo, redo)
        self.undo_service.record(operation)

    def remove_grade_function(self, student_id, assignment_id):
        """
        Here we remove a grade by its student_id an by its assignment_id
        :param student_id: natural number representing the unique code of a Student
        :param assignment_id: natural number representing the unique code of an Assignment
        :return:
        """

        GRADE = self.repository.find_by_ids(student_id, assignment_id)
        self.repository.remove(lambda grade: not(grade.student_id == student_id and grade.assignment_id == assignment_id))
        return GRADE

    def remove_grade(self, student_id, assignment_id):
        """
        Here we remove a grade by its student and assignment id.
        :param student_id: natural number representing the unique code of a student
        :param assignment_id: natural number representing the unique code of an assignment
        """
        GRADE = self.remove_grade_function(student_id, assignment_id)

        undo = FunctionCall(self.repository.add_grade_student, GRADE)
        redo = FunctionCall(self.remove_grade_function, student_id, assignment_id)
        operation = Operation(undo, redo)
        self.undo_service.record(operation)

    def filter_grades_by_student_id(self, student_id):
        """
        Here we filter grades list by student_id.
        :param student_id: natural number representing the unique code of a student
        :return: filter grades list by student_id
        """
        return list(filter((lambda student: student.student_id == student_id), self.get_grades_list()))

    def filter_grades_by_assignment_id(self, assignment_id):
        """
        Here we filter grades list by assignment_id.
        :param assignment_id: natural number representing the unique code of an assignment
        :return: filter grades list by assignment_id
        """
        return list(filter((lambda assignment: assignment.assignment_id == assignment_id), self.get_grades_list()))

    def get_grades_list(self):
        """
        Here we pass the grades list from repository to service, so that we can display the grades in Ui later
        :return: grades repository
        """
        return self.repository.get_grades_list_repository()

    def give_a_mark(self, student_id, assignment_id, grade_value):
        """
        Here we give a mark to a student's assignment an we create an operation with undo and redo functions.
        :param student_id: the student's id which will be graded
        :param assignment_id: the assignment id which will be graded
        :param grade_value: the mark
        """

        grade = self.repository.give_a_mark(student_id, assignment_id, grade_value)
        self.validator.validate(grade)
        undo = FunctionCall(self.reset_a_mark, grade.student_id, grade.assignment_id)
        redo = FunctionCall(self.repository.give_a_mark, grade.student_id, grade.assignment_id, grade.grade_value)
        operation = Operation(undo, redo)
        self.undo_service.record(operation)

    def reset_a_mark(self, student_id, assignment_id):
        """
        Here we set the grade_value of a grade to 0.
        :param student_id: the student's id which will be ungraded
        :param assignment_id: the assignment id which will be ungraded
        :return:
        """
        grade = self.repository.find_by_ids(student_id, assignment_id)
        grade.grade_value = 0

    def init_grades(self):
        self.repository.add_grade_student(Grade(1, 1, 0))
        self.repository.add_grade_student(Grade(1, 2, 10))
        self.repository.add_grade_student(Grade(1, 3, 9))
        self.repository.add_grade_student(Grade(1, 6, 7))
        self.repository.add_grade_student(Grade(2, 10, 0))
        self.repository.add_grade_student(Grade(3, 10, 0))
        self.repository.add_grade_student(Grade(5, 10, 8))
        self.repository.add_grade_student(Grade(4, 7, 4))
        self.repository.add_grade_student(Grade(4, 2, 0))
        self.repository.add_grade_student(Grade(8, 10, 0))
        self.repository.add_grade_student(Grade(10, 10, 0))

