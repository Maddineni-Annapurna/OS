import tkinter as tk
from tkinter import messagebox

class DeadlockGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔄 Deadlock Recovery Simulator")
        self.root.geometry("600x600")
        self.process_entries = []
        self.alloc_entries = []
        self.max_entries = []
        self.avail_entry = None

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Number of Processes:").pack()
        self.proc_count = tk.Entry(self.root)
        self.proc_count.pack()

        tk.Label(self.root, text="Number of Resources:").pack()
        self.res_count = tk.Entry(self.root)
        self.res_count.pack()

        tk.Button(self.root, text="Next", command=self.generate_matrices).pack(pady=10)

    def generate_matrices(self):
        try:
            self.n = int(self.proc_count.get())
            self.m = int(self.res_count.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid integers.")
            return

        for widget in self.root.winfo_children()[6:]:
            widget.destroy()

        tk.Label(self.root, text="Allocation Matrix:").pack()
        self.alloc_entries = []
        for i in range(self.n):
            row = tk.Entry(self.root)
            row.pack()
            self.alloc_entries.append(row)

        tk.Label(self.root, text="Maximum Matrix:").pack()
        self.max_entries = []
        for i in range(self.n):
            row = tk.Entry(self.root)
            row.pack()
            self.max_entries.append(row)

        tk.Label(self.root, text="Available Resources (space separated):").pack()
        self.avail_entry = tk.Entry(self.root)
        self.avail_entry.pack()

        tk.Button(self.root, text="Check Deadlock", command=self.deadlock_recovery).pack(pady=10)

        self.result_label = tk.Label(self.root, text="", justify="left")
        self.result_label.pack()

    def parse_matrix(self, entries):
        matrix = []
        for entry in entries:
            try:
                row = list(map(int, entry.get().strip().split()))
                if len(row) != self.m:
                    raise ValueError
                matrix.append(row)
            except:
                messagebox.showerror("Input Error", "Enter rows with correct number of integers.")
                return None
        return matrix

    def deadlock_recovery(self):
        alloc = self.parse_matrix(self.alloc_entries)
        maxm = self.parse_matrix(self.max_entries)
        try:
            avail = list(map(int, self.avail_entry.get().strip().split()))
        except:
            messagebox.showerror("Input Error", "Invalid available vector.")
            return

        if alloc is None or maxm is None or len(avail) != self.m:
            return

        processes = list(range(self.n))
        result_text = ""

        def calculate_need(max_matrix, alloc_matrix):
            return [[max_matrix[i][j] - alloc_matrix[i][j] for j in range(len(max_matrix[0]))] for i in range(len(max_matrix))]

        def is_safe_state():
            need = calculate_need(maxm, alloc)
            finish = [False] * len(processes)
            work = avail[:]
            safe_seq = []

            while True:
                allocated = False
                for i in range(len(processes)):
                    if not finish[i] and all(need[i][j] <= work[j] for j in range(len(work))):
                        for j in range(len(work)):
                            work[j] += alloc[i][j]
                        finish[i] = True
                        safe_seq.append(processes[i])
                        allocated = True
                if not allocated:
                    break
            return all(finish), safe_seq

        safe, seq = is_safe_state()

        if safe:
            result_text += "✅ No Deadlock Detected!\n"
            result_text += "✔ Safe Sequence: " + " → ".join(f"P{p}" for p in seq)
        else:
            result_text += "❌ Deadlock Detected!\n"
            while not safe:
                kill_p = len(processes) - 1
                result_text += f"💀 Terminating Process P{processes[kill_p]}\n"
                for j in range(len(avail)):
                    avail[j] += alloc[kill_p][j]
                processes.pop(kill_p)
                alloc.pop(kill_p)
                maxm.pop(kill_p)
                safe, seq = is_safe_state()
            result_text += "\n✅ Deadlock Recovered!\n✔ New Safe Sequence: " + " → ".join(f"P{p}" for p in seq)

        self.result_label.config(text=result_text)

# Run GUI
root = tk.Tk()
app = DeadlockGUI(root)
root.mainloop()
