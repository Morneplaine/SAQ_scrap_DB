import os
import subprocess
import sys


def create_update_req_file():
    try:
        # Check if requirements.txt already exists
        if os.path.exists("requirements.txt"):
            print(
                "requirements.txt already exists. It will be updated with current dependencies."
            )
        else:
            print("Creating a new requirements.txt file.")

        # Use pip to freeze currently installed packages and write to requirements.txt
        with open("requirements.txt", "w") as file:
            subprocess.run(["pip", "freeze"], stdout=file)

        print("requirements.txt updated successfully.")

    except Exception as e:
        print(f"An error occurred while creating/updating requirements.txt: {e}")


def install_requirements():
    try:
        # Install packages listed in requirements.txt
        subprocess.run(["pip", "install", "-r", "requirements.txt"])
        print("All requirements installed successfully.")
    except Exception as e:
        print(f"An error occurred while installing requirements: {e}")


def create_virtual_env():
    print("Creating virtual environment...")
    subprocess.run(["python3", "-m", "venv", ".venv"])
    print("Virtual environment '.venv' created.")


def activate_virtual_env():
    print("Activating virtual environment...")
    if os.name == "nt":  # Windows
        activation_command = ".venv\\Scripts\\activate"
    else:  # MacOS/Linux
        activation_command = "source .venv/bin/activate"
    print(f"Run '{activation_command}' to activate the virtual environment.")


def initialize_git():
    print("Initializing Git repository...")
    subprocess.run(["git", "init"])
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Initial commit"])
    print("Git repository initialized and first commit created.")


def create_github_repo(repo_name):
    print("Creating GitHub repository...")
    subprocess.run(
        [
            "gh",
            "repo",
            "create",
            repo_name,
            "--public",
            "--source",
            ".",
            "--remote",
            "origin",
        ]
    )
    print("GitHub repository created and linked.")


def upgrade_pip():
    try:
        # Run the upgrade pip command
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True
        )
        print("pip has been upgraded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while upgrading pip: {e}")


def list_installed_packages():
    try:
        # Run the pip list command
        result = subprocess.run(
            ["pip", "list"], capture_output=True, text=True, check=True
        )

        # Print the output of pip list
        print("Installed packages:\n")
        print(result.stdout)
        choice_upd = print("do you want to update all packages? (y/n): ")
        if choice_upd == "y":
            try:
                subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "--upgrade",
                        "-r",
                        "requirements.txt",
                    ],
                    check=True,
                )
                print("All packages in requirements.txt have been upgraded.")
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while upgrading packages: {e}")
            print("All packages have been updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while listing packages: {e}")


def main():

    venv_activated = input(
        "Have you activated the virtual environment? (y/n), n will do it y will do nothing: "
    ).lower()
    if venv_activated == "n":
        project_name = input("Enter the project name: ")
        create_virtual_env()
        activate_virtual_env()
        upgrade_pip
        print(sys.prefix)
    else:
        print("check that the activation is in force:")
        print(sys.prefix)
        upgrade_pip()
        print("we just tried to upgrate pip in case ")
        list_installed_packages()

    install_choice = input(
        "have you imported a requirement file and do you want to install the requirements? (y/n): "
    ).lower()
    if install_choice == "y":
        install_requirements()
        list_installed_packages()
    requirement_choice = input(
        "Do you want to create a requirements.txt file? (y/n): "
    ).lower()
    if requirement_choice == "y":
        create_update_req_file()

    git_choice = input("Do you want to initialize a git repository? (y/n): ").lower()
    if git_choice == "y":
        initialize_git()
        project_name = input("Enter the project name: ")

        create_github_repo(project_name)


if __name__ == "__main__":
    # main()
    git_choice = input("Do you want to initialize a git repository? (y/n): ").lower()
    if git_choice == "y":
        initialize_git()
        project_name = input("Enter the project name: ")

        create_github_repo(project_name)
