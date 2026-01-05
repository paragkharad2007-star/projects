import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import ast

# ---------------- Bug Finder Functions ----------------
def check_syntax(code, file_name="<input>"):
    try:
        compile(code, file_name, "exec")
        return None
    except SyntaxError as e:
        return f"{e}"

def find_undefined_vars(code):
    tree = ast.parse(code)
    defined_names = set()
    undefined_names = set()

    class Analyzer(ast.NodeVisitor):
        def __init__(self):
            self.defined = set()
            self.used = set()

        def visit_FunctionDef(self, node):
            for arg in node.args.args:
                self.defined.add(arg.arg)
            self.generic_visit(node)

        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Store):
                self.defined.add(node.id)
            elif isinstance(node.ctx, ast.Load):
                if node.id not in self.defined and not hasattr(__builtins__, node.id):
                    self.used.add(node.id)

    analyzer = Analyzer()
    analyzer.visit(tree)
    undefined_names = analyzer.used - analyzer.defined
    return list(undefined_names)

def find_unused_imports(code):
    tree = ast.parse(code)
    imports = set()
    used_names = set()

    class ImportAnalyzer(ast.NodeVisitor):
        def visit_Import(self, node):
            for alias in node.names:
                imports.add(alias.asname or alias.name)

        def visit_ImportFrom(self, node):
            for alias in node.names:
                imports.add(alias.asname or alias.name)

        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Load):
                used_names.add(node.id)

    analyzer = ImportAnalyzer()
    analyzer.visit(tree)
    unused = imports - used_names
    return list(unused)

def generate_quick_fix(code):
    fixes = []
    undefined_vars = find_undefined_vars(code)
    if undefined_vars:
        for var in undefined_vars:
            fixes.append(f"Initialize undefined variable '{var}' at top: {var} = None")

    unused_imports = find_unused_imports(code)
    if unused_imports:
        for imp in unused_imports:
            fixes.append(f"Remove unused import '{imp}'")

    if code.rstrip() != code:
        fixes.append("Remove trailing blank lines and spaces at end of file")

    if not fixes:
        fixes.append("No quick fixes needed!")
    return fixes

def apply_quick_fix(code):
    lines = code.splitlines()
    undefined_vars = find_undefined_vars(code)
    unused_imports = find_unused_imports(code)

    for var in undefined_vars:
        lines.insert(0, f"{var} = None  # Quick fix applied")

    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            if any(imp in stripped for imp in unused_imports):
                continue
        new_lines.append(line)

    while new_lines and new_lines[-1].strip() == "":
        new_lines.pop()

    return "\n".join(new_lines)

def analyze_code(code, file_name="<input>"):
    results = []

    syntax_err = check_syntax(code, file_name)
    if syntax_err:
        results.append(("Syntax Error", syntax_err))
    else:
        results.append(("Syntax", "No syntax errors detected"))

    undefined_vars = find_undefined_vars(code)
    if undefined_vars:
        results.append(("Warning", f"Undefined variables detected: {undefined_vars}"))
    else:
        results.append(("Variables", "No undefined variables"))

    unused_imports = find_unused_imports(code)
    if unused_imports:
        results.append(("Info", f"Unused imports detected: {unused_imports}"))
    else:
        results.append(("Info", "No unused imports detected"))

    return results

# ---------------- GUI Functions ----------------
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            code_input.delete("1.0", tk.END)
            code_input.insert(tk.END, code)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file:\n{e}")

def run_analysis():
    code = code_input.get("1.0", tk.END).strip()
    if not code:
        messagebox.showwarning("Warning", "Please enter or load Python code first.")
        return

    results = analyze_code(code)

    output_area.config(state='normal')
    output_area.delete("1.0", tk.END)
    for r_type, msg in results:
        if "Error" in r_type:
            output_area.insert(tk.END, f"{r_type}: {msg}\n", "error")
        elif "Warning" in r_type:
            output_area.insert(tk.END, f"{r_type}: {msg}\n", "warning")
        elif "Info" in r_type:
            output_area.insert(tk.END, f"{r_type}: {msg}\n", "ok")
    output_area.config(state='disabled')

    quick_fixes = generate_quick_fix(code)
    quick_fix_area.config(state='normal')
    quick_fix_area.delete("1.0", tk.END)
    for fix in quick_fixes:
        quick_fix_area.insert(tk.END, f"- {fix}\n")
    quick_fix_area.config(state='disabled')

def apply_fixes():
    code = code_input.get("1.0", tk.END)
    fixed_code = apply_quick_fix(code)
    code_input.delete("1.0", tk.END)
    code_input.insert(tk.END, fixed_code)
    messagebox.showinfo("Quick Fix", "Quick fixes applied to the code!")

# ---------------- Tkinter GUI ----------------
root = tk.Tk()
root.title("Python Bug Finder - Quick Fix")
root.geometry("850x750")
root.configure(bg="#1e1e1e")

# Code input
code_label = tk.Label(root, text="Python Code:", fg="white", bg="#1e1e1e", font=("Arial", 12, "bold"))
code_label.pack(pady=(10, 0))
code_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 12), height=15, bg="#2e2e2e", fg="white", insertbackground="white")
code_input.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Buttons
button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(pady=5)
load_button = tk.Button(button_frame, text="Load File", command=select_file, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
load_button.pack(side=tk.LEFT, padx=5)
analyze_button = tk.Button(button_frame, text="Run Analysis", command=run_analysis, bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
analyze_button.pack(side=tk.LEFT, padx=5)
fix_button = tk.Button(button_frame, text="Apply Quick Fixes", command=apply_fixes, bg="#FF9800", fg="white", font=("Arial", 12, "bold"))
fix_button.pack(side=tk.LEFT, padx=5)

# Analysis output
output_label = tk.Label(root, text="Analysis Results:", fg="white", bg="#1e1e1e", font=("Arial", 12, "bold"))
output_label.pack(pady=(10, 0))
output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 12), height=10, bg="#2e2e2e", fg="white", state='disabled', insertbackground="white")
output_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Quick Fix output
quick_label = tk.Label(root, text="Quick Fix Suggestions:", fg="white", bg="#1e1e1e", font=("Arial", 12, "bold"))
quick_label.pack(pady=(10, 0))
quick_fix_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 12), height=8, bg="#2e2e2e", fg="white", state='disabled', insertbackground="white")
quick_fix_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Color tags
output_area.tag_configure("error", foreground="#ff4c4c")
output_area.tag_configure("warning", foreground="#ffa500")
output_area.tag_configure("ok", foreground="#4CAF50")

root.mainloop()
