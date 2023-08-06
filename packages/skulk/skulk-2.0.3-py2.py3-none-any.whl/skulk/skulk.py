#!/usr/bin/env python3

"""
Skulk.

A tool to help get your repo in good shape for a release.

It works for packages intended for PyPi.

It has 2 public functions:

1. main() : A wizard that guides you to choosing a version that does not conflict with any git tags
   or PyPi versions.

If no pre-push hook exists in the repo, skulk will prompt and help to make one.

2. run_pre_push_checks() : A function that is designed to be called from a git pre-push hook.

Assumptions: 1. You have a file named VERSION at the top level of the repo. It should contain a
simple semver such as 1.2.3 2. You have a CHANGELOG.md  at the top level of the repo.


WIZARD MESSAGES:

1. Nothing will happen until the end. You can exit at any time.
2. Do you want to simply push your code(0), deploy a pre-release(1), or deploy a release(2)?
3. If pre-release(1) or release(2):
    a. You'll be shown the current version and the latest version on PyPi.
    b. You'll be asked to choose a new version from the options.


"""

from __future__ import print_function
from builtins import input
import datetime
import os
import sys
from . import util
from .bumper import Bumper


class Skulk(object):
    """A wizard to guide the user to a good version and changelog."""

    def __init__(self):
        self.repo = util.get_repo()
        self.branch = self.repo.active_branch
        self.branch_name = self.branch.name
        self.working_dir = self.repo.working_dir
        self.hook_filename = os.path.join(self.working_dir, ".git", "hooks", "pre-push")
        self.changelog_filename = os.path.join(self.working_dir, "CHANGELOG.md")
        self.version_filename = os.path.join(self.working_dir, "VERSION")
        self.pip_name = util.get_pip_name(self.repo)
        self.bumper = None
        self.edit_changelog = False
        self.changelog_addition = ""

    def run(self):
        """
        Guide the user to ensure version and changelog are valid.
        """

        self.check_pre_push_hook()
        self.check_clean()
        self.bumper = Bumper(self.repo, self.pip_name)
        if self.ask_do_tag_release():
            self.bumper.run()

        self.ask_changelog_additions()

        # Now we do the actual work.
        # CHANGELOG
        if self.edit_changelog:
            self.resolve_changelog()

        if self.bumper.next_version:
            with open(self.version_filename, "w", encoding="utf-8") as vfn:
                vfn.write(self.bumper.next_version)

        self.commit_version_changelog()
        tag = self.add_tag()
        do_push = self.ask_push(tag)
        if do_push:
            self.push(tag)
        else:
            print("No worries. Use the following command to push later. Bye\n")
            if tag:
                print(f"git push --atomic origin {self.branch_name} {tag.name}")
            else:
                print(f"git push origin {self.branch_name}")
        sys.exit(0)

    # PRIVATE
    def ask_push(self, tag=None):
        """Ask the user if he wants to push the branch and tag."""
        if tag:
            question = f"Do you want me to push the branch and tag: {self.branch_name} + {tag.name}` for you?"
        else:
            question = f"Do you want me to push the branch: {self.branch_name} for you?"
        return util.yes_no(question)

    def push(self, tag=None):
        """Push the branch and tag."""
        origin = self.repo.remote("origin")
        if tag:
            origin.push(self.branch)
            origin.push(tag)
            print("Pushed branch and tag.\n")
        else:
            origin.push(self.branch)
            print("Pushed branch.\n")

    def add_tag(self):
        """Add a tag to the repo."""
        if self.bumper.next_version:
            label = "Pre-release" if self.bumper.is_prerelease() else "Release"
            tag = self.repo.create_tag(
                self.bumper.next_version, message=f"{label}: {self.bumper.next_version}"
            )
            print(f"Created tag: {tag.name}")
            return tag
        return None

    def commit_version_changelog(self):
        """Commit the version and changelog files."""
        if self.bumper.next_version:
            if self.repo.is_dirty():
                self.repo.index.add([self.changelog_filename, self.version_filename])
                self.repo.index.commit(
                    f"Update changelog and sets version to {self.bumper.next_version}"
                )
                print("Committed Version and Changelog\n")

        elif self.edit_changelog:
            if self.repo.is_dirty():
                self.repo.index.add([self.changelog_filename])
                self.repo.index.commit("Update changelog")
                print("Committed Changelog\n")

    def check_clean(self):
        """Check that the repo is clean and give user a chance to clean it up.

        User can continue with a dirty repo, but we at least want to warn them.
        """
        if not self.repo.is_dirty():
            print("Repo clean. Good to go.")
            return

        mods = [item.a_path for item in self.repo.index.diff(None)]
        untracked = self.repo.untracked_files
        if mods:
            print(util.magenta("Modified files:\n{}".format("\n".join(mods))))
        if untracked:
            print(util.magenta("Untracked files:\n{}".format("\n".join(untracked))))

        print(
            "----------\nAttention: Repo is dirty. Uncommitted changes won't be included. Is this ok?"
        )
        print("If you want to include them, please commit them now.")
        cont = input(
            util.green(
                "When you are happy, press enter to continue or type 'exit' to exit."
            )
        )
        if cont == "exit":
            sys.stderr.write("Exited.\n")
            sys.exit(0)

    def ask_do_tag_release(self):
        """Ask the user if he wants to make a pre-release from this branch."""
        return util.yes_no(
            "Do you want to tag and deploy from this branch?",
            "No, push only",
            "Yes, push and deploy a tagged release.",
        )

    def ask_changelog_additions(self):
        """Generate the reference additions to the changelog.

        Do not write anything to the changelog file yet."""
        stub = ""
        if self.bumper.next_version:
            self.edit_changelog = True
            date_string = datetime.date.today().strftime("%d %b %Y")
            stub = f"## Version:{self.bumper.next_version} -- {date_string}\n\n"
        else:
            self.edit_changelog = util.yes_no(
                "No version bump. Do you want to add entries in the changelog anyway?"
            )
            stub = "## Unreleased\n\n"

        if self.edit_changelog:
            terminal_advice = util.yellow(
                "Here are some recent commit message for reference:\n"
            )
            terminal_advice += "-" * 30 + "\n"

            commits = util.get_recent_commits(self.repo)
 
            commit_messages = ([f"* {c.summary} [{c.hexsha[:7]}]" for c in commits])
            terminal_advice += "\n".join(commit_messages) or ""
            terminal_advice += "\n" + ("-" * 30) + "\n"

            sections = [
                "Added",
                "Changed",
                "Deprecated",
                "Removed",
                "Fixed",
                "Security",
            ]
            terminal_advice += util.yellow(
                "You may want to use these headngs to categorize your changelog entries:\n"
            )
            terminal_advice += "".join([f"### {s}\n" for s in sections])
            terminal_advice += "-" * 30 + "\n\n"
            print(terminal_advice)

            if self.bumper.next_version or self.changelog_needs_unreleased_stub():
                self.changelog_addition = stub

    def resolve_changelog(self):
        """Help the user to get the changelog file up-to-date."""
        with open(self.changelog_filename, "r", encoding="utf-8") as clog:
            content = clog.read() or "--"

        content = self.changelog_addition + "\n\n" + content

        with open(self.changelog_filename, "w", encoding="utf-8") as clog:
            clog.write(content)

        print("Resolve CHANGELOG:")

        input(
            util.green(
                "Please EDIT and SAVE your CHANGELOG (There's no need to commit), then press enter to continue."
            )
        )

    def changelog_needs_unreleased_stub(self):
        """Return True if the changelog needs an unreleased stub."""
        with open(self.changelog_filename, "r", encoding="utf-8") as f:
            datafile = f.readlines()

        for line in datafile:
            if line.startswith("## Unreleased"):
                return False
            elif line.startswith("## Version"):
                return True
        return True



    def check_pre_push_hook(self):
        """Check if there is a legacy pre-push hook and delete it."""
        hook_detection_line = "skulk.run_pre_push_checks()"
        delete_hook = False
        if os.path.exists( self.hook_filename):
            with open( self.hook_filename, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip() == hook_detection_line:
                        delete_hook = True
        if delete_hook:
            print(f"Found legacy pre-push hook '{self.hook_filename}' - Deleting ...")
            try:
                os.unlink( self.hook_filename)
            except IOError as ex:
                print(f"Error deleting '{self.hook_filename}': {ex}")
                util.enter_to_continue_or_exit("Please delete it manually, then press enter")
def main():
    """Run the wizard."""
    wizard = Skulk()
    wizard.run()


if __name__ == "__main__":
    main()
