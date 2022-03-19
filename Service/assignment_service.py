import datetime

from Domain.assignment import Assignment
from Undo.undo_service import FunctionCall, Operation, CascadedOperation


class AssignmentService:
    """
        This is AssignmentService class. Here we perform specific functionalities and validate the input.
        We raise value errors if something is wrong.
    """
    def __init__(self, assignment_repository, assignment_validator, grade_service, undo_service):
        """
        This is the constructor for AssignmentService class. Here we have the assignment repository and assignment
        validators.
        :param assignment_repository: it is a AssignmentRepository type where we have the list of assignments and
            some functionalities (add, remove)
        :param assignment_validator: it is a AssignmentValidator type where are methods responsible with validation
        :param grade_service: here we have all the methods from grade service
        :param undo_service: here we have all the methods from undo service
        """
        self.repository = assignment_repository
        self.validator = assignment_validator
        self.grade_service = grade_service
        self.undo_service = undo_service
        
    def create_assignment(self, assignment_id, description, deadline):
        """
        Here we 'create' and validate the new assignment.
        :param assignment_id: natural number representing the unique code of an Assignment
        :param description: string representing the task of an Assignment
        :param deadline: date type representing the last date to push an Assignment
        """

        new_assignment = Assignment(assignment_id, description, deadline)
        self.validator.validate(new_assignment)
        self.repository.add_assignment(new_assignment)

        undo = FunctionCall(self.remove_assignment_function, assignment_id)
        redo = FunctionCall(self.repository.add_assignment, new_assignment)
        operation = Operation(undo, redo)
        self.undo_service.record(operation)

    def remove_assignment_function(self, assignment_id):
        """
        Here we remove a assignment by its id.
        :param assignment_id: natural number representing the unique code of an assignment
        """

        ASSIGNMENT = self.repository.find_by_id(assignment_id)
        self.repository.remove(lambda assignment: not assignment.assignment_id == assignment_id)
        return ASSIGNMENT

    def remove_assignment(self, assignment_id):
        """
        Here we remove a assignment by its id and we create an operation with undo and redo functions.
        :param assignment_id: natural number representing the unique code of an assignment
        We also make an operation, so that we can undo and redo.
        When we remove an assignment, we remove its grades as well
        """
        ASSIGNMENT = self.remove_assignment_function(assignment_id)

        undo = FunctionCall(self.repository.add_assignment, ASSIGNMENT)
        redo = FunctionCall(self.remove_assignment_function, assignment_id)
        operation = Operation(undo, redo)

        grades = self.grade_service.filter_grades_by_assignment_id(assignment_id)
        for grade in grades:
            self.grade_service.remove_grade_function(grade.student_id, grade.assignment_id)

        cascade_list = [operation]
        for grade in grades:
            undo = FunctionCall(self.grade_service.create_grade, grade.student_id, grade.assignment_id,
                                grade.grade_value)
            redo = FunctionCall(self.grade_service.remove_grade_function, grade.student_id, grade.assignment_id)
            cascade_list.append(Operation(undo, redo))

        cascade_operations = CascadedOperation(*cascade_list)
        self.undo_service.record(cascade_operations)

    def update(self, assignment_id, description, deadline):
        """
        Here we update an assignment by its id.
        :param assignment_id: natural number representing the unique code of an assignment
        :param description: string, representing the new description of an assignment
        :param deadline: date type, representing the last date of an assignment
        """

        assignment, old_description, old_deadline = self.repository.update(assignment_id, description, deadline)
        self.validator.validate(assignment)
        undo = FunctionCall(self.repository.un_update, assignment_id, old_description,
                            old_deadline)
        redo = FunctionCall(self.repository.update, assignment.assignment_id, assignment.description,
                            assignment.deadline)
        operation = Operation(undo, redo)
        self.undo_service.record(operation)

    def get_assignment_list(self):
        """
        Here we pass the assignments list from repository to service, so that we can display the assignments in Ui later
        :return: assignment repository
        """
        return self.repository.get_assignment_list()

    def init_assignments(self):
        self.repository.add_assignment(Assignment(1, 'Compute 1+1.', datetime.datetime(2099, 2, 4)))
        self.repository.add_assignment(Assignment(2, 'Compute 1+2.', datetime.datetime(2022, 2, 4)))
        self.repository.add_assignment(Assignment(3, 'Compute 1+3.', datetime.datetime(2999, 2, 4)))
        self.repository.add_assignment(Assignment(4, 'Compute 1+4.', datetime.datetime(2024, 2, 4)))
        self.repository.add_assignment(Assignment(5, 'Compute 1+5.', datetime.datetime(2025, 2, 4)))
        self.repository.add_assignment(Assignment(6, 'Write a letter to your mom.', datetime.datetime(2025, 2, 4)))
        self.repository.add_assignment(Assignment(7, 'Write a letter to your dad.', datetime.datetime(2020, 12, 12)))
        self.repository.add_assignment(Assignment(8, 'Write a letter to your younger self.',
                                                   datetime.datetime(2021, 1, 3)))
        self.repository.add_assignment(Assignment(9, 'Write a letter to Santa Claus.', datetime.datetime(2099, 7, 14)))
        self.repository.add_assignment(Assignment(10, 'Write a letter to your grandma.',
                                                   datetime.datetime(1995, 10, 4)))

