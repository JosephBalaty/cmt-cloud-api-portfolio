
# Course Management Tool Online Portfolio
Course Management Tool for course management in schools.


## How to use (PowerShell)
From the root directory, run './src/setup_cmt.ps1'.\
Run 'flask --app ./src/cmt_app run'.

setup_cmt.ps1 will instantiate a new virtual environment, install needed dependencies (excluding Python version), and activate the environment.\
-Delete will delete the current venv when set to $true.\
-Create will create and instantiate a new environment ready for testing when set to $true.\
Both parameters are, by default, set to $true.


## Technologies
Uses Flask to run the application. Python, 0Auth for authentication services, and Google's Datastore for data persistence.

Python version: 3.12.1

## Additional Information
Info on data entites (including relationship types, and description of attributes) can be found in 'model_documentation.docx' from the root directory. Program uses the MIT License.
