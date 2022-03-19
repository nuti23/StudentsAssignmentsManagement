import datetime

from Statistics.statistics import StatisticsService


def menu():
    print("[0] Exit")
    print("-------STUDENT OPERATIONS-----------")
    print("[1] Add a student")
    print("[2] Remove a student")
    print("[3] Update student")
    print('[4] Display students list')
    print("-------ASSIGNMENT OPERATIONS----------")
    print("[5] Add an assignment")
    print("[6] Remove an assignment")
    print("[7] Update an assignment")
    print('[8] Display assignments list')
    print("---------GRADE OPERATIONS-----------")
    print('[9] Give an assignment to a student')
    print('[10] Give an assignment to a group')
    print('[11] Display grades list')
    print("[12]: Grade an assignment")
    print("------------STATISTICS-------------")
    print('[13]: Students who received a given assignment, ordered by average grade')
    print("[14]: Students who have at least one late assignment")
    print("[15]: Ranking")
    print("------------UNDO/REDO-------------")
    print("[16]: UNDO")
    print("[17]: REDO")


class Ui:
    def __init__(self, student_service, assignment_service, grade_service, undo_service):
        """
        This is the main constructor. Here we bring all the information from our program.
        for example: student_service, assignment_service, grade_service
        :param student_service: it is represented by a StudentService class, where we have all the features for a student
        :param assignment_service: it is represented by a StudentService class, where we have all the features for a assignment
        :param grade_service: it is represented by a StudentService class, where we have all the features for a grade
        """
        self._student_service = student_service
        self._assignment_service = assignment_service
        self._grade_service = grade_service
        self.undo_service = undo_service

    def start(self):
        """
        Here we start our program. We collect information from the user (input) and we call the responsible functions.
        """

        command_dictionary = {"0": exit,
                              "1": self.add_student, "2": self.remove_student,
                              "3": self.update_student, '4': self.display_student_list,
                              '5': self.add_assignment, "6": self.remove_assignment,
                              "7": self.update_assignment, '8': self.display_assignment_list,
                              "9": self.give_assignment_student, '10': self.give_assignment_group,
                              "11": self.display_grades_list, "12": self.give_a_mark,
                              "13": self.statistic_average_grade, "14": self.statistic_late_assignment,
                              "15": self.statistic_best_school_situation,
                              '16': self.undo_service.undo, '17': self.undo_service.redo}

        #self._student_service.init_students()
        #self._assignment_service.init_assignments()
        #self._grade_service.init_grades()

        print("Welcome! Please pick an option.")
        while True:
            menu()
            print()
            command = input('Enter your option: ')

            if command in command_dictionary:
                try:
                    command_dictionary[command]()
                except Exception as ex:
                    print(ex)
            else:
                print("Invalid command!")
            print()

    def add_student(self):
        """
        Here we add a new student using the methods from StudentService.
        We raise error if id or group aren't valid.
        """
        student_id = input("ID: ")
        name = input("name: ")
        group = input("group: ")

        try:
            student_id = int(student_id)
            group = int(group)
        except:
            raise ValueError("id and group must be integers!")

        self._student_service.create_student(student_id, name, group)

    def remove_student(self):
        """
        Here we remove a student by its id, using the methods from StudentService.
        We raise error if id isn't valid.
        """
        student_id = input('ID: ')
        try:
            student_id = int(student_id)
        except:
            raise ValueError("id must be an integer")

        self._student_service.remove_student(student_id)

    def update_student(self):
        """
        Here we update a student by its id, using the methods from StudentService.
        """
        student_id = int(input("ID: "))
        print("trying to update student with id", student_id)
        name = input("new name: ")
        group = int(input("new group: "))
        self._student_service.update(student_id, name, group)

    def display_student_list(self):
        """
        Here we display the students list.
        """
        students_list = self._student_service.get_students_list()
        for student in students_list:
            print(student.student_id, "*", student.name, "*", student.group)
        print()

    def add_assignment(self):
        """
        Here we add a new student using the methods from AssignmentService.
        We raise error if the d, day, month or year given aren't valid.
        """
        assignment_id = input("ID: ")
        description = input("description: ")
        print("deadline...")
        day = input("deadline day: ")
        month = input("deadline month: ")
        year = input("deadline year: ")
        try:
            assignment_id = int(assignment_id)
            day = int(day)
            month = int(month)
            year = int(year)
        except:
            raise ValueError("id, day, month and year must be integers!")
        deadline = datetime.datetime(year, month, day)

        self._assignment_service.create_assignment(assignment_id, description, deadline)

    def remove_assignment(self):
        """
        Here we remove an assignment by its id, using the methods from AssignmentService.
        We raise error if the id given isn't valid.
        """
        assignment_id = input("ID: ")
        try:
            assignment_id = int(assignment_id)
        except:
            raise ValueError("id must be an integer")
        self._assignment_service.remove_assignment(assignment_id)
        #self._grade_service.remove_grade_when_remove_assignment(assignment_id)

    def update_assignment(self):
        """
        Here we update an assignment by its id, using the methods from AssignmentService.
        """
        assignment_id = int(input("ID: "))
        print("trying to update assignment with id", assignment_id)

        description = input("new description: ")
        print("new deadline... ")
        day = int(input("new day: "))
        month = int(input("new month: "))
        year = int(input("new year: "))
        deadline = datetime.datetime(year, month, day)
        self._assignment_service.update(assignment_id, description, deadline)

    def display_assignment_list(self):
        """
        Here we display the assignments list.
        """
        assignment_list = self._assignment_service.get_assignment_list()
        for assignment in assignment_list:
            print(assignment.assignment_id, '*', assignment.description, '*', assignment.deadline)
        print()

    def give_assignment_student(self):
        """
        Here we give an assignment to a student by its id.
        We raise error if the student_id or assignment_id given aren't available.
        """
        first_test = 0
        second_test = 0
        student_id = int(input("student ID: "))
        assignment_id = int(input("assignment ID: "))
        students_list = self._student_service.get_students_list()
        assignment_list = self._assignment_service.get_assignment_list()

        for student in students_list:
            if student.student_id == student_id:
                first_test = 1
        for assignment in assignment_list:
            if assignment.assignment_id == assignment_id:
                second_test = 1

        if first_test == 1 and second_test == 1:
            self._grade_service.create_grade(student_id, assignment_id, 0)
        else:
            raise ValueError('student_id or assignment_id unreachable!')

    def give_assignment_group(self):
        """
        Here we give an assignment to a group of students.
        We raise error if the group or assignment_id given aren't available.
        """
        first_test = 0
        second_test = 0
        group = int(input("group: "))
        assignment_id = int(input("assignment ID: "))
        students_list = self._student_service.get_students_list()
        assignment_list = self._assignment_service.get_assignment_list()

        for assignment in assignment_list:
            if assignment.assignment_id == assignment_id:
                first_test = 1

        for student in students_list:
            if student.group == group and first_test == 1:
               second_test = 1
               self._grade_service.create_grade(student.student_id, assignment_id, grade_value=0)

        if first_test == 0 or second_test == 0:
            raise ValueError('group or assignment_id unreachable!')

    def display_grades_list(self):
        """
        Here we display the grades list.
        """
        grades_list = self._grade_service.get_grades_list()
        for grade in grades_list:
            print(grade.student_id, '*', grade.assignment_id, '*', grade.grade_value)
        print()

    def display_student_assignments(self, student_id):
        """
        Here we display assignments of a given student by its id.
        :param student_id: given id
        """
        print("Choose assignment ID from: ")
        grades_list = self._grade_service.get_grades_list()
        for grade in grades_list:
            if grade.student_id == student_id and grade.grade_value == 0:
                print(grade.assignment_id)

    def give_a_mark(self):

        student_id = int(input("student ID: "))
        self.display_student_assignments(student_id)
        assignment_id = int(input("assignment ID: "))

        grade_value = int(input("grade: "))
        self._grade_service.give_a_mark(student_id, assignment_id, grade_value)
        print()

    def statistic_average_grade(self):
        assignment_id = int(input("assignment ID: "))
        statistics_service = StatisticsService(self._grade_service, self._student_service, self._assignment_service)

        above_average_names, below_average_names = statistics_service.average_grade_statistic(assignment_id)

        print("there are", len(above_average_names), "ABOVE AVERAGE students: ")
        for name in above_average_names:
            print(name)
        print("there are", len(below_average_names),"BELOW AVERAGE students: ")
        for name in below_average_names:
            print(name)

    def statistic_late_assignment(self):
        statistics_service = StatisticsService(self._grade_service, self._student_service, self._assignment_service)
        students_names_list = statistics_service.late_assignments_statistics()
        print("there are", len(students_names_list), "students with late assignments, namely:")
        for name in students_names_list:
            print(name)

    def statistic_best_school_situation(self):
        statistics_service = StatisticsService(self._grade_service, self._student_service, self._assignment_service)
        students_ranking = statistics_service.names_and_final_grades_statistics()
        students_ranking.sort(key=take_second, reverse=True)

        for student in students_ranking:
            print(student[0], student[1])


def take_second(element):
    return element[1]