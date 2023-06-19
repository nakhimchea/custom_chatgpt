import os
from pandas import DataFrame, read_excel


class FileOperator:
    def __init__(self):
        print("Done Initializing File Reader")

    @staticmethod
    def read_from_excel(file_path: str) -> DataFrame:
        dataframe = read_excel(os.path.join(file_path))

        return dataframe

    @staticmethod
    def write_to_text(file_path: str, lines: list):
        print("Writing to text file...")
        with open(os.path.join(file_path), 'w') as file:
            file.writelines('\n'.join(lines))

        print("Done Writing to file.")
