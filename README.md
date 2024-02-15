# Attraction Voting System

This is a web application designed to allow users to vote for attractions, view their voting history, submit new attractions, and analyze voting data. The application is built using Flask, a Python web framework.

## Features

- **User Authentication**: Users can log in and out of the system using a unique user ID.
- **Attraction Voting**: Users can vote for attractions and provide comments.
- **Voting History**: Users can view their voting history, including attractions they have voted for and their comments.
- **Attraction Submission**: Users can submit new attractions to be added to the system.
- **Attraction Filtering**: Users can filter attractions by country, type, or both.
- **Data Analysis**: Users can analyze voting data to see the top attractions based on votes.

## File Structure

- **app.py**: Main Flask application file containing the server-side logic.
- **templates/**: Directory containing HTML templates for rendering web pages.
- **votes.txt**: File storing user voting history data.
- **places.txt**: File storing attraction data.

## Setup and Installation

To implement the application on a new PC/server, follow these steps:

1. **Clone the Repository**: Clone the repository to your local machine or server.

2. **Install Python**: Ensure that Python is installed on your system. If not, download and install Python from the [official Python website](https://www.python.org/).

3. **Install Required Packages**: Navigate to the project directory in your terminal or command prompt and install the required Python packages using the following command:
   ```
   pip install -r requirements.txt
   ```

4. **Run the Application**: Start the Flask application by running the following command in your terminal or command prompt:
   ```
   python app.py
   ```

5. **Access the Application**: Once the application is running, you can access it in your web browser at the following URL:
   ```
   http://localhost:5050/tourism
   ```

## Usage

Once the application is set up and running, users can perform the following actions:

1. **Log In or Create Account**: Users can log in with their user ID or create a new account if they are new to the system.

2. **Vote for Attractions**: Users can search for attractions and submit their votes along with optional comments.

3. **View Voting History**: Users can view their voting history to see attractions they've voted for and their comments.

4. **Submit New Attractions**: Users can submit new attractions to be added to the system.

5. **Analyze Voting Data**: Users can analyze voting data to see the top attractions based on votes.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request.
