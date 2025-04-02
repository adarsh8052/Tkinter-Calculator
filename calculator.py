import tkinter as tk
import re
class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Calculator")
        self.root.geometry("320x420")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        try:
            self.root.iconbitmap("calculator.ico")
        except:
            pass
        self.current_expression = ""
        self.total_expression = ""

        # Create the display frame
        self.display_frame = self.create_display_frame()
        self.total_label, self.current_label = self.create_display_labels()

        # Dictionary with all the buttons
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }

        # Create the buttons frame
        self.buttons_frame = self.create_buttons_frame()

        # Configure the buttons frame to expand with the window
        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        # Create the digit buttons
        self.create_digit_buttons()

        # Create the operator buttons
        self.create_operator_buttons()

        # Create the special buttons
        self.create_special_buttons()

        # Bind keyboard keys
        self.bind_keys()

    def bind_keys(self):
        """Bind keyboard keys to calculator functions"""
        self.root.bind("<Return>", lambda event: self.evaluate())
        self.root.bind("<BackSpace>", lambda event: self.backspace())
        self.root.bind("<Key>", self.key_press)

    def key_press(self, event):
        """Handle key press events"""
        if event.char.isdigit() or event.char == '.':
            self.add_to_expression(event.char)
        elif event.char == '+':
            self.append_operator('+')
        elif event.char == '-':
            self.append_operator('-')
        elif event.char == '*':
            self.append_operator('×')
        elif event.char == '/':
            self.append_operator('÷')
        elif event.char == '=':
            self.evaluate()
        elif event.char == '\r':  # Enter key
            self.evaluate()

    def create_display_frame(self):
        """Create the frame that will contain the display"""
        frame = tk.Frame(self.root, height=100, bg="#f8f8f8", bd=2, relief=tk.GROOVE)
        frame.pack(expand=True, fill="both", padx=10, pady=10)
        return frame

    def create_display_labels(self):
        """Create the labels that will display the expressions and results"""
        total_label = tk.Label(
            self.display_frame,
            text=self.total_expression,
            anchor=tk.E,
            bg="#f8f8f8",
            fg="#404040",
            padx=10,
            font=("Arial", 14)
        )
        total_label.pack(expand=True, fill="both")

        current_label = tk.Label(
            self.display_frame,
            text=self.current_expression,
            anchor=tk.E,
            bg="#f8f8f8",
            fg="#000000",
            padx=10,
            font=("Arial", 24, "bold")
        )
        current_label.pack(expand=True, fill="both")

        return total_label, current_label

    def create_buttons_frame(self):
        """Create the frame that will contain all the buttons"""
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(expand=True, fill="both", padx=10, pady=10)
        return frame

    def create_digit_buttons(self):
        """Create the digit buttons (0-9 and decimal point)"""
        for digit, grid_value in self.digits.items():
            button = tk.Button(
                self.buttons_frame,
                text=str(digit),
                font=("Arial", 14),
                fg="#000000",
                bg="#ffffff",
                bd=1,
                relief=tk.RAISED,
                activebackground="#e0e0e0",
                command=lambda x=digit: self.add_to_expression(x)
            )
            button.grid(
                row=grid_value[0],
                column=grid_value[1],
                sticky=tk.NSEW,
                padx=5,
                pady=5
            )

    def create_operator_buttons(self):
        """Create the operator buttons (+, -, ×, ÷)"""
        # Addition button
        self.create_addition_button()

        # Subtraction button
        self.create_subtraction_button()

        # Multiplication button
        self.create_multiplication_button()

        # Division button
        self.create_division_button()

    def create_addition_button(self):
        """Create the addition button (+)"""
        button = tk.Button(
            self.buttons_frame,
            text="+",
            font=("Arial", 14, "bold"),
            fg="#ffffff",
            bg="#ff9500",
            bd=1,
            relief=tk.RAISED,
            activebackground="#e08500",
            command=lambda: self.append_operator("+")
        )
        button.grid(row=3, column=4, sticky=tk.NSEW, padx=5, pady=5)

    def create_subtraction_button(self):
        """Create the subtraction button (-)"""
        button = tk.Button(
            self.buttons_frame,
            text="-",
            font=("Arial", 14, "bold"),
            fg="#ffffff",
            bg="#ff9500",
            bd=1,
            relief=tk.RAISED,
            activebackground="#e08500",
            command=lambda: self.append_operator("-")
        )
        button.grid(row=2, column=4, sticky=tk.NSEW, padx=5, pady=5)

    def create_multiplication_button(self):
        """Create the multiplication button (×)"""
        button = tk.Button(
            self.buttons_frame,
            text="×",
            font=("Arial", 14, "bold"),
            fg="#ffffff",
            bg="#ff9500",
            bd=1,
            relief=tk.RAISED,
            activebackground="#e08500",
            command=lambda: self.append_operator("×")
        )
        button.grid(row=1, column=4, sticky=tk.NSEW, padx=5, pady=5)

    def create_division_button(self):
        """Create the division button (÷)"""
        button = tk.Button(
            self.buttons_frame,
            text="÷",
            font=("Arial", 14, "bold"),
            fg="#ffffff",
            bg="#ff9500",
            bd=1,
            relief=tk.RAISED,
            activebackground="#e08500",
            command=lambda: self.append_operator("÷")
        )
        button.grid(row=0, column=4, sticky=tk.NSEW, padx=5, pady=5)

    def create_special_buttons(self):
        """Create the special buttons (clear, equals, etc.)"""
        # Clear button
        self.create_clear_button()

        # Equals button
        self.create_equals_button()

        # Square button
        self.create_square_button()

        # Square root button
        self.create_sqrt_button()

        # Backspace button
        self.create_backspace_button()

    def create_clear_button(self):
        """Create the clear button (C)"""
        button = tk.Button(
            self.buttons_frame,
            text="C",
            font=("Arial", 14),
            fg="#ffffff",
            bg="#a5a5a5",
            bd=1,
            relief=tk.RAISED,
            activebackground="#909090",
            command=self.clear
        )
        button.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)

    def create_equals_button(self):
        """Create the equals button (=)"""
        button = tk.Button(
            self.buttons_frame,
            text="=",
            font=("Arial", 14, "bold"),
            fg="#ffffff",
            bg="#ff9500",
            bd=1,
            relief=tk.RAISED,
            activebackground="#e08500",
            command=self.evaluate
        )
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

    def create_square_button(self):
        """Create the square button (x²)"""
        button = tk.Button(
            self.buttons_frame,
            text="x²",
            font=("Arial", 14),
            fg="#ffffff",
            bg="#a5a5a5",
            bd=1,
            relief=tk.RAISED,
            activebackground="#909090",
            command=self.square
        )
        button.grid(row=0, column=2, sticky=tk.NSEW, padx=5, pady=5)

    def create_sqrt_button(self):
        """Create the square root button (√)"""
        button = tk.Button(
            self.buttons_frame,
            text="√",
            font=("Arial", 14),
            fg="#ffffff",
            bg="#a5a5a5",
            bd=1,
            relief=tk.RAISED,
            activebackground="#909090",
            command=self.sqrt
        )
        button.grid(row=0, column=3, sticky=tk.NSEW, padx=5, pady=5)

    def create_backspace_button(self):
        """Create the backspace button (⌫)"""
        button = tk.Button(
            self.buttons_frame,
            text="⌫",
            font=("Arial", 14),
            fg="#ffffff",
            bg="#a5a5a5",
            bd=1,
            relief=tk.RAISED,
            activebackground="#909090",
            command=self.backspace
        )
        button.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

    def add_to_expression(self, value):
        """Add a digit or decimal point to the current expression"""
        # Prevent multiple decimal points
        if value == "." and "." in self.current_expression:
            return

        self.current_expression += str(value)
        self.update_current_label()

    def append_operator(self, operator):
        """Append an operator to the expression"""
        if not self.current_expression and not self.total_expression:
            return

        if not self.current_expression:
            self.total_expression = self.total_expression[:-1] + operator
        else:
            # If there's a current expression, move it to the total expression
            # and add the operator
            self.total_expression += self.current_expression + operator
            self.current_expression = ""

        self.update_labels()

    def clear(self):
        """Clear all expressions"""
        self.current_expression = ""
        self.total_expression = ""
        self.update_labels()

    def backspace(self):
        """Remove the last character from the current expression"""
        self.current_expression = self.current_expression[:-1]
        self.update_current_label()

    def square(self):
        """Square the current expression"""
        if not self.current_expression:
            return

        try:
            value = float(self.current_expression)
            self.current_expression = str(value ** 2)
            self.update_current_label()
        except:
            self.current_expression = "Error"
            self.update_current_label()

    def sqrt(self):
        """Calculate the square root of the current expression"""
        if not self.current_expression:
            return

        try:
            value = float(self.current_expression)
            if value < 0:
                self.current_expression = "Error"
            else:
                self.current_expression = str(value ** 0.5)
            self.update_current_label()
        except:
            self.current_expression = "Error"
            self.update_current_label()

    def evaluate(self):
        """Evaluate the full expression"""
        if not self.total_expression and not self.current_expression:
            return

        try:
            # Prepare the full expression for evaluation
            expression = self.total_expression + self.current_expression

            # Replace the display symbols with actual operators
            expression = expression.replace("×", "*")
            expression = expression.replace("÷", "/")

            # Evaluate the expression
            result = str(eval(expression))

            # Update the display
            self.total_expression = ""
            self.current_expression = result
            self.update_labels()
        except Exception as e:
            self.current_expression = "Error"
            self.update_current_label()

    def update_labels(self):
        """Update both display labels"""
        self.update_total_label()
        self.update_current_label()

    def update_total_label(self):
        """Update the total expression label"""
        self.total_label.config(text=self.total_expression)

    def update_current_label(self):
        """Update the current expression label"""
        # Format the display for better readability
        if self.current_expression:
            # If it's a number, format it nicely
            if self.current_expression != "Error":
                try:
                    # Check if it's a float with decimal part
                    if "." in self.current_expression:
                        # Remove trailing zeros after decimal point
                        display_text = re.sub(r'\.0+$', '', self.current_expression)
                    else:
                        display_text = self.current_expression
                except:
                    display_text = self.current_expression
            else:
                display_text = self.current_expression
        else:
            display_text = "0"

        self.current_label.config(text=display_text)


if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()