# Task: Readme Example Verification
You are provided with a Flask-based project.
Use .venv as environment
Follow `README.md` to test all code examples. 
Verify the conttent of readme actually run as documented.
Identify all mismatches between documentation and actual implementation.
Generate `corrected_readme.md` with working examples.
Print all discovered defects to `defects.txt` with error traces.

## Goals
- Validate that onboarding instructions succeed as written.
- Run every detail and confirm the behavior matches the documentation.
- Capture failing commands with full error traces.
- Provide test cases to judge if function works

## Expected Output

1. `defects.txt` - List of all bugs found with with reproduction steps and error traces.
2. `corrected_readme.md` - Fixed version of the readme with working commands and code.
3. `requirements.txt` - Add required the libraries based on the .venv
4. `setup.sh` - Bash file to setup the environment
5. `test_files` - Test files to see if evertthing goes well
6. `run_tests.sh` - Test command to run testcases with pytest, all test should be passed


