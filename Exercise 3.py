import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os

class Student:
    def __init__(self, code, name, cw1, cw2, cw3, exam):
        self.code = code
        self.name = name
        self.cw1 = int(cw1)
        self.cw2 = int(cw2)
        self.cw3 = int(cw3)
        self.exam = int(exam)
    
    def total_coursework(self):
        return self.cw1 + self.cw2 + self.cw3
    
    def overall_percentage(self):
        return ((self.total_coursework() + self.exam) / 160) * 100
    
    def grade(self):
        perc = self.overall_percentage()
        if perc >= 70: return 'A'
        elif perc >= 60: return 'B'
        elif perc >= 50: return 'C'
        elif perc >= 40: return 'D'
        else: return 'F'
    
    def format_output(self):
        return f"""
{'='*60}
Student Name: {self.name}
Student Number: {self.code}
Total Coursework: {self.total_coursework()}/60
Exam Mark: {self.exam}/100
Overall Percentage: {self.overall_percentage():.2f}%
Grade: {self.grade()}
{'='*60}
"""

class StudentManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        self.filename = "studentMarks.txt"
        self.students = []
        self.load_data()
        
        self.create_widgets()
    
    def load_data(self):
        if not os.path.exists(self.filename):
            data = """10
1345,John Curry,8,15,7,45
2345,Sam Sturtivant,14,15,14,77
9876,Lee Scott,17,11,16,99
3724,Matt Thompson,19,11,15,81
1212,Ron Herrema,14,17,18,66
8439,Jake Hobbs,10,11,10,43
2344,Jo Hyde,6,15,10,55
9384,Gareth Southgate,5,6,8,33
8327,Alan Shearer,20,20,20,100
2983,Les Ferdinand,15,17,18,92"""
            with open(self.filename, 'w') as f:
                f.write(data)
        
        try:
            with open(self.filename, 'r') as f:
                lines = f.readlines()
                num_students = int(lines[0].strip())
                self.students = []
                for i in range(1, num_students + 1):
                    parts = lines[i].strip().split(',')
                    student = Student(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5])
                    self.students.append(student)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")
    
    def save_data(self):
        try:
            with open(self.filename, 'w') as f:
                f.write(f"{len(self.students)}\n")
                for s in self.students:
                    f.write(f"{s.code},{s.name},{s.cw1},{s.cw2},{s.cw3},{s.exam}\n")
            messagebox.showinfo("Success", "Data saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {e}")
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Student Manager", 
                              font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#333')
        title_label.pack(pady=20)
        
        # Top buttons frame
        top_button_frame = tk.Frame(self.root, bg='#f0f0f0')
        top_button_frame.pack(pady=10)
        
        btn_view_all = tk.Button(top_button_frame, text="View All Student Records",
                                command=self.view_all_records, font=('Arial', 11),
                                bg='#e0e0e0', relief='raised', width=22, height=2,
                                cursor='hand2', bd=2)
        btn_view_all.grid(row=0, column=0, padx=10)
        
        btn_highest = tk.Button(top_button_frame, text="Show Highest Score",
                               command=self.show_highest, font=('Arial', 11),
                               bg='#e0e0e0', relief='raised', width=22, height=2,
                               cursor='hand2', bd=2)
        btn_highest.grid(row=0, column=1, padx=10)
        
        btn_lowest = tk.Button(top_button_frame, text="Show Lowest Score",
                              command=self.show_lowest, font=('Arial', 11),
                              bg='#e0e0e0', relief='raised', width=22, height=2,
                              cursor='hand2', bd=2)
        btn_lowest.grid(row=0, column=2, padx=10)
        
        # Individual record section
        individual_frame = tk.Frame(self.root, bg='#f0f0f0')
        individual_frame.pack(pady=15)
        
        label_individual = tk.Label(individual_frame, text="View Individual Student Record:",
                                   font=('Arial', 12), bg='#f0f0f0')
        label_individual.grid(row=0, column=0, padx=10)
        
        self.student_combo = ttk.Combobox(individual_frame, width=30, font=('Arial', 10),
                                         state='readonly')
        self.update_combo()
        self.student_combo.grid(row=0, column=1, padx=10)
        
        btn_view_record = tk.Button(individual_frame, text="View Record",
                                   command=self.view_individual_record, font=('Arial', 11),
                                   bg='#e0e0e0', relief='raised', width=15, height=2,
                                   cursor='hand2', bd=2)
        btn_view_record.grid(row=0, column=2, padx=10)
        
        # Display area
        display_frame = tk.Frame(self.root, bg='#f0f0f0')
        display_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.display_text = scrolledtext.ScrolledText(display_frame, 
                                                      font=('Courier', 10),
                                                      bg='white', fg='black',
                                                      relief='sunken', bd=2,
                                                      wrap='word')
        self.display_text.pack(fill='both', expand=True)
        
        # Bottom buttons frame
        bottom_frame = tk.Frame(self.root, bg='#f0f0f0')
        bottom_frame.pack(pady=15)
        
        buttons_bottom = [
            ("Sort Records", self.sort_records),
            ("Add Student", self.add_student),
            ("Delete Student", self.delete_student),
            ("Update Student", self.update_student)
        ]
        
        for i, (text, cmd) in enumerate(buttons_bottom):
            btn = tk.Button(bottom_frame, text=text, command=cmd,
                          font=('Arial', 10), bg='#d0d0d0',
                          relief='raised', width=15, height=2,
                          cursor='hand2', bd=2)
            btn.grid(row=0, column=i, padx=8)
    
    def update_combo(self):
        student_list = [f"{s.name} ({s.code})" for s in self.students]
        self.student_combo['values'] = student_list
        if student_list:
            self.student_combo.current(0)
    
    def clear_display(self):
        self.display_text.delete(1.0, tk.END)
    
    def display_output(self, text):
        self.clear_display()
        self.display_text.insert(1.0, text)
    
    def view_all_records(self):
        if not self.students:
            self.display_output("No students found.")
            return
        
        output = "\n" + "="*60 + "\n"
        output += "ALL STUDENT RECORDS\n"
        output += "="*60 + "\n"
        
        total_perc = 0
        for s in self.students:
            output += s.format_output()
            total_perc += s.overall_percentage()
        
        avg_perc = total_perc / len(self.students)
        output += f"\n{'='*60}\n"
        output += f"Total Students: {len(self.students)}\n"
        output += f"Average Percentage: {avg_perc:.2f}%\n"
        output += f"{'='*60}\n"
        
        self.display_output(output)
    
    def view_individual_record(self):
        if not self.students:
            self.display_output("No students found.")
            return
        
        selected_idx = self.student_combo.current()
        if selected_idx >= 0:
            student = self.students[selected_idx]
            output = "\n--- INDIVIDUAL STUDENT RECORD ---\n"
            output += student.format_output()
            self.display_output(output)
    
    def show_highest(self):
        if not self.students:
            self.display_output("No students found.")
            return
        
        highest = max(self.students, key=lambda s: s.overall_percentage())
        output = "\n--- HIGHEST SCORING STUDENT ---\n"
        output += highest.format_output()
        self.display_output(output)
    
    def show_lowest(self):
        if not self.students:
            self.display_output("No students found.")
            return
        
        lowest = min(self.students, key=lambda s: s.overall_percentage())
        output = "\n--- LOWEST SCORING STUDENT ---\n"
        output += lowest.format_output()
        self.display_output(output)
    
    def sort_records(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Sort Options")
        dialog.geometry("300x180")
        dialog.configure(bg='#f0f0f0')
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Choose Sort Order:", font=('Arial', 12, 'bold'),
                bg='#f0f0f0').pack(pady=20)
        
        def sort_asc():
            self.students.sort(key=lambda s: s.overall_percentage())
            self.update_combo()
            self.view_all_records()
            dialog.destroy()
        
        def sort_desc():
            self.students.sort(key=lambda s: s.overall_percentage(), reverse=True)
            self.update_combo()
            self.view_all_records()
            dialog.destroy()
        
        tk.Button(dialog, text="Ascending Order", command=sort_asc,
                 font=('Arial', 10), bg='#e0e0e0', width=18, height=2,
                 relief='raised', bd=2, cursor='hand2').pack(pady=5)
        tk.Button(dialog, text="Descending Order", command=sort_desc,
                 font=('Arial', 10), bg='#e0e0e0', width=18, height=2,
                 relief='raised', bd=2, cursor='hand2').pack(pady=5)
    
    def add_student(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Student")
        dialog.geometry("450x500")
        dialog.configure(bg='#f0f0f0')
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Add New Student", font=('Arial', 14, 'bold'),
                bg='#f0f0f0').pack(pady=15)
        
        frame = tk.Frame(dialog, bg='#f0f0f0')
        frame.pack(pady=10, padx=20)
        
        fields = [
            ('Student Code (1000-9999):', 'code'),
            ('Student Name:', 'name'),
            ('Coursework 1 (0-20):', 'cw1'),
            ('Coursework 2 (0-20):', 'cw2'),
            ('Coursework 3 (0-20):', 'cw3'),
            ('Exam Mark (0-100):', 'exam')
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(frame, text=label, font=('Arial', 10), bg='#f0f0f0',
                    anchor='w').grid(row=i, column=0, sticky='w', pady=8)
            entry = tk.Entry(frame, font=('Arial', 10), width=25)
            entry.grid(row=i, column=1, pady=8, padx=10)
            entries[key] = entry
        
        def save_student():
            try:
                code = entries['code'].get().strip()
                if not (code.isdigit() and 1000 <= int(code) <= 9999):
                    messagebox.showerror("Error", "Invalid student code! Must be 1000-9999")
                    return
                
                if any(s.code == code for s in self.students):
                    messagebox.showerror("Error", "Student code already exists!")
                    return
                
                name = entries['name'].get().strip()
                if not name:
                    messagebox.showerror("Error", "Name cannot be empty!")
                    return
                
                cw1 = int(entries['cw1'].get())
                cw2 = int(entries['cw2'].get())
                cw3 = int(entries['cw3'].get())
                exam = int(entries['exam'].get())
                
                if not (0 <= cw1 <= 20 and 0 <= cw2 <= 20 and 0 <= cw3 <= 20):
                    messagebox.showerror("Error", "Coursework marks must be 0-20!")
                    return
                
                if not (0 <= exam <= 100):
                    messagebox.showerror("Error", "Exam mark must be 0-100!")
                    return
                
                student = Student(code, name, cw1, cw2, cw3, exam)
                self.students.append(student)
                self.save_data()
                self.update_combo()
                self.display_output(f"Student '{name}' added successfully!")
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for marks!")
        
        btn_frame = tk.Frame(dialog, bg='#f0f0f0')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Add Student", command=save_student,
                 font=('Arial', 11), bg='#4CAF50', fg='white',
                 width=15, height=2, relief='raised', bd=2,
                 cursor='hand2').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                 font=('Arial', 11), bg='#f44336', fg='white',
                 width=15, height=2, relief='raised', bd=2,
                 cursor='hand2').pack(side='left', padx=5)
    
    def delete_student(self):
        if not self.students:
            messagebox.showinfo("Info", "No students to delete.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Student")
        dialog.geometry("500x550")
        dialog.configure(bg='#f0f0f0')
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Select Student to Delete", font=('Arial', 14, 'bold'),
                bg='#f0f0f0').pack(pady=15)
        
        frame = tk.Frame(dialog, bg='#f0f0f0')
        frame.pack(pady=10, fill='both', expand=True, padx=20)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        
        listbox = tk.Listbox(frame, font=('Arial', 10), height=20,
                            yscrollcommand=scrollbar.set, selectmode='single')
        listbox.pack(fill='both', expand=True)
        scrollbar.config(command=listbox.yview)
        
        for s in self.students:
            listbox.insert('end', f"{s.name} ({s.code})")
        
        def delete():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a student to delete!")
                return
            
            student = self.students[selection[0]]
            if messagebox.askyesno("Confirm Delete", 
                                  f"Are you sure you want to delete:\n{student.name} ({student.code})?"):
                self.students.remove(student)
                self.save_data()
                self.update_combo()
                self.display_output(f"Student '{student.name}' deleted successfully!")
                dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg='#f0f0f0')
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="Delete", command=delete,
                 font=('Arial', 11), bg='#f44336', fg='white',
                 width=15, height=2, relief='raised', bd=2,
                 cursor='hand2').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                 font=('Arial', 11), bg='#9E9E9E', fg='white',
                 width=15, height=2, relief='raised', bd=2,
                 cursor='hand2').pack(side='left', padx=5)
    
    def update_student(self):
        if not self.students:
            messagebox.showinfo("Info", "No students to update.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Student")
        dialog.geometry("500x650")
        dialog.configure(bg='#f0f0f0')
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Update Student Record", font=('Arial', 14, 'bold'),
                bg='#f0f0f0').pack(pady=15)
        
        # Student selection
        select_frame = tk.Frame(dialog, bg='#f0f0f0')
        select_frame.pack(pady=10, fill='x', padx=20)
        
        tk.Label(select_frame, text="Select Student:", font=('Arial', 11, 'bold'),
                bg='#f0f0f0').pack(anchor='w')
        
        listbox_frame = tk.Frame(select_frame, bg='#f0f0f0')
        listbox_frame.pack(fill='x', pady=5)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')
        
        listbox = tk.Listbox(listbox_frame, font=('Arial', 10), height=8,
                            yscrollcommand=scrollbar.set, selectmode='single')
        listbox.pack(fill='both', expand=True)
        scrollbar.config(command=listbox.yview)
        
        for s in self.students:
            listbox.insert('end', f"{s.name} ({s.code})")
        
        # Update fields
        update_frame = tk.Frame(dialog, bg='#f0f0f0')
        update_frame.pack(pady=10, padx=20)
        
        tk.Label(update_frame, text="Select Field to Update:", font=('Arial', 11, 'bold'),
                bg='#f0f0f0').grid(row=0, column=0, columnspan=2, sticky='w', pady=5)
        
        update_var = tk.StringVar(value="name")
        
        fields = [
            ("Name", "name"),
            ("Coursework 1", "cw1"),
            ("Coursework 2", "cw2"),
            ("Coursework 3", "cw3"),
            ("Exam Mark", "exam")
        ]
        
        for i, (text, val) in enumerate(fields):
            tk.Radiobutton(update_frame, text=text, variable=update_var, value=val,
                          font=('Arial', 10), bg='#f0f0f0',
                          selectcolor='#e0e0e0').grid(row=i+1, column=0, sticky='w', pady=3)
        
        tk.Label(update_frame, text="New Value:", font=('Arial', 10, 'bold'),
                bg='#f0f0f0').grid(row=len(fields)+1, column=0, sticky='w', pady=(15, 5))
        
        new_value_entry = tk.Entry(update_frame, font=('Arial', 10), width=30)
        new_value_entry.grid(row=len(fields)+2, column=0, columnspan=2, pady=5)
        
        def update():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a student!")
                return
            
            student = self.students[selection[0]]
            field = update_var.get()
            new_value = new_value_entry.get().strip()
            
            if not new_value:
                messagebox.showerror("Error", "Please enter a new value!")
                return
            
            try:
                if field == "name":
                    student.name = new_value
                elif field == "cw1":
                    val = int(new_value)
                    if not (0 <= val <= 20):
                        raise ValueError("Coursework mark must be 0-20")
                    student.cw1 = val
                elif field == "cw2":
                    val = int(new_value)
                    if not (0 <= val <= 20):
                        raise ValueError("Coursework mark must be 0-20")
                    student.cw2 = val
                elif field == "cw3":
                    val = int(new_value)
                    if not (0 <= val <= 20):
                        raise ValueError("Coursework mark must be 0-20")
                    student.cw3 = val
                elif field == "exam":
                    val = int(new_value)
                    if not (0 <= val <= 100):
                        raise ValueError("Exam mark must be 0-100")
                    student.exam = val
                
                self.save_data()
                self.update_combo()
                self.display_output(f"Student '{student.name}' updated successfully!")
                dialog.destroy()
                
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
        
        btn_frame = tk.Frame(dialog, bg='#f0f0f0')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Update", command=update,
                 font=('Arial', 11), bg='#FF9800', fg='white',
                 width=15, height=2, relief='raised', bd=2,
                 cursor='hand2').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                 font=('Arial', 11), bg='#9E9E9E', fg='white',
                 width=15, height=2, relief='raised', bd=2,
                 cursor='hand2').pack(side='left', padx=5)

def main():
    root = tk.Tk()
    app = StudentManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()