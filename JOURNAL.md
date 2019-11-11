# IT-229-A Project 1 Journal

## 11/3/2019 - Project Initialization
To begin this project, I started by:
* Creating this journal
* Defining python module requirements in `requirements.txt`
    * The only require python module as of now is `pygame`
* Creating a python virtual environment with the commmand `python -m venv ai_venv`
    * From now on, work on this project (including module installation) will take place within this "venv".
    * To activate (on Windows): `.\ai_venv\Scripts\activate`
    * To deactivate: `deactivate`
* Installing the required packages by running `pip -r requirements.txt`
* Completed the project steps in chapter 12
    * A few minor changes where made, but the code mostly follows what is laid out in the book.
* Created a .gitignore file to exclude non-project files
* Created a README.md file for the project
* Create a git repository for the project and pushed it to GitHub

## 11/9/2019 - Aliens!
* Implemented aliens in the game as detailed in chapter 13
* Ran into a new issue: pylint is giving errors about pygame not existing in my IDE. Unsure how to fix this at this time.
* Also implemented play button and dynamic difficulty scaling as detailed in chapter 14.

## 11/10/2019 - Scoring
* Implemented scoreboard and remaining ships diplay functionality as detailed in chapter 14.
* Issues with pylint persist - still need to get around to fixing that.

## Next steps:
* Return to the book and implement challenge (try-it-yourself) features
* Refactor code where appropriate
* Customize the game to match retro space invades look'n'feel.