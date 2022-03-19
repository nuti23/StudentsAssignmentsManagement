from Domain.student import Student
from Undo.undo_service import FunctionCall, Operation, CascadedOperation


class StudentService:
    """
    This is StudentService class. Here we perform specific functionalities and validate the input.
    We raise value errors if something is wrong.
    """
    def __init__(self, student_repository, student_validator, grade_service, undo_service):
        """
        This is the constructor for StudentService class. Here we have the student repository and student validators.
        :param student_repository: it is a StudentRepository type where we have the list of students and
                some functionalities (add, remove)
        :param student_validator: it is a StudentValidator type where are methods responsible with validation
        :param grade_service: here we have all the methods from grade service
        :param undo_service: here we have all the methods from undo service
        """
        self.repository = student_repository
        self.validator = student_validator
        self.grade_service = grade_service
        self.undo_service = undo_service

    def create_student(self, student_id, name, group):
        """
        Here we 'create' and validate the new student.
        :param student_id: natural number representing the unique code of a Student
        :param name: string representing the name of a Student
        :param group: natural number representing the group of a Student
        """

        new_student = Student(student_id, name, group)
        self.validator.validate(new_student)
        self.repository.add_student(new_student)

        undo = FunctionCall(self.remove_student_function, student_id)
        redo = FunctionCall(self.repository.add_student, new_student)
        operation = Operation(undo, redo)
        self.undo_service.record(operation)

    def remove_student_function(self, student_id):
        """
        Here we remove a student by its id.
        :param student_id: natural number representing the unique code of a student
        """
        STUDENT = self.repository.find_by_id(student_id)
        self.repository.remove(lambda student: not student.student_id == student_id)
        return STUDENT

    def remove_student(self, student_id):
        """
        Here we remove a student by its id an we also create an operation with undo and redo functions.
        :param student_id: natural number representing the unique code of a student
        We also make an operation, so that we can undo and redo.
        When we remove a student, we remove its grades as well
        """
        STUDENT = self.remove_student_function(student_id)

        undo = FunctionCall(self.repository.add_student, STUDENT)
        redo = FunctionCall(self.remove_student_function, student_id)
        operation = Operation(undo, redo)

        grades = self.grade_service.filter_grades_by_student_id(STUDENT.student_id)
        for grade in grades:
            self.grade_service.remove_grade_function(grade.student_id, grade.assignment_id)

        cascade_list = [operation]
        for grade in grades:
            undo = FunctionCall(self.grade_service.create_grade, grade.student_id, grade.assignment_id, grade.grade_value)
            redo = FunctionCall(self.grade_service.remove_grade_function, grade.student_id, grade.assignment_id)
            cascade_list.append(Operation(undo, redo))

        cascade_operations = CascadedOperation(*cascade_list)
        self.undo_service.record(cascade_operations)

    def update(self, student_id, name, group):
        """
        Here we update a student by its id.
        :param group: new group for a student
        :param name: new name for a student
        :param student_id: natural number representing the unique code of a student
        """
        student, old_name, old_group = self.repository.update(student_id, name, group)
        self.validator.validate(student)

        undo = FunctionCall(self.repository.un_update, student_id, old_name,
                            old_group)
        redo = FunctionCall(self.repository.update, student.student_id, student.name,
                            student.group)
        operation = Operation(undo, redo)
        self.undo_service.record(operation)


    def get_students_list(self):
        """
        Here we pass the students list from repository to service, so that we can display the students in Ui later
        :return: students repository
        """
        return self.repository.get_students_list()

    def init_students(self):
        self.repository.add_student(Student(1, 'ANA', 122))
        self.repository.add_student(Student(2, 'IONEL', 123))
        self.repository.add_student(Student(3, 'MIRUNA', 12))
        self.repository.add_student(Student(4, 'PATRIK', 111))
        self.repository.add_student(Student(5, 'GEORGEL', 123))
        self.repository.add_student(Student(6, 'PATRICIA', 191))
        self.repository.add_student(Student(7, 'RAFAELO', 122))
        self.repository.add_student(Student(8, 'IRI', 123))
        self.repository.add_student(Student(9, 'MARIAN', 119))
        self.repository.add_student(Student(10, 'IRINA', 91))
