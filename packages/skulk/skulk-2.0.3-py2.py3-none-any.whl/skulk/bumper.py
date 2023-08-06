import sys
import os
import re
import json
import subprocess
import semver
import functools

from . import util


MOCKED = False
MOCK_VERSIONS = {
    "pypi": ["0.1.7", "1.4.3", "1.4.4", "1.4.5"],
    "tags": ["0.1.2", "0.1.3", "1.4.4", "1.4.5"],
}


class Bumper(object):
    """A class to help the user bump the version."""

    def __init__(self, repo, pip_name):
        self.repo = repo
        self.pip_name = pip_name
        self.version_filename = os.path.join(self.repo.working_dir, "VERSION")
        self.current_version = _read_version_file(self.version_filename)
        self.versions = None
        self.next_version = None

        self.latest_pypi_version = None
        self.latest_tag_version = None
        self.latest_version = None

    def is_prerelease(self):
        """Return True if the current version is a prerelease."""
        return semver.Version.parse(self.current_version).prerelease is not None

    def run(self):
        """Wizard to choose a version."""

        self._set_versions()

        print("Versions:")
        print(json.dumps(self.versions, indent=3))
        print(f"The latest version on PyPi is: {self.latest_pypi_version}")
        print(f"The latest tag in the repo is: {self.latest_tag_version}")
        print(
            "When you push this branch, we'll deploy to PyPi and we'll tag the repo with the version you choose."
        )

        if self.current_version not in self.versions["pypi"] + self.versions["tags"]:
            print(
                f"The local VERSION file contains a valid version: {self.current_version}."
            )

            print("You can use this version or you can bump to a new version.")
            do_bump = util.yes_no("Do you wish to bump the version?")
            if not do_bump:
                return

        else:
            do_bump = True
            print(
                f"The local VERSION file contains an invalid version: {self.current_version}. It has been used already."
            )
            print("You'll need to bump the version.")

        version_options = get_version_options(self.latest_version)

        version_options += [
            "Explicit: Specify a version manually. This is not recommended.",
            "Cancel: I changed my mind. I don't want to tag or release. I just want to push.",
            "Exit!"
        ]

        # options = [f"{v[0]: <16} {v[1]}" for v in version_options]
        num_options = len(version_options)
        exit_option = num_options
        no_tags_option = num_options - 1
        custom_option = num_options - 2

        bump_type = 0
        msg = "Choose a new version"
        while bump_type not in range(1, len(version_options) + 1):
            print(msg)
            for i, opt in enumerate(version_options):
                n = i + 1
                print(f"{n}: {opt}")
            bump_type = input(util.green("Enter a number: "))
            if not bump_type.isdigit():
                bump_type = 0
            bump_type = int(bump_type)
            msg = f"Please choose a number between 1 and {num_options}."

        if bump_type == exit_option:
            sys.stderr.write("Exited:\n")
            sys.exit(1)
        msg = ""
        if bump_type == custom_option:  # specify a version
            custom_valid = False
            while not custom_valid:
                print(msg)
                custom_version = input(
                    util.green("Enter a version string or type 'exit' to exit: ")
                )
                if custom_version == "exit":
                    sys.stderr.write("Exited:\n")
                    sys.exit(1)
                if not semver.Version.is_valid(custom_version):
                    msg = f"Version {custom_version} is not a valid semver string."
                elif custom_version in self.versions["pypi"]:
                    msg = f"Version {custom_version} has already been released to PyPi."
                elif custom_version in self.versions["tags"]:
                    msg = (
                        f"Version {custom_version} has already been tagged in the repo."
                    )
                else:
                    custom_valid = True
                    msg = f"Version {custom_version} is valid."
                    self.next_version = custom_version
        elif bump_type == no_tags_option:  # no tags
            self.next_version = None
        else:  # bump_type is one of the regular options
            self.next_version = str(version_options[bump_type - 1])
        print(self.next_version)
        if self.next_version:
            print(f"You bumped the version to: {self.next_version}")
        else:
            print("You chose to push with no tag or release.")

    def _set_versions(self):
        """Fetch the latest tags and PyPi versions."""
        if MOCKED:
            self.versions = MOCK_VERSIONS
        else:
            self.versions = {"pypi": self.get_pypi_versions(), "tags": self.get_tags()}

        self.latest_pypi_version = _sorted_versions(self.versions["pypi"])[-1]
        self.latest_tag_version = _sorted_versions(self.versions["tags"])[-1]
        # These should be the same, but if they're not, we'll use the highest
        self.latest_version = _sorted_versions(
            [self.latest_pypi_version, self.latest_tag_version]
        )[-1]

    def get_pypi_versions(self):
        """
        Return a list of all PyPi versions for the named package.
        """
        return _get_pypi_versions(self.pip_name)

    def get_tags(self):
        """Return a list of all tags in the repo."""
        return _sorted_versions([str(tag) for tag in self.repo.tags])

    def is_released_version(self, version):
        """Return True if the version has been released to PyPi or tagged in the repo."""
        if not semver.Version.is_valid(version):
            return None
        release_version = str(
            semver.Version.parse(version).replace(prerelease=None, build=None)
        )
        if release_version in self.versions["pypi"] + self.versions["tags"]:
            return release_version
        return None

def _pypi_to_semver(p):
    """Convert a PyPi version to a semver."""
    return p.replace("rc", "-rc.")


def _sorted_versions(versions):
    """Sort a list of versions."""
    return sorted(versions, key=functools.cmp_to_key(semver.compare))


def _read_version_file(filename):
    """Pull the version from the VERSION file."""
    version = util.first_nonblank_line(filename)
    if not version:
        sys.stderr.write(
            f"Can't get version string from the version file: {filename}. using 0.0.1\n"
        )
        return "0.0.1"
    return version if semver.Version.is_valid(version) else "0.0.1"


def _get_pypi_versions(pip_name):
    """
    Return a list of all PyPi versions for the named package.

    The package may not exist on PyPi, in which case we return an empty list. We
    don't error out, because it's perfectly valid for no package to exist. We
    can still deploy there.
    """

    # notice this command says: Install version== (i.e. it requests an invalid
    # version). It fails as intended, and the result is a message to say can't
    # find version in versions. It lists the existing versions which we split
    # and return. Check for py3 and py 27 compatible by using both pips.
    args = [
        "pip3",
        "install",
        "--index-url",
        util.PROD_PYPI_INDEX,
        f"{pip_name}==",
    ]
    output = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).communicate()
    if len(output) < 2 or "none" in output[1].decode("utf-8"):
        args = [
            "pip2.7",
            "install",
            "--index-url",
            util.PROD_PYPI_INDEX,
            f"{pip_name}==",
        ]
        output = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).communicate()
        if len(output) < 2 or "none" in output[1].decode("utf-8"):
            return []

    output = output[1]
    regex = re.compile(
        r"^.*Could not find a version.*from versions:(.*)\).*", re.DOTALL
    )
    match = regex.match(output.decode("utf-8"))
    if match:
        result = [_pypi_to_semver(v.strip()) for v in match.group(1).split(r", ")]

        return _sorted_versions([v for v in result if semver.Version.is_valid(v)])
    return []


def get_version_options(latest_version):
    """Return a list of the most likely versions to bump to
    
    See the tests for examples.
    """
    latest = semver.Version.parse(latest_version)
    if latest.prerelease:
        version_options = [
            str(latest.next_version(part="prerelease")),
            str(latest.next_version(part="patch")),
        ]
        latest = latest.replace(prerelease=None)
        version_options += [
            str(latest.next_version(part="minor").bump_prerelease()),
            str(latest.next_version(part="minor")),
            str(latest.next_version(part="major").bump_prerelease()),
            str(latest.next_version(part="major")),
        ]
    else:
        version_options = [
            str(latest.next_version(part="prerelease")),
            str(latest.next_version(part="patch")),
            str(latest.next_version(part="minor").bump_prerelease()),
            str(latest.next_version(part="minor")),
            str(latest.next_version(part="major").bump_prerelease()),
            str(latest.next_version(part="major")),
        ]
    return version_options
