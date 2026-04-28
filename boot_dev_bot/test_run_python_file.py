from functions.run_python_files import run_python_file


def test():
    result = run_python_file("calculator", "main.py")
    print("Result for calculator.py file:")
    print(result)
    print("")

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Result for calculator.py doing 3 + 5:")
    print(result)
    print("")

    result = run_python_file("calculator", "tests.py")
    print("Result for calculator.py tests:")
    print(result)
    print("")

    result = run_python_file("calculator", "../main.py")
    print("Result for 'calculator/../main.py' file:")
    print(result)
    print("")

    result = run_python_file("calculator", "nonexistent.py")
    print("Result for '/calculator/nonexistent.py' file:")
    print(result)
    print("")

    result = run_python_file("calculator", "lorem.txt")
    print("Result for 'calculator/lorem.txt' file:")
    print(result)
    print("")


if __name__ == "__main__":
    test()
