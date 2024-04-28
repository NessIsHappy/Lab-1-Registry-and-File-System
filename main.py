import os
import shutil
import argparse


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

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    filesys_parser = subparsers.add_parser('filesys')
    filesys_parser.add_argument('-cr', '--create', type=str, nargs=1, help='create a new file')
    filesys_parser.add_argument('-a', '--append', type=str, nargs=1, help='append to a file')
    filesys_parser.add_argument('-rd', '--read', type=str, nargs=1, help='read from a file')
    filesys_parser.add_argument('-cp', '--copy', type=str, nargs=2, help='copy file to a directory')
    filesys_parser.add_argument('-rn', '--rename', type=str, nargs=2, help='rename file')
    filesys_parser.add_argument('-d', '--delete', type=str, nargs=1, help='delete a file')

    registry_parser = subparsers.add_parser('registry')
    registry_parser.add_argument('-cr', '--create', nargs=1, help='create a new key')
    registry_parser.add_argument('-d', '--delete', nargs=1, help='delete a key')
    registry_parser.add_argument('-w', '--write', nargs=1, help='write to a key')

    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
