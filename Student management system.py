import json
import tkinter as tk
from tkinter import messagebox

class Student:
    def __init__(self, name, roll_number, address="", phone_number="", division=""):
        self.name = name
        self.roll_number = roll_number
        self.address = address
        self.phone_number = phone_number
        self.division = division
        self.grades = []

    def add_grade(self, grade):
        self.grades.append(grade)

    def average_grade(self):
        if len(self.grades) == 0:
            return "No grades recorded"
        else:
            return sum(self.grades) / len(self.grades)

    def to_dict(self):
        return {
            'name': self.name,
            'roll_number': self.roll_number,
            'address': self.address,
            'phone_number': self.phone_number,
            'division': self.division,
            'grades': self.grades
        }

    @staticmethod
    def from_dict(data):
        student = Student(data['name'], data['roll_number'], data['address'], data['phone_number'], data['division'])
        student.grades = data['grades']
        return student


class StudentManagementSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")

        self.students = []

        # Load data if available
        try:
            self.load_data("students.json")
        except FileNotFoundError:
            messagebox.showinfo("Info", "No existing data found.")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.main_frame, text="Add Student", command=self.add_student_window).pack(fill=tk.X, padx=10, pady=5)
        tk.Button(self.main_frame, text="Remove Student", command=self.remove_student_window).pack(fill=tk.X, padx=10, pady=5)
        tk.Button(self.main_frame, text="Add Grade", command=self.add_grade_window).pack(fill=tk.X, padx=10, pady=5)
        tk.Button(self.main_frame, text="Edit Division", command=self.edit_division_window).pack(fill=tk.X, padx=10, pady=5)
        tk.Button(self.main_frame, text="Display Students", command=self.display_students_window).pack(fill=tk.X, padx=10, pady=5)

    def add_student_window(self):
        add_student_window = tk.Toplevel(self.root)
        add_student_window.title("Add Student")

        tk.Label(add_student_window, text="Name:").pack()
        name_entry = tk.Entry(add_student_window)
        name_entry.pack()

        tk.Label(add_student_window, text="Roll Number:").pack()
        roll_number_entry = tk.Entry(add_student_window)
        roll_number_entry.pack()

        tk.Label(add_student_window, text="Address:").pack()
        address_entry = tk.Entry(add_student_window)
        address_entry.pack()

        tk.Label(add_student_window, text="Phone Number:").pack()
        phone_number_entry = tk.Entry(add_student_window)
        phone_number_entry.pack()

        tk.Label(add_student_window, text="Division:").pack()
        division_entry = tk.Entry(add_student_window)
        division_entry.pack()

        def add_student():
            name = name_entry.get()
            roll_number = roll_number_entry.get()
            address = address_entry.get()
            phone_number = phone_number_entry.get()
            division = division_entry.get()
            student = Student(name, roll_number, address, phone_number, division)
            self.students.append(student)
            messagebox.showinfo("Info", "Student added successfully.")
            add_student_window.destroy()

        tk.Button(add_student_window, text="Add", command=add_student).pack()

    def remove_student_window(self):
        remove_student_window = tk.Toplevel(self.root)
        remove_student_window.title("Remove Student")

        tk.Label(remove_student_window, text="Roll Number:").pack()
        roll_number_entry = tk.Entry(remove_student_window)
        roll_number_entry.pack()

        def remove_student():
            roll_number = roll_number_entry.get()
            for student in self.students:
                if student.roll_number == roll_number:
                    self.students.remove(student)
                    messagebox.showinfo("Info", "Student removed successfully.")
                    remove_student_window.destroy()
                    return
            messagebox.showinfo("Info", "Student not found.")

        tk.Button(remove_student_window, text="Remove", command=remove_student).pack()

    def add_grade_window(self):
        add_grade_window = tk.Toplevel(self.root)
        add_grade_window.title("Add Grade")

        tk.Label(add_grade_window, text="Roll Number:").pack()
        roll_number_entry = tk.Entry(add_grade_window)
        roll_number_entry.pack()

        tk.Label(add_grade_window, text="Grade:").pack()
        grade_entry = tk.Entry(add_grade_window)
        grade_entry.pack()

        def add_grade():
            roll_number = roll_number_entry.get()
            grade = float(grade_entry.get())
            for student in self.students:
                if student.roll_number == roll_number:
                    student.add_grade(grade)
                    messagebox.showinfo("Info", "Grade added successfully.")
                    add_grade_window.destroy()
                    return
            messagebox.showinfo("Info", "Student not found.")

        tk.Button(add_grade_window, text="Add", command=add_grade).pack()

    def edit_division_window(self):
        edit_division_window = tk.Toplevel(self.root)
        edit_division_window.title("Edit Division")

        tk.Label(edit_division_window, text="Roll Number:").pack()
        roll_number_entry = tk.Entry(edit_division_window)
        roll_number_entry.pack()

        tk.Label(edit_division_window, text="New Division:").pack()
        new_division_entry = tk.Entry(edit_division_window)
        new_division_entry.pack()

        def edit_division():
            roll_number = roll_number_entry.get()
            new_division = new_division_entry.get()
            for student in self.students:
                if student.roll_number == roll_number:
                    student.division = new_division
                    messagebox.showinfo("Info", "Division edited successfully.")
                    edit_division_window.destroy()
                    return
            messagebox.showinfo("Info", "Student not found.")

        tk.Button(edit_division_window, text="Edit", command=edit_division).pack()

    def display_students_window(self):
        display_students_window = tk.Toplevel(self.root)
        display_students_window.title("Display Students")

        if not self.students:
            tk.Label(display_students_window, text="No students in the system.").pack()
        else:
            for student in self.students:
                tk.Label(display_students_window, text=f"Name: {student.name}, Roll Number: {student.roll_number}, "
                                                        f"Address: {student.address}, "
                                                        f"Phone Number: {student.phone_number}, "
                                                        f"Division: {student.division}, "
                                                        f"Average Grade: {student.average_grade()}").pack()


    def save_data(self, filename):
        with open(filename, 'w') as file:
            data = [student.to_dict() for student in self.students]
            json.dump(data, file)

    def load_data(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            self.students = [Student.from_dict(student_data) for student_data in data]


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystemGUI(root)
    root.mainloop()


