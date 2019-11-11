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

## 11/11/2019 - Finishing touches
* Implemented challenge/try-it-yourself feature 14-1: the ability to press P to play.
* Implemented challenge/try-it-yourself feature 14-5: persistent high scores
* Fixed 'pygame has no member attribute' errors in pylint by adding the following to VSCode's `settings.json`:
    ```
    "python.linting.pylintArgs": [
        "--extension-pkg-whitelist=pygame"
    ]
    ```
    * Solution was found here: https://stackoverflow.com/questions/50569453/why-does-it-say-that-module-pygame-has-no-init-member
    * This seems to have fixed other issues with pylint I was unaware of, as pylint has found new issues for me to fix.
* Completed challenge/try-it-yourself feature 14-7: code refactoring.
* Tweaked the scoreboard to have labels, and to render fonts with a transparent background.
    * I made the font render with a transparent background by ommitting the last argument to `pygame.font.render`:
    ```
    # Non-transparent background
    self.high_score_image = self.font.render(score_str, True, self.text_color,
                                                 self.settings.bg_color)
    # Transparent background
    self.high_score_image = self.font.render(score_str, True, self.text_color)
    ```

## Next steps:
* Customize the game to match retro Space Invaders look'n'feel.