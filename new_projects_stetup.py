import os
import subprocess

def create_virtual_env():
    print("Creating virtual environment...")
    subprocess.run(["python3", "-m", "venv", ".venv"])
    print("Virtual environment '.venv' created.")

def activate_virtual_env():
    print("Activating virtual environment...")
    if os.name == 'nt':  # Windows
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
    subprocess.run(["gh", "repo", "create", repo_name, "--public", "--source", ".", "--remote", "origin"])
    print("GitHub repository created and linked.")

def main():
    project_name = input("Enter the project name: ")
    create_virtual_env()
    activate_virtual_env()
    initialize_git()

    # Ask if the user wants to create a GitHub repo
    if input("Do you want to create a GitHub repository? (y/n): ").lower() == 'y':
        create_github_repo(project_name)

if __name__ == "__main__":
    main()
