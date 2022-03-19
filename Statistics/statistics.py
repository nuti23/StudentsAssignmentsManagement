from datetime import date, datetime


class StatisticsService:

    def __init__(self, grade_service, student_service, assignment_service):
        """
        Here is the constructor of StatisticsService class.
        :param grade_service: here we have all the functionalities from GradeService class
        :param student_service: here we have all the functionalities from StudentService class
        :param assignment_service: here we have all the functionalities from AssignmentService class
        """
        self.grade_service = grade_service
        self.student_service = student_service
        self.assignment_service = assignment_service

    def filter_by_assignment(self, assignment_id):
        """
        Here we filter grades_list such that in the end, we will have only grades of a given assignment, identified by
        its id (assignment_id).
        :param assignment_id: unique integer, representing the id of an assignment
        :return: grades list where all the grades are from a given assignment (assignment_id)
        """
        grades_list = self.grade_service.get_grades_list()
        return list(filter((lambda grade: grade.assignment_id == assignment_id), grades_list))

    def average_grade_of_an_assignment(self, assignment_id):
        """
        Here we compute the average grade of a given assignment, by its id
        :param assignment_id: unique integer, representing the id of an assignment
        :return: average grade of an assignment
        """
        grades_list = self.filter_by_assignment(assignment_id)
        sum_of_marks = float(0)
        for grade in grades_list:
            sum_of_marks = sum_of_marks + grade.grade_value
        length = len(grades_list)
        if length == 0:
            raise ValueError("this assignment isn't assigned yet!")
        average_grade = float(sum_of_marks/length)
        return average_grade

    def average_grade_statistic(self, assignment_id):
        """
        Here we construct students_names_above_list and students_names_below_list lists, where we will stock the names
        of the students that are above the average_grade and below the average_grade.
        :param assignment_id: unique integer, representing the id of an assignment
        :return: students_names_above_list and students_names_below_list lists (lists containing names of the students)
        """
        average_grade = self.average_grade_of_an_assignment(assignment_id)

        students_names_above_list = []
        students_names_below_list = []

        grades_list = self.filter_by_assignment(assignment_id)
        students_list = self.student_service.get_students_list()

        students_ids_above = []
        students_ids_below = []

        for grade in grades_list:
            if grade.grade_value < average_grade:
                students_ids_below.append(grade.student_id)
            else:
                students_ids_above.append(grade.student_id)

        for id in students_ids_above:
            for student in students_list:
                if student.student_id == id:
                    students_names_above_list.append(student.name)

        for id in students_ids_below:
            for student in students_list:
                if student.student_id == id:
                    students_names_below_list.append(student.name)
        return students_names_above_list, students_names_below_list

    def filter_by_grade_0(self):
        """
        Here we filter the grades_list, such that in the end, we will have only grades that are not evaluated yet
         (grade_value == 0)
        :return: a list where all the grades have grade_value == 0
        """
        grades_list = self.grade_service.get_grades_list()
        return list(filter((lambda grade: grade.grade_value == 0), grades_list))

    def late_assignments_statistics(self):
        """
        Here we construct a list, from grades_list where all grade_value == 0, in witch we'll put the names of the
        students that have at least one late assignment (grade_value == 0 and assignment.deadline < today's date)
        :return: a list in witch we'll put the names of the students that have at least one late assignment
        """
        students_ids_list = []
        students_names_list = []
        grades_list_0 = self.filter_by_grade_0()

        for grade in grades_list_0:
            assignment_id = grade.assignment_id
            for assignment in self.assignment_service.get_assignment_list():
                if assignment.assignment_id == assignment_id:
                    if assignment._deadline < datetime.today():
                        students_ids_list.append(grade.student_id)

        for id in students_ids_list:
            for student in self.student_service.get_students_list():
                if student.student_id == id:
                    students_names_list.append(student.name)
        return students_names_list

    def filter_grades_by_student_id(self, student_id):
        """
        Here we filter grades_list, such that in the end, will have a new list, in witch we'll have only grades of
        a given student (given by id)
        :param student_id:  unique integer, representing the id of a student
        :return: new list, in witch we'll have only grades of a given student
        """
        grades_list = self.grade_service.get_grades_list()
        return list(filter((lambda grade: grade.student_id == student_id), grades_list))

    def average_grade_of_a_student(self, student_id):
        """
        Here ve compute the average grade of a student (given by student_id)
        :param student_id: new list, in witch we'll have only grades a given student
        :return: average grade of a student, float type
        """
        grades_of_student_id_list = self.filter_grades_by_student_id(student_id)
        sum_of_marks = float(0)
        for grade in grades_of_student_id_list:
            sum_of_marks = sum_of_marks + grade.grade_value
        length = len(grades_of_student_id_list)

        if length == 0:
            return 0.0
        final_grade = float(sum_of_marks/length)
        return final_grade

    def all_students_final_grades_statistics(self):
        """
        Here we create a list where we have the student id on the fist position and the average grade on the
        second position of an element.
        [[[student.student_id1], [final_grade1]], [[student.student_id2], [final_grade2]], .....]
        :return: the list with student ids and its corresponding average grade
        """
        student_id_and_final_grade_list = []
        for student in self.student_service.get_students_list():
            final_grade = self.average_grade_of_a_student(student.student_id)
            student_id_and_final_grade_list.append([[student.student_id], [final_grade]])
        return student_id_and_final_grade_list

    def names_and_final_grades_statistics(self):
        """
        Here we create from student_id_and_final_grade_list list the names of the students.
        :return: list with  names of the students and its corresponding average grades
        """
        students_id_and_final_grade_list = self.all_students_final_grades_statistics()
        names_and_final_grades_list = []
        for position in students_id_and_final_grade_list:
            for student in self.student_service.get_students_list():
                if position[0] == [student.student_id]:
                    names_and_final_grades_list.append([[student.name], [position[1]]])
        return names_and_final_grades_list
