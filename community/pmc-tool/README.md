# Community health monitor for the PMC

This is a project developed as part of Google Summer of Code 2023. See the [proposal document](https://docs.google.com/document/d/1v6JCx5QWhod5Z1Q3S6CfRCDeWqkNR6RUeiQ25-vUR6w/edit?usp=sharing). The project started being developed by @AibekYrysbekov , with mentorship from @aijamalnk and @pabloem.

## GitHub Data Analysis Tool

The GitHub Data Analysis Tool is a Django web application designed to help users analyze and visualize GitHub data, such as pull requests and issues. This tool allows users to extract valuable insights from their GitHub repositories by providing various features to retrieve, process, and display repository data.

## Features

1. Data Retrieval: The application connects to the GitHub API to fetch information about pull requests and issues from a specified repository.
2. Data Storage: Fetched data is stored in a SQLite database, allowing for efficient data management and retrieval.
3. Data Visualization: Users can view the data through an intuitive web interface. The tool offers visualizations such as lists of pull requests, issues, authors, and more.
4. Date Filtering: Users can select a date range to filter the data, enabling analysis of activities within specific time periods.
5. New Authors: The tool identifies and displays new authors who made their first pull request or issue during the selected date range.
6. Data Update: The application provides a feature to update data from the GitHub repository, ensuring that the analysis is always based on the latest information.

## How It's Useful

1. The GitHub Data Analysis Tool is particularly useful for open-source project maintainers, development teams, and GitHub repository owners. It offers the following benefits:
2. Insightful Analysis: With the ability to visualize pull requests and issues, repository owners can gain insights into development trends, identifying busy periods, peak contributors, and more.
3. New Contributors Tracking: The "New Authors" feature helps identify and recognize new contributors who have recently joined the project, encouraging community engagement.
4. Performance Evaluation: Teams can evaluate their productivity by analyzing their performance in terms of completed pull requests and resolved issues.
5. Data-Driven Decision-Making: By analyzing data from different time periods, the tool assists in data-driven decision-making, resource allocation, and project planning.
6. Monitoring and Maintenance: The tool supports tracking changes over time, making it easier to monitor the health and maintenance of a GitHub repository.

How to Use

1. Create a file named token.txt in the same directory as the script. Inside the token.txt file, save your personal access token for the GitHub API.

2. Install the required dependencies. The code relies on the requests and sqlite3 modules. You can install them using the following command:

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


