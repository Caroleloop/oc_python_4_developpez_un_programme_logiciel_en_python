
# Tournament Management System

This project implements a tournament management system, allowing you to manage tournaments, players, rounds and scores. It is designed for use in chess tournaments.


## Requirements

Before running the program, please ensure that the following prerequisites are installed:

- **Python 3.7+**: Make sure Python is installed on your machine. You can check your Python version by running the following command in your terminal:
  ```bash
  python --version
  ```


## ERunning the program

### Start program

1. **Connect this repository** to your local machine:
   ```bash
   git clone https://github.com/Caroleloop/oc_python_4_developpez_un_programme_logiciel_en_python.git
   cd tournament-management
   ```


2. **Create a virtual environment**

+ Go to the current folder

+ Create your virtual environment

        ```bash            
        python -m venv <your-virtual-env-name>
	   ```         


3. **Activate virtual environment**

        ```bash           
        <your-virtual-env-name>\Scripts\activate.bat (sous Windows)
         ```          
	or
        ```bash            
        source <your-virtual-env-name>/bin/activate (sous Mac/Linux)
        ```          


4. **Package installation**  Install the necessary libraries by running:

        ```bash            
        pip install -r requirements.txt
        ```            
 The `requirements.txt` file should contain the libraries required for your project (e.g. Flask, etc.).

5. **Run the program** using Python:
   ```bash
   python main.py
   ```

   The program starts up and presents you with a menu where you can choose various actions, such as creating a tournament, adding players and so on.
   

### Project structure

Here is an overview of the project structure:

```
tournament-management/
│
├── controllers/ 			# Contains the tournament logic control files.
├── models/					# Contains data models (Tournament, Player, etc.)
├── views/ 					# Contains views for user display
├── utils/ 					# Contains utility functions
├── main.py 				# Main file for executing the program
├── requirements.txt 		# Dependency file for installing the necessary packages
└── README.md 				# Documentation for this project
```

## Application

1. **Manage players**: You can add, modify and remove players from the tournament.
2. **Create a tournament**: When running the program, you will be prompted to enter the tournament name, location, start date and other information. You can also add players to the tournament.
3. **Manage rounds**: The system creates rounds and lets you update match scores.
4. **View tournament details**: You can view information on all tournaments, including players, rounds and match results.

### Main controls
Here is a list of the main actions you can perform in the program menu:

1. Create a new tournament
2. Add players to a tournament
3. Remove players from a tournament
4. Create a new round
5. Update match scores
6. Modify a tournament
7. Delete tournament
8. Display information on all tournaments
9. Exit program

## Generate a `flake8` report in HTML format

To guarantee code quality, you can use **Flake8** to analyze the code and generate a report in HTML format.

### Steps to generate a `flake8` report :

1. **Install `flake8-html`** to generate HTML reports:
   ```bash
   pip install flake8-html
   ```

2. **Run `flake8`** on your project with the option to generate an HTML report :
   ```bash
   flake8 --output-file=flake8-report.html --format=html
   ```

   This generates a `flake8-report.html` file in the current directory with details of any code style errors detected.

3. **View HTML report**:
   Open the `flake8-report.html` file in your browser to see the results of the analysis.
   
   
   
## Auteurs

* **Carole Roch** _alias_ [@Caroleloop](https://github.com/Caroleloop)