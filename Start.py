from Domain.student import Student
from Repository.assignment_repository import AssignmentRepository
from Repository.grade_repository import GradeRepository
from Repository.student_repository import StudentRepository
from Repository_Binary_File.assignment_repository_binary_file import AssignmentRepositoryBinaryFile
from Repository_Binary_File.grade_repository_binary_file import GradeRepositoryBinaryFile
from Repository_Binary_File.student_repository_binary_file import StudentRepositoryBinaryFile
from Repository_TextFile.assignment_repository_text_file import AssignmentRepositoryTextFile
from Repository_TextFile.grade_repository_text_file import GradeRepositoryTextFile
from Repository_TextFile.student_repository_text_file import StudentRepositoryTextFile
from Service.assignment_service import AssignmentService
from Service.grade_service import GradeService
from Service.settings_properties import SettingsProperties

from Service.student_service import StudentService
from Ui.console import Ui
from Undo.undo_service import UndoRedoService
from Validators.assignment_validator import AssignmentValidator
from Validators.grade_validator import GradeValidator
from Validators.student_validator import StudentValidator

settings_properties = SettingsProperties()
dictionary = settings_properties.settings_data

if dictionary["repository"] == "inmemory":
    student_repository = StudentRepository()
    assignment_repository = AssignmentRepository()
    grade_repository = GradeRepository()
elif dictionary["repository"] == "textfiles":
    student_repository = StudentRepositoryTextFile(dictionary['student'])
    assignment_repository = AssignmentRepositoryTextFile(dictionary['assignment'])
    grade_repository = GradeRepositoryTextFile(dictionary['grade'])
elif dictionary["repository"] == "binaryfiles":
    student_repository = StudentRepositoryBinaryFile(dictionary['student'])
    assignment_repository = AssignmentRepositoryBinaryFile(dictionary['assignment'])
    grade_repository = GradeRepositoryBinaryFile(dictionary['grade'])


undo_redo_service = UndoRedoService()

grade_validator = GradeValidator()
grade_service = GradeService(grade_repository, grade_validator, undo_redo_service)

student_validator = StudentValidator()
student_service = StudentService(student_repository, student_validator, grade_service, undo_redo_service)

assignment_validator = AssignmentValidator()
assignment_service = AssignmentService(assignment_repository, assignment_validator, grade_service, undo_redo_service)


ui = Ui(student_service, assignment_service, grade_service, undo_redo_service)
ui.start()



