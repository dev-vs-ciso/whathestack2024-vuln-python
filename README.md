# whathestack2024-vuln-python


How to protect from secrets - local pre-commit

`pip install pre-commit --break-system-packages`

Note
If invoking pip returns “not found”, try pip3.

`pip3 install pre-commit --break-system-packages`

This will show the folder of the installation, which needs to be added to PATH, because pre-commit is a binary executable.

You can open another terminal window and type pre-commit. If pre-commit is in path, you’ll se an error message like this
An error has occurred: FatalError: git failed. Is it installed, and are you in a Git repository directory?

After this a file needs to be created in the root folder of every repository, called `.pre-commit-config.yaml` and containing the following:

'''
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0  # Specify the desired version of Gitleaks
    hooks:
      - id: gitleaks
'''

Finally, on each repository call the following command without a virtual environment:

`pre-commit install`