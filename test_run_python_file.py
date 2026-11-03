from functions.run_python_file import run_python_file


print("Result of running main.py:")
print(run_python_file("calculator", "main.py"))
print("Result of running main.py with arguments:")
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print("Result of running tests.py:")
print(run_python_file("calculator", "tests.py"))
print("Result of running ../main.py:")
print(run_python_file("calculator", "../main.py"))
print("Result of running nonexistent.py:")
print(run_python_file("calculator", "nonexistent.py"))
print("Result of running lorem.txt:")
print(run_python_file("calculator", "lorem.txt"))