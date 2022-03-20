
###  Student Lab Assignment
An application that manages student lab assignments for a discipline. The application stores:
- **Student**: `student_id`, `name`, `group`
- **Assignment**: `assignment_id`, `description`, `deadline`
- **Grade**: `assignment_id`, `student_id`, `grade_value`

The application allows the user to:
1. Manage students and assignments. The user can add, remove, update, and list both students and assignments. (CRUD)
2. Give assignments to a student or a group of students. In case an assignment is given to a group of students, every student in the group will receive it. In case there are students who were previously given that assignment, it will not be assigned again.
3. Grade student for a given assignment. When grading, the program allows the user to select the assignment that is graded, from the student’s list of ungraded assignments. A student’s grade for a given assignment cannot be changed. Deleting a student removes their assignments. Deleting an assignment also removes all grades at that assignment. (cascade)
4. Create statistics:
    - All students who received a given assignment, ordered by average grade for that assignment.
    - All students who are late in handing in at least one assignment. These are all the students who have an ungraded assignment for which the deadline has passed.
    - Students with the best school situation, sorted in descending order of the average grade received for all assignments.
5. Unlimited undo/redo functionality. Each step will undo/redo the previous operation performed by the user. Undo/redo operations must cascade and have a memory-efficient implementation (no superfluous list copying)
6. In settings.properties.txt file the user can specify the repository type and the corresponding names of the files; there are 3 types of repository
    6.1 simple Repository: inmemory
    6.2 Text File Repository: textfiles
    6.3 Bianry File Repository: binaryfiles
7. Unit test cases 
---
