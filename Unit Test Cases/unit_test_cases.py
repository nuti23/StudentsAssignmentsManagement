
import unittest
import datetime

from Domain.assignment import Assignment
from Domain.grade import Grade
from Domain.student import Student
from Repository.assignment_repository import AssignmentRepository, AssignmentRepositoryException
from Repository.grade_repository import GradeRepository, GradeRepositoryException
from Repository.student_repository import StudentRepository, StudentRepositoryException
from Service.assignment_service import AssignmentService
from Service.grade_service import GradeService
from Service.student_service import StudentService
from Statistics.statistics import StatisticsService
from Undo.undo_service import UndoRedoService, UndoRedoException
from Validators.assignment_validator import AssignmentValidator, AssignmentException
from Validators.grade_validator import GradeValidator, GradeException
from Validators.student_validator import StudentValidator, StudentException


class StudentTest(unittest.TestCase):
    def test_student(self):
        student = Student(1, "POPESCU", 914)
        self.assertEqual(student.student_id, 1)
        self.assertEqual(student.name, 'POPESCU')
        self.assertEqual(student.group, 914)

    def test_setter(self):
        student = Student(1, 'DUMA', 888)
        student.name = 'POP'
        student.group = 999
        self.assertEqual(student.name, 'POP')
        self.assertEqual(student.group, 999)


class StudentRepositoryTestCases(unittest.TestCase):

    def test_repository(self):
        students_list = [Student(15, "Izac McRonald", 3),
                         Student(16, "Milen McRonald", 55),
                         Student(17, "Serena Williams", 11)]
        repository = StudentRepository(students_list)
        length = len(repository.students_list)
        self.assertEqual(length, 3)
        return repository

    def test_add(self):
        students_list = []
        repository = StudentRepository(students_list)
        new_student = Student(1, 'Jack', 101)
        repository.add_student(new_student)
        length = len(students_list)
        self.assertEqual(length, 1)
        self.assertRaises(StudentRepositoryException, repository.add_student, new_student)

    def test_remove(self):
        repository = self.test_repository()
        repository.remove(lambda student: not student.name == "Izac McRonald")
        self.assertEqual(len(repository.students_list), 2)

    def test_find_by_id(self):
        repository = self.test_repository()
        student_id = 17
        student = repository.find_by_id(student_id)

        self.assertEqual(student.student_id, 17)
        self.assertEqual(student.name, "Serena Williams")
        self.assertEqual(student.group, 11)

        repository = self.test_repository()
        student_id = 19
        self.assertRaises(StudentRepositoryException, repository.find_by_id, student_id)

    def test_exception(self):
        exception = StudentRepositoryException("not good!")
        self.assertEqual(exception.message, "not good!")
        self.assertTrue(type(exception) == StudentRepositoryException)

    def test_get_students_list(self):
        value = True
        repository = self.test_repository()
        students_list = [Student(15, "Izac McRonald", 3),
                         Student(16, "Milen McRonald", 55),
                         Student(17, "Serena Williams", 11)]
        list = repository.get_students_list()
        for index in range(0, len(list)-1):
            if (students_list[index].student_id != list[index].student_id\
                    or students_list[index].name != list[index].name\
                    or students_list[index].group != list[index].group): value = False
        self.assertTrue(value)


class StudentValidatorTest(unittest.TestCase):
    def test_student_validator(self):

        student = Student(121, '', 18)
        student_validator = StudentValidator()
        self.assertRaises(StudentException, student_validator.validate, student)

        student = Student('', 'John', 18)
        student_validator = StudentValidator()
        self.assertRaises(StudentException, student_validator.validate, student)

        student = Student(121, 'John', '')
        student_validator = StudentValidator()
        self.assertRaises(StudentException, student_validator.validate, student)

        student = Student('ID', 'John', 18)
        student_validator = StudentValidator()
        self.assertRaises(StudentException, student_validator.validate, student)

        student = Student(3, 'John', '12')
        student_validator = StudentValidator()
        self.assertRaises(StudentException, student_validator.validate, student)

        student = Student(3, 33, 12)
        student_validator = StudentValidator()
        self.assertRaises(StudentException, student_validator.validate, student)


class ServiceTest(unittest.TestCase):
    def start_tests(self):
        undo_service = UndoRedoService()

        students_list = [Student(15, "Izac McRonald", 3),
                         Student(16, "Milen McRonald", 55),
                         Student(17, "Serena Williams", 11)]
        student_repository = StudentRepository(students_list)
        student_validator = StudentValidator()

        assignment_list = [Assignment(2, "Compute 1+1.", datetime.datetime(2020, 3, 4)),
                           Assignment(3, "Compute 1+2.", datetime.datetime(2020, 5, 4)),
                           Assignment(4, "Compute 100!.", datetime.datetime(2020, 3, 4))]
        assignment_repository = AssignmentRepository(assignment_list)
        assignment_validator = AssignmentValidator()

        grades_list = [Grade(15, 2, 0),
                       Grade(16, 14, 10),
                       Grade(17, 14, '')]
        grade_repository = GradeRepository(grades_list)
        grade_validator = GradeValidator()
        grade_service = GradeService(grade_repository, grade_validator, undo_service)

        student_service = StudentService(student_repository, student_validator, grade_service, undo_service)
        assignment_service = AssignmentService(assignment_repository, assignment_validator, grade_service, undo_service)

        return student_service, assignment_service, grade_service, undo_service

    def test_create_student(self):
        student_service, assignment_service, grade_service, undo_service = self.start_tests()
        student_service.create_student(5, 'IONEL', 111)
        students_list = student_service.get_students_list()
        self.assertEqual(len(students_list), 4)

    def test_remove_student(self):
        student_service, assignment_service, grade_service, undo_service = self.start_tests()
        student_service.remove_student(15)
        students_list = student_service.get_students_list()
        self.assertEqual(len(students_list), 2)

    def test_update_student(self):
        student_service, assignment_service, grade_service, undo_service = self.start_tests()
        student_service.update(15, 'MARIN', 222)
        students_list = student_service.get_students_list()
        self.assertEqual(students_list[0].name, 'MARIN')
        self.assertEqual(students_list[0].group, 222)

    def test_remove_assignment(self):
        student_service, assignment_service, grade_service, undo_service = self.start_tests()
        assignment_service.remove_assignment(2)
        assignment_list = assignment_service.get_assignment_list()
        self.assertEqual(len(assignment_list), 2)

    def test_update_assignment(self):
        pass
        # student_service, assignment_service, grade_service, undo_service = self.start_tests()
        # assignment_list = assignment_service.get_assignment_list()
        # assignment_service.update(3, "NO MORE HOMEWORK!", datetime.datetime(2020, 3, 4))
        # self.assertEqual(assignment_list[0].description, "NO MORE HOMEWORK!")
        # self.assertEqual(assignment_list[0].deadline, datetime.datetime(2020, 3, 4))

    def test_create_assignment(self):
        student_service, assignment_service, grade_service, undo_service = self.start_tests()
        assignment_service.create_assignment(5 , 'MIAU', datetime.datetime(2222,2,2))
        assignment_list = assignment_service.get_assignment_list()
        self.assertEqual(len(assignment_list), 4)

    def test_remove_grade(self):
        student_service, assignment_service, grade_service, undo_service = self.start_tests()
        grade_service.remove_grade(15, 2)
        grades_list = grade_service.get_grades_list()
        self.assertEqual(len(grades_list), 2)

    def test_give_a_mark(self):
        student_service, assignment_service, grade_service, undo_service = self.start_tests()
        grade_service.give_a_mark(15, 2, 9)
        grades_list = grade_service.get_grades_list()
        self.assertEqual(grades_list[0].grade_value, 9)
        self.assertRaises(ValueError, grade_service.give_a_mark, 15, 2, 9)

    def test_reset_a_mark(self):
        student_service, assignment_service, grade_service, undo_service = self.start_tests()
        grade_service.reset_a_mark(16, 14)
        grades_list = grade_service.get_grades_list()
        self.assertEqual(grades_list[0].grade_value, 0)

    def test_create_grade(self):
        student_service, assignment_service, grade_service, undo_service = self.start_tests()
        grade_service.create_grade(1, 55, 4)
        grades_list = grade_service.get_grades_list()
        self.assertEqual(len(grades_list), 4)


class StatisticsTest(unittest.TestCase):

    def start_tests(self):
        undo_service = UndoRedoService()

        students_list = [Student(15, "Izac McRonald", 3),
                         Student(16, "Milen McRonald", 55),
                         Student(17, "Serena Williams", 11)]
        student_repository = StudentRepository(students_list)
        student_validator = StudentValidator()

        assignment_list = [Assignment(2, "Compute 1+1.", datetime.datetime(2020, 3, 4)),
                           Assignment(3, "Compute 1+2.", datetime.datetime(2020, 5, 4)),
                           Assignment(4, "Compute 100!.", datetime.datetime(2020, 3, 4))]
        assignment_repository = AssignmentRepository(assignment_list)
        assignment_validator = AssignmentValidator()

        grades_list = [Grade(15, 2, 0),
                       Grade(16, 14, 10),
                       Grade(17, 14, 4),
                       Grade(15, 3, 10),
                       Grade(17, 3, 9)]
        grade_repository = GradeRepository(grades_list)
        grade_validator = GradeValidator()
        grade_service = GradeService(grade_repository, grade_validator, undo_service)

        student_service = StudentService(student_repository, student_validator, grade_service, undo_service)
        assignment_service = AssignmentService(assignment_repository, assignment_validator, grade_service, undo_service)

        return student_service, assignment_service, grade_service, undo_service

    def test_average_grade_statistics(self):
        student_service, assignment_service, grade_service, undo_service = self.start_tests()
        statistics_service = StatisticsService(grade_service, student_service, assignment_service)
        students_names_above_list, students_names_below_list = statistics_service.average_grade_statistic(3)
        self.assertEqual(len(students_names_above_list), 1)
        self.assertEqual(len(students_names_below_list), 1)

    def test_late_assignments_statistics(self):
        student_service, assignment_service, grade_service, undo_service = self.start_tests()
        statistics_service = StatisticsService(grade_service, student_service, assignment_service)
        students_names_list = statistics_service.late_assignments_statistics()
        self.assertEqual(len(students_names_list), 1)

    def test_names_and_final_grades_statistics(self):
        student_service, assignment_service, grade_service, undo_service = self.start_tests()
        statistics_service = StatisticsService(grade_service, student_service, assignment_service)
        names_and_final_grades_list = statistics_service.names_and_final_grades_statistics()
        self.assertEqual(len(names_and_final_grades_list), 3)


class AssignmentTest(unittest.TestCase):
    def test_assignment(self):
        assignment = Assignment(1, "Compute 1+1.", datetime.datetime(2020, 4, 5))
        self.assertEqual(assignment.assignment_id, 1)
        self.assertEqual(assignment._description, "Compute 1+1.")
        self.assertEqual(assignment._deadline, datetime.datetime(2020, 4, 5))

    def test_setter(self):
        assignment = Assignment(1, "Compute 1+1.", datetime.datetime(2020, 4, 5))
        assignment.description = "Compute 2+1."
        assignment.deadline = datetime.datetime(2020, 10, 5)
        self.assertEqual(assignment.description, "Compute 2+1.")
        self.assertEqual(assignment.deadline, datetime.datetime(2020, 10, 5))


class AssignmentRepositoryTestCase(unittest.TestCase):
    def test_repository(self):
        assignment_list = [Assignment(2, "Compute 1+1.", datetime.datetime(2020, 3, 4)),
                           Assignment(3, "Compute 1+2.", datetime.datetime(2020, 5, 4)),
                           Assignment(4, "Compute 100!.", datetime.datetime(2020, 3, 4))]
        repository = AssignmentRepository(assignment_list)
        self.assertEqual(len(repository.assignment_list), 3)
        return repository

    def test_add(self):
        repository = self.test_repository()
        repository.add_assignment(Assignment(5, "Compute 101!.", datetime.datetime(2020, 12, 4)))
        self.assertEqual(len(repository.assignment_list), 4)
        self.assertRaises(AssignmentRepositoryException, repository.add_assignment, Assignment(5, "Compute 101!.", datetime.datetime(2020, 12, 4)))

    def test_remove(self):
        repository = self.test_repository()
        repository.remove(lambda assignment: not assignment.deadline == datetime.datetime(2020, 3, 4))
        self.assertEqual(len(repository.assignment_list), 1)


    def test_get_students_list(self):
        value = True
        repository = self.test_repository()
        assignment_list = [Assignment(2, "Compute 1+1.", datetime.datetime(2020, 3, 4)),
                           Assignment(3, "Compute 1+2.", datetime.datetime(2020, 5, 4)),
                           Assignment(4, "Compute 100!.", datetime.datetime(2020, 3, 4))]
        list = repository.get_assignment_list()
        for index in range(0, len(list)-1):
            if (assignment_list[index].assignment_id != list[index].assignment_id\
                    or assignment_list[index]._description != list[index].description\
                    or assignment_list[index]._deadline != list[index].deadline): value = False
        self.assertTrue(value)

    def test_find_by_id(self):
        repository = self.test_repository()
        assignment_id = 2
        assignment = repository.find_by_id(assignment_id)

        self.assertEqual(assignment.assignment_id, 2)
        self.assertEqual(assignment.description, "Compute 1+1.")
        self.assertEqual(assignment.deadline, datetime.datetime(2020, 3, 4))

        self.assertRaises(AssignmentRepositoryException, repository.find_by_id, 10)


class AssignmentValidatorTest(unittest.TestCase):

    def test_assignment_validator(self):
        assignment = Assignment(23, '', datetime.datetime(2021, 5, 25))
        assignment_validator = AssignmentValidator()
        self.assertRaises(AssignmentException, assignment_validator.validate, assignment)

        assignment = Assignment('', 'Compute 5*8.', datetime.datetime(2021, 5, 25))
        assignment_validator = AssignmentValidator()
        self.assertRaises(AssignmentException, assignment_validator.validate, assignment)

        assignment = Assignment(23, 'Compute 5*8.', '')
        assignment_validator = AssignmentValidator()
        self.assertRaises(AssignmentException, assignment_validator.validate, assignment)

        assignment = Assignment('miau', 'Compute 5*8.', datetime.datetime(2021, 5, 25))
        assignment_validator = AssignmentValidator()
        self.assertRaises(AssignmentException, assignment_validator.validate, assignment)

        assignment = Assignment(23, 5, datetime.datetime(2021, 5, 25))
        assignment_validator = AssignmentValidator()
        self.assertRaises(AssignmentException, assignment_validator.validate, assignment)

        assignment = Assignment(23, 'Compute 5*8.', 5)
        assignment_validator = AssignmentValidator()
        self.assertRaises(AssignmentException, assignment_validator.validate, assignment)


class GradeTest(unittest.TestCase):
    def test_grade(self):
        grade = Grade(1, 5, 3)
        self.assertEqual(grade.student_id, 1)
        self.assertEqual(grade.assignment_id, 5)
        self.assertEqual(grade.grade_value, 3)

    def test_setter(self):
        grade = Grade(1, 2, 5)
        grade.grade_value = 10
        self.assertEqual(grade.grade_value, 10)


class GradeRepositoryTestCase(unittest.TestCase):
    def test_repository(self):
        grades_list = [Grade(15, 20, 3),
                       Grade(16, 14, 10),
                       Grade(17, 14, '')]
        repository = GradeRepository(grades_list)
        length = len(repository.grades_list)
        self.assertEqual(length, 3)
        return repository

    def test_add_grade_student(self):
        grades_list = []
        repository = GradeRepository(grades_list)
        new_grade = Grade(1, 1, 10)
        repository.add_grade_student(new_grade)
        self.assertEqual(len(grades_list), 1)

        self.assertRaises(GradeRepositoryException, repository.add_grade_student, new_grade)

    def test_remove(self):
        repository = self.test_repository()
        repository.remove(lambda grade: not grade.student_id == 15)
        grades_list = repository.get_grades_list_repository()
        self.assertEqual(len(grades_list), 2)

    def test_find_by_ids(self):
        repository = self.test_repository()
        grade = repository.find_by_ids(15, 20)

        self.assertEqual(grade.student_id, 15)
        self.assertEqual(grade.assignment_id, 20)
        self.assertRaises(GradeRepositoryException, repository.find_by_ids, 200, 222)


class GradeValidatorTest(unittest.TestCase):

    def test_grade_validator(self):

        grade = Grade('', 2, 9)
        grade_validator = GradeValidator()
        self.assertRaises(GradeException, grade_validator.validate, grade)

        grade = Grade(1, '', 9)
        grade_validator = GradeValidator()
        self.assertRaises(GradeException, grade_validator.validate, grade)

        grade = Grade(1, 2, '')
        grade_validator = GradeValidator()
        self.assertRaises(GradeException, grade_validator.validate, grade)

        grade = Grade('miau', 2, 9)
        grade_validator = GradeValidator()
        self.assertRaises(GradeException, grade_validator.validate, grade)

        grade = Grade(1, 'miau', 9)
        grade_validator = GradeValidator()
        self.assertRaises(GradeException, grade_validator.validate, grade)

        grade = Grade(1, 2, 'miau')
        grade_validator = GradeValidator()
        self.assertRaises(GradeException, grade_validator.validate, grade)

        grade = Grade(1, 2, 15)
        grade_validator = GradeValidator()
        self.assertRaises(GradeException, grade_validator.validate, grade)


class UndoTest(unittest.TestCase):

    def start_tests(self):
        undo_service = UndoRedoService()

        students_list = [Student(15, "Izac McRonald", 3),
                         Student(16, "Milen McRonald", 55),
                         Student(17, "Serena Williams", 11)]
        student_repository = StudentRepository(students_list)
        student_validator = StudentValidator()

        assignment_list = [Assignment(2, "Compute 1+1.", datetime.datetime(2020, 3, 4)),
                           Assignment(3, "Compute 1+2.", datetime.datetime(2020, 5, 4)),
                           Assignment(4, "Compute 100!.", datetime.datetime(2020, 3, 4))]
        assignment_repository = AssignmentRepository(assignment_list)
        assignment_validator = AssignmentValidator()

        grades_list = [Grade(15, 2, 0),
                       Grade(16, 3, 10),
                       Grade(17, 4, 4),
                       Grade(15, 3, 10),
                       Grade(17, 3, 9)]
        grade_repository = GradeRepository(grades_list)
        grade_validator = GradeValidator()
        grade_service = GradeService(grade_repository, grade_validator, undo_service)

        student_service = StudentService(student_repository, student_validator, grade_service, undo_service)
        assignment_service = AssignmentService(assignment_repository, assignment_validator, grade_service, undo_service)

        return student_service, assignment_service, grade_service, undo_service

    def test_undo(self):
        undo_redo_service = UndoRedoService()
        self.assertRaises(UndoRedoException, undo_redo_service.undo)
        self.assertRaises(UndoRedoException, undo_redo_service.redo)

    def test_student_undo(self):
        student_service, assignment_service, grade_service, undo_service = self.start_tests()
        student_service.remove_student(15)
        undo_service.undo()
        students_list = student_service.get_students_list()
        grades_list = grade_service.get_grades_list()
        self.assertEqual(len(students_list), 3)

        student_service.create_student(999, "pupu", 3)
        undo_service.undo()
        undo_service.redo()
        self.assertEqual(len(students_list), 4)
        self.assertEqual(len(grades_list), 5)


    def test_assignment_undo(self):
        student_service, assignment_service, grade_service, undo_service = self.start_tests()
        assignment_service.remove_assignment(3)
        assignments_list = assignment_service.get_assignment_list()
        grades_list = grade_service.get_grades_list()
        self.assertEqual(len(assignments_list), 2)
        self.assertEqual(len(grades_list), 2)

        undo_service.undo()
        self.assertEqual(len(assignments_list), 3)
        self.assertEqual(len(grades_list), 5)


        assignment_service.create_assignment(7474, "miauee", datetime.datetime(9999, 3, 2))
        undo_service.undo()
        undo_service.redo()

    def test_grade_undo(self):
        student_service, assignment_service, grade_service, undo_service = self.start_tests()
        grade_service.remove_grade(15, 2)
        undo_service.undo()
        undo_service.redo()




