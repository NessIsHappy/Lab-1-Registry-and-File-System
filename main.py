import os
import shutil
import argparse
import winreg


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


def read_file(file_name: str) -> str:
    try:
        with open(file_name, "r") as file:
            print(file.read())
            return file.read()
    except FileNotFoundError:
        print("No such file!")
        return ''


def copy_file(file_name: str, new_directory: str) -> None:
    new_name = os.path.join(new_directory, file_name)
    shutil.copyfile(file_name, new_name)


def rename_file(file_name: str, new_name: str) -> None:
    try:
        os.rename(file_name, new_name)
    except FileExistsError:
        print("File exists!")


def create_key(key_name: str) -> None:
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_name)
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Can't create a key! {e}")


def delete_key(key_name: str) -> None:
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_name)
    except Exception as e:
        print(f"Can't delete a key! {e}")


def write_key(key_name: str, value_name: str, value_data) -> None:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_name, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Can't append to key! {e}")


def find_file(target_dir: str, search_string: str) -> None:
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as f:
                    for line_number, line in enumerate(f, 1):
                        if search_string in line:
                            print(f'Found in file: {file_path}, line: {line_number}, content: {line.strip()}')
            except (IOError, OSError):
                print(f'Error reading file: {file_path}')


def find_key(root_key: str, target_value: str) -> None:
    def search_recursively(key: any) -> None:
        try:
            i = 0
            while True:
                subkey_name = winreg.EnumKey(key, i)
                subkey = winreg.OpenKey(key, subkey_name)
                search_recursively(subkey)
                i += 1
        except WindowsError:
            pass

        try:
            i = 0
            while True:
                value_name, value_data, value_type = winreg.EnumValue(key, i)
                if target_value in str(value_data):
                    print(f"Found '{target_value}' in {winreg.QueryValue(key, None)}\\{value_name}")
                i += 1
        except WindowsError:
            pass

    root_key_map = {
        'HKEY_CLASSES_ROOT': winreg.HKEY_CLASSES_ROOT,
        'HKEY_CURRENT_USER': winreg.HKEY_CURRENT_USER,
        'HKEY_LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE,
        'HKEY_USERS': winreg.HKEY_USERS,
        'HKEY_CURRENT_CONFIG': winreg.HKEY_CURRENT_CONFIG
    }

    if root_key in root_key_map:
        hkey = root_key_map[root_key]
        with winreg.ConnectRegistry(None, hkey) as reg:
            search_recursively(reg)


def main():

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    filesys_parser = subparsers.add_parser('filesys')
    filesys_parser.add_argument('-cr', '--create', type=str, nargs=1, metavar='FILENAME', help='create a new file')
    filesys_parser.add_argument('-a', '--append', type=str, nargs=1, metavar='FILENAME', help='append to a file')
    filesys_parser.add_argument('-rd', '--read', type=str, nargs=1, metavar='FILENAME', help='read from a file')
    filesys_parser.add_argument('-cp', '--copy', type=str, nargs=2, metavar=('OLD', 'NEW'), help='copy a file')
    filesys_parser.add_argument('-rn', '--rename', type=str, nargs=2, metavar=('FILENAME', 'DIR'), help='rename file')
    filesys_parser.add_argument('-d', '--delete', type=str, nargs=1, metavar='FILENAME', help='delete a file')
    filesys_parser.add_argument('-f', '--find', type=str, nargs=2, metavar=('DIR', 'STRING'), help='find a string')

    registry_parser = subparsers.add_parser('registry')
    registry_parser.add_argument('-cr', '--create', nargs=1, metavar='KEYNAME', help='create a new key')
    registry_parser.add_argument('-d', '--delete', nargs=1, metavar='KEYNAME', help='delete a key')
    registry_parser.add_argument('-w', '--write', nargs=3, metavar=('KEYNAME', 'NAME', 'DATA'), help='write to a key')
    registry_parser.add_argument('-f', '--find', nargs=2, metavar=('ROOTKEY', 'VALUE'), help='find a key')

    args = parser.parse_args()
    args_dict = vars(args)

    if len(vars(args)) == 7:
        for command in args_dict:
            if args_dict[command] is not None:
                if command == 'create':
                    create_file(args_dict[command][0])
                elif command == 'append':
                    append_file(args_dict[command][0])
                elif command == 'read':
                    read_file(args_dict[command][0])
                elif command == 'copy':
                    copy_file(args_dict[command][0], args_dict[command][1])
                elif command == 'rename':
                    rename_file(args_dict[command][0], args_dict[command][1])
                elif command == 'delete':
                    delete_file(args_dict[command][0])
                elif command == 'find':
                    find_file(args_dict[command][0], args_dict[command][1])
    elif len(vars(args)) == 4:
        for command in args_dict:
            if args_dict[command] is not None:
                if command == 'create':
                    create_key(args_dict[command][0])
                elif command == 'delete':
                    delete_key(args_dict[command][0])
                elif command == 'write':
                    write_key(args_dict[command][0], args_dict[command][1], args_dict[command][2])
                elif command == 'find':
                    find_key(args_dict[command][0], args_dict[command][1])


if __name__ == "__main__":
    main()
