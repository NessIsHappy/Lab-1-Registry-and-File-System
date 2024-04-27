import os
import shutil


def create_file(file_name: str) -> None:
    try:
        file = open(file_name, "x")
        file.close()
    except FileExistsError:
        print("Already exists!")


def delete_file(file_name: str) -> None:
    try:
        os.remove(file_name)
    except FileNotFoundError:
        print("No such file!")


def append_file(file_name: str) -> None:
    text = input("Write text to append to file:")
    with open(file_name, "a") as file:
        file.write(text)


def read_file(file_name: str) -> None:
    try:
        with open(file_name, "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("No such file!")


def copy_file(file_name: str, new_directory: str) -> None:
    new_name = os.path.join(new_directory, file_name)
    shutil.copyfile(file_name, new_name)


def rename_file(file_name: str, new_name: str) -> None:
    try:
        os.rename(file_name, new_name)
    except FileExistsError:
        print("File exists!")


def main():
    create_file('file.txt')
    append_file('file.txt')
    read_file('file.txt')
    copy_file('file.txt', 'Z:\\Desktop\\ЦК')
    rename_file('file.txt', 'file_diff.txt')
    delete_file('file_diff.txt')


if __name__ == "__main__":
    main()
