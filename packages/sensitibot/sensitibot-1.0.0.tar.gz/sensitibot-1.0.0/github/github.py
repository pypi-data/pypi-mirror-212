import os
import sys
import urllib

import requests
from tqdm import tqdm

from reader import reader

api_url = 'https://api.github.com'
raw_url = 'https://raw.githubusercontent.com'
headers = {}
multipleRepositories = False


def process_github(owner, repository=None, branch=None, token=None, deep_search=False, wide_search=False):
    """
    Initiates the process of getting the files from GitHub.

    Args:
        owner (str): The GitHub user.
        repository (str): The repository to search.
        branch (str): The branch to search.
        token (str): The GitHub token.
        deep_search (bool): If true, the content of the files will be analyzed.
        wide_search (bool): If true, all the tables or sheets will be analyzed.

    Returns:
        dict: The result of getting the files.
    """
    global multipleRepositories
    TOKEN = os.getenv("GITHUB_TOKEN", default=None)
    if token != None:
        TOKEN = token

    if TOKEN != None:
        headers['Authorization'] = f'Bearer {TOKEN}'

    files = {}
    result = {}
    if repository == None:
        multipleRepositories = True
        files = get_files_from_repositories(owner)
    else:
        print(f'Searching repositoriy {owner}/{repository}:')
        files = get_files_from_repository(owner, repository, branch)
        if files != None:
            files = {"repositories": [files]}

    if files == None:
        print("\nNo dataset files found")
        return None

    result = reader.process_files(files, deep_search, wide_search)
    if result == None:
        print("\nYour files are clean!")
        return None

    return result


def get_files_from_repositories(owner):
    """
    Gets the files from all repositories of the GitHub user.

    Args:
        owner (str): The GitHub user.

    Returns:
        dict: The files from all repositories of the GitHub user.
    """
    print(f'Searching repositories for {owner}:')

    json_repos = get_repositories_from_api(owner)
    if json_repos == None:
        return None

    print(f'\t{len(json_repos)} public repositories found\n')

    result = {"repositories": []}

    number_of_repos = len(json_repos)
    remaining = get_rate_limit()
    if remaining <= number_of_repos:
        number_of_repos = remaining
        print(
            f'Warning: Only {number_of_repos} repositories will be analyzed, because the GitHub API rate limit has been exceeded.')

    pbar = tqdm(json_repos,
                desc="Reading repositories", ncols=200, unit=" repo", ascii=' █', bar_format="Reading repository {n_fmt}/{total_fmt} |{bar:20}| r:{desc}")
    for repository in pbar:
        pbar.set_description(repository["name"])
        result_repository = get_files_from_repository(
            owner, repository["name"], repository["default_branch"])

        if result_repository == None:
            continue

        result["repositories"].append(result_repository)

    if len(result["repositories"]) == 0:
        return None

    return result


def get_repositories_from_api(owner):
    """
    Gets the repositories from the GitHub API.

    Args:
        owner (str): The GitHub user.

    Returns:
        dict: The repositories from the GitHub API.
    """
    json_repos = {}
    per_page = 100
    count = per_page
    page = 1
    while count == per_page:
        response = requests.get(
            f'{api_url}/users/{owner}/repos?page={page}&per_page={per_page}', headers=headers)
        if not response.ok:
            error = response.json()
            error_message = error.get('message')
            if error_message == "Not Found":
                print(f'Error: Github User or Organization {error_message}\n')
                sys.exit(1)  # exit with non-zero exit code
            elif error_message == "Bad credentials":
                print("Error: Bad credentials\n")
                sys.exit(1)  # exit with non-zero exit code
            elif "API rate limit exceeded" in error_message:
                if page == 1:   # If the first request has already exceeded the rate limit, we can't continue
                    print(
                        "API rate limit exceeded, could not analyze GitHub user or organization.")
                    return None
                else:           # If the rate limit has been exceeded after the first request, we can continue with the repositories already found
                    print(
                        "API rate limit exceeded, not all repositories will be analyzed.")
                    break

        if page == 1:
            json_repos = response.json()
        else:
            json_repos.extend(response.json())
        page += 1
        count = len(response.json())

    return json_repos


def get_rate_limit():
    """
    Gets the rate limit from the GitHub API.

    Returns:
        int: The rate limit from the GitHub API.
    """
    response = requests.get(f'{api_url}/rate_limit', headers=headers)
    json_data = response.json()
    return json_data["rate"]["remaining"]


def get_files_from_repository(owner, repository, branch=None):
    """
    Gets the files from the GitHub repository.

    Args:
        owner (str): The GitHub user.
        repository (str): The repository to search.
        branch (str): The branch to search.

    Returns:
        dict: The files from the GitHub repository.
    """
    # In case the branch is not specified, we need to get the default branch
    if branch == None:
        branch = get_default_branch_of_repository(owner, repository)

    response = requests.get(
        f'{api_url}/repos/{owner}/{repository}/git/trees/{branch}?recursive=1', headers=headers)
    if not response.ok:
        error = response.json()
        error_message = error.get('message')
        if error_message == "Not Found":
            if multipleRepositories:
                return None
            else:
                print(f'Error: Repository {error_message}\n')
                sys.exit(1)  # exit with non-zero exit code
        elif error_message == "Bad credentials":
            print("Error: Bad credentials\n")
            sys.exit(1)  # exit with non-zero exit code
        elif error_message == "Git Repository is empty.":
            return None
        elif "API rate limit exceeded" in error_message:
            print("API rate limit exceeded")
            return None

    json_files = response.json()

    result_repository = file_selector(json_files, owner, repository)

    return result_repository


def get_default_branch_of_repository(owner, repository):
    """
    Gets the default branch of the GitHub repository.

    Args:
        owner (str): The GitHub user.
        repository (str): The repository to search.

    Returns:
        str: The default branch of the GitHub repository.
    """
    response = requests.get(
        f'{api_url}/repos/{owner}/{repository}', headers=headers)
    if not response.ok:
        error = response.json()
        error_message = error.get('message')
        if error_message == "Not Found":
            if multipleRepositories:
                return None
            else:
                print(f'Error: Repository {error_message}\n')
                sys.exit(1)  # exit with non-zero exit code
        elif error_message == "Bad credentials":
            print("Error: Bad credentials\n")
            sys.exit(1)  # exit with non-zero exit code
        elif "API rate limit exceeded" in error_message:
            print(
                "API rate limit exceeded, not all repositories have been analyzed.")
            return None

    json_repo = response.json()
    return json_repo["default_branch"]


def file_selector(json_files, owner, repository):
    """
    Selects the data sets files from the GitHub repository.

    Args:
        json_files (dict): The files from the GitHub repository.
        owner (str): The GitHub user.
        repository (str): The repository.

    Returns:
        dict: The data sets files from the GitHub repository.
    """
    result_repository = {"name": repository, "files": []}

    extensions = [".csv", ".tsv", ".xlsx", "xlsm", "xltx",
                  "xltm", ".mdb", ".accdb", ".json", ".jsonl"]

    for file in json_files["tree"]:
        if (file["type"] == "blob"):

            if any(file["path"].endswith(ext) for ext in extensions):
                result_repository["files"].append(
                    urllib.parse.quote(f'{raw_url}/{owner}/{repository}/master/{file["path"]}', safe=':/.'))

    # Only return the result if there are files of any type
    if len(result_repository["files"]) == 0:
        return None

    return result_repository
