import os

from reader import reader


def process_local(directory=None, deep_search=False, wide_search=False):
    """
    Initiates the process of getting the files from the local repository.

    Args:
        directory (str): The directory to search.
        deep_search (bool): If true, the content of the files will be analyzed.
        wide_search (bool): If true, all the tables or sheets will be analyzed.

    Returns:
        dict: The result of getting the files.
    """
    files = get_files_recursively(directory)

    if files == None:
        print("\nNo dataset files found")
        return None

    result = reader.process_files(files, deep_search, wide_search)
    if result == None:
        print("\nYour files are clean!")
        return None

    return result


def get_files_recursively(directory):
    """
    Gets the files from the local directory.

    Args:
        directory (str): The directory to search.

    Returns:
        dict: The files from the local directory.
    """
    if directory == None:
        directory = "./"

    result = {"repositories": [{"name": "local", "files": []}]}

    extensions = [".csv", ".tsv", ".xlsx", "xlsm", "xltx",
                  "xltm", ".mdb", ".accdb", ".json", ".jsonl"]

    print(f'Searching directory {directory}:')

    for root, _, files in os.walk(directory):
        for filename in files:

            if any(filename.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, filename)
                result["repositories"][0]["files"].append(filepath)

    # Only return the result if there are files of any type
    if len(result["repositories"][0]["files"]) == 0:
        return None

    return result
