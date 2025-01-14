# Community health monitor for the PMC

This is a project developed as part of Google Summer of Code 2023. See the [proposal document](https://docs.google.com/document/d/1v6JCx5QWhod5Z1Q3S6CfRCDeWqkNR6RUeiQ25-vUR6w/edit?usp=sharing). The project started being developed by @AibekYrysbekov , with mentorship from @aijamalnk and @pabloem.

The objective is to develop a tool that can be used to analyze information about an open source community. It queries information from the GitHub API and generates reports on the latest state of the community.


## Saving Pull Request Data to SQLite Database

This code is designed to fetch a list of pull requests from a specified GitHub repository and save the obtained data to a SQLite database. It also demonstrates an example of utilizing the saved data by printing it to the console.

How to Use

1. Create a file named token.txt in the same directory as the script. Inside the token.txt file, save your personal access token for the GitHub API.

2.Install the required dependencies. The code relies on the requests and sqlite3 modules. You can install them using the following command:

    pip install requests sqlite3

3. Specify the repository owner and repository name in the owner and repo variables, respectively. This allows the code to fetch pull request data from the desired repository.

4. Run the code. It will make requests to the GitHub API, fetch the pull request data from the specified repository, and save it to a SQLite database. A file named pull_requests.db will be       created, containing a table named pull_requests with columns for author (the pull request author) and count (the number of pull requests).

5. After saving the data to the database, the code will retrieve the information from the pull_requests table and print the author and pull request count to the console.

Important

  Ensure that you have the necessary permissions and access rights to use the GitHub API.
  Verify the correct installation of dependencies and the availability of the required modules before running the code.
  Make sure the token.txt file contains a valid access token for the GitHub API.
  If everything is set up correctly, the code will fetch and store pull request data in the SQLite database. Then, it will print information about each author and their corresponding pull request count to the console.


 # Running the Django Application
Follow these instructions to run the Django application:

## Prerequisites
Before running the application, make sure you have the following components installed:

Python (version 3.7 or above)

## Installing Dependencies

1. Open the terminal and navigate to the root directory of the project.
2. Install the required dependencies by running the following command:

     pip install -r requirements.txt

## Configuring the Database
1. In the settings.py file, ensure that the database settings match your configuration. By default, SQLite is used as the database.
2. Run the migrations to create the necessary database tables:
  "pullRequests", "issues"

     python manage.py migrate

## Starting the Development Server
1. In the terminal, run the following command to start the Django development server:

     python manage.py runserver

3. After starting the server, open a web browser and navigate to http://localhost:8000/ to see your application.


