from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python

def main():
    print(get_file_content("calculator", "dne"))
    print(write_file("calculator", "pkg/morelorem.txt", "sama lama heheh"))
    print(run_python("calculator", "main.py", "5 + 3"))

main()
