import os
import sys
from git import InvalidGitRepositoryError, Repo


MOCKED = True
PROD_PYPI_INDEX = "https://pypi.org/simple/"


def yellow(rhs):
    """Return the rhs in red."""
    return f"\033[93m{rhs}\033[0m"


def green(rhs):
    """Return the rhs in green."""
    return f"\033[92m{rhs}\033[0m"


def red(rhs):
    """Return the rhs in red."""
    return f"\033[91m{rhs}\033[0m"

def magenta(rhs):
    """Return the rhs in magenta."""
    return f"\033[95m{rhs}\033[0m"


def yes_no(question, *args):
    """Ask a yes/no question and return True or False."""
    options = args or ["No", "Yes"]

    print(question)
    for i, opt in enumerate(options):
        print(f"{i}: {opt}")
    while True:
        inp = int(input(green("Enter a number: ")))
        if inp in [0, 1]:
            return [False, True][inp]
        else:
            print("You must choose 0 for {}, or 1 for {}..".format(*options))

def get_repo():
    """Return the Repository object.

    Exit if not in a workable state.
    """
    try:
        repo = Repo(".")
    except InvalidGitRepositoryError:
        sys.stderr.write("Not a git repo. Can't continue.\n")
        sys.exit(1)
    if not MOCKED:
        if repo.is_dirty():
            sys.stderr.write( red("Dirty repo. Can't continue. Commit or stash changes and try again.\n"))
            sys.exit(1)
    return repo

def nonblank_lines(fileobject):
    """Generator to help search a file."""
    for line in fileobject:
        line = line.rstrip()
        if line:
            yield line

def first_nonblank_line(filename):
    """Use a generator to return the first non blank line, or None."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            gen = nonblank_lines(f)
            return next(gen, None)
    except FileNotFoundError:
        print("The specified file was not found.")
        return None
    except PermissionError:
        print("You don't have permission to access this file.")
        return None



def get_pip_name(repo):
    """
    Return the pip name, which may be different than the repo name.

    If the pip name is different, it should be the first line of the MANIFEST
    file as a comment.
    """
    manifest_file = os.path.join(repo.working_dir, "MANIFEST.in")
    base_name = os.path.basename(repo.working_dir)
    try:
        first_line = first_nonblank_line(manifest_file)
        if first_line[0] == "#":
            return first_line.split(" ")[1]
    except IndexError: 
        pass
    return base_name
    

def get_recent_commits(repo):
    """Get commits frm here back to the last tag on the master branch."""
    branch = repo.active_branch
    master_shas = set(
        [c.hexsha for c in repo.iter_commits(rev=repo.branches.master)]
    )
    tag_shas = [t.commit.hexsha for t in reversed(repo.tags)]
    
    master_tag_sha = None
    for sha in tag_shas:
        if sha in master_shas:
            master_tag_sha = sha
            break
    result = []
    for c in repo.iter_commits(rev=branch):
        result.append(c)
        if c.hexsha == master_tag_sha:
            break
    return result

def enter_to_continue_or_exit(cont_message):
    cont = input(
        green(
            "f{cont_message}. Type 'exit' to exit."
        )
    )
    if cont.lower() == "exit":
        sys.stderr.write("Exited.\n")
        sys.exit(0)