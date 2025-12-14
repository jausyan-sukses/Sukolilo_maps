import tkinter as tk

class CoolButtonFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="#f4f4f2")  # light neutral background
        self.create_buttons()

    def on_enter(self, event):
        event.widget['bg'] = '#e6e6fa'  # gentle hover lavender

    def on_leave(self, event):
        event.widget['bg'] = '#3bd45c'  # original button color

    def create_buttons(self):
        # List of (button text, command function)
        buttons = [
            ("Draw Node", lambda: print("Set draw mode")),
            ("Delete", lambda: print("Set delete mode")),
            ("Connect Nodes", lambda: print("Set connect mode")),
            ("Create Turn", lambda: print("Set turn mode")),
            ("Print List", lambda: print("Print connections")),
            ("Find Quick", lambda: print("Set find quick mode"))
        ]
        for text, cmd in buttons:
            btn = tk.Button(
                self,
                text=text,
                command=cmd,
                font=("Segoe UI", 11, "bold"),
                bg="#3bd45c",
                fg="#262626",
                activebackground="#d11717",
                activeforeground="#262626",
                borderwidth=0,
                relief="flat",
                padx=20,
                pady=8,
                cursor="hand2"
            )
            btn.pack(side="top", fill="x", expand=True, pady=5, padx=30)
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)

# Minimal example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Cool Simple Tkinter Buttons")
    CoolButtonFrame(root).pack(fill="x", pady=30)
    root.mainloop()