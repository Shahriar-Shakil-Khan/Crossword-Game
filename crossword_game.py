import tkinter as tk
from tkinter import messagebox

class SimpleCrossword:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Crossword Puzzle")
        self.current_level = 0

        self.levels = [
            {
                'solution': [
                    ['C', 'A', 'T', '', 'D'],
                    ['', '', 'H', '', 'O'],
                    ['', '', 'I', '', 'G'],
                    ['', 'O', 'N', 'E', ''],
                    ['', '', '', '', '']
                ],
                'clues': {
                    "Across": {
                        1: "A pet (3 letters)",
                        4: "A number (3 letters)"
                    },
                    "Down": {
                        1: "A word describing a slim person(3 letters)",
                        2: "Man's best friend (3 letters)"
                    }
                },
                'prefilled': {
                    (0, 0): 'C',
                    (3, 1): 'O'
                }
            },
            {
                'solution': [
                    ['M', 'A', 'N', 'G', 'O',],
                    ['A', '', '', '', 'N'],
                    ['S', '', 'A', '', 'I'],
                    ['S', 'I', 'T', '', 'O'],
                    ['', '', '', 'O', 'N']
                ],
                'clues': {
                    "Across": {
                        1: "a fruit (5 letters)",
                        2: " No, ___ down!(3 letters)",
                        3: "Opposite of 'off' (2 letters)"
                    },
                    "Down": {
                        1: "Newton's laws deal with this property of objects. (4 letters)",
                        2: "Preposition used to indicate a specific location or time (2 letters)",
                        3: "A bulb vegetable (5 letters)"
                    }
                },
                'prefilled': {
                    (0, 0): 'M',
                    (2, 0): 'S',
                    (3, 2): 'T',
                }
            }
        ]
        self.user_answers = [["" for _ in range(5)] for _ in range(5)]

        self.create_widgets()

    def create_widgets(self):
        self.clear_grid()

        level_label = tk.Label(self.root, text=f"Level {self.current_level + 1}", font=("Arial", 14, "bold"))
        level_label.grid(row=0, column=0, columnspan=5, pady=10)

        clues_frame = tk.Frame(self.root)
        clues_frame.grid(row=1, column=6, rowspan=5, sticky="nw", padx=20)

        tk.Label(clues_frame, text="ACROSS", font=("Arial", 12, "bold")).pack(anchor="w")
        for num, clue in self.levels[self.current_level]['clues']["Across"].items():
            tk.Label(clues_frame, text=f"{num}. {clue}", wraplength=220, justify="left").pack(anchor="w")

        tk.Label(clues_frame, text="\nDOWN", font=("Arial", 12, "bold")).pack(anchor="w")
        for num, clue in self.levels[self.current_level]['clues']["Down"].items():
            tk.Label(clues_frame, text=f"{num}. {clue}", wraplength=220, justify="left").pack(anchor="w")

        self.display_grid()

        button_frame = tk.Frame(self.root)
        button_frame.grid(row=7, column=0, columnspan=5, pady=10)

        tk.Button(button_frame, text="Check Answers", command=self.check_answers, font=("Arial", 12), bg="lightblue").pack(side="left", padx=10)

        self.switch_level_button = tk.Button(button_frame, text="Switch Level", command=self.switch_level, font=("Arial", 12), bg="lightgreen", state="disabled")
        self.switch_level_button.pack(side="left", padx=10)

    def display_grid(self):
        solution = self.levels[self.current_level]['solution']
        prefilled = self.levels[self.current_level].get('prefilled', {})
        self.cells = []

        for i in range(5):
            row = []
            for j in range(5):
                if solution[i][j] != "":
                    entry = tk.Entry(
                        self.root,
                        width=4,
                        font=("Arial", 14),
                        justify="center",
                        relief="solid",
                        validate="key",
                        validatecommand=(self.root.register(self.validate_input), '%P')
                    )
                    entry.grid(row=i+2, column=j)

                    if (i, j) in prefilled:
                        entry.insert(0, prefilled[(i, j)])
                        entry.config(state="disabled", disabledbackground="lightgray", disabledforeground="black")
                    else:
                        entry.bind("<KeyRelease>", lambda e, i=i, j=j: self.convert_to_uppercase(i, j))
                        entry.bind("<FocusOut>", lambda e, i=i, j=j: self.update_answer(i, j))

                    row.append(entry)
                else:
                    row.append(None)
            self.cells.append(row)

    def clear_grid(self):
        for widget in self.root.winfo_children():
            widget.grid_forget()

    def validate_input(self, new_value):

        if len(new_value) > 1:
            return False
        if new_value and not new_value.isalpha():
            return False
        return True

    def convert_to_uppercase(self, row, col):

        if self.cells[row][col]['state'] != 'disabled':
            current_value = self.cells[row][col].get()
            if len(current_value) > 1:

                current_value = current_value[0]
            self.cells[row][col].delete(0, tk.END)
            self.cells[row][col].insert(0, current_value.upper())

    def update_answer(self, row, col):

        if self.cells[row][col] and self.cells[row][col]['state'] != 'disabled':
            self.user_answers[row][col] = self.cells[row][col].get().upper()

    def check_answers(self):
        all_correct = True
        solution = self.levels[self.current_level]['solution']
        prefilled = self.levels[self.current_level].get('prefilled', {})

        for i in range(5):
            for j in range(5):
                if solution[i][j] != "":
                    if (i, j) in prefilled:
                        continue
                    user_input = self.cells[i][j].get().upper()
                    if user_input != solution[i][j]:
                        all_correct = False

        if all_correct:
            messagebox.showinfo("Well done!", "All answers are correct!")
            self.switch_level_button.config(state="normal")
        else:
            messagebox.showwarning("Try Again", "Some answers were incorrect.")


        for i in range(5):
            for j in range(5):
                if self.cells[i][j] and (i, j) not in prefilled:
                    self.cells[i][j].delete(0, tk.END)
                    self.user_answers[i][j] = ""

    def switch_level(self):
        if self.current_level < len(self.levels) - 1:
            self.current_level += 1
            self.user_answers = [["" for _ in range(5)] for _ in range(5)]
            self.create_widgets()
        else:
            messagebox.showinfo("Completed", "You've finished all levels!")

if __name__ == "__main__":
    root = tk.Tk()
    game = SimpleCrossword(root)
    root.mainloop()