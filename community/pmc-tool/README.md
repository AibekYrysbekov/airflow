Saving Pull Request Data to SQLite Database

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
