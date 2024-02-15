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

1. Clone the repository to your local machine.
2. Install Python if not already installed.
3. Install the required Python packages using `pip install -r requirements.txt`.
4. Run the Flask application using `python app.py`.
5. Access the application in your web browser at `http://localhost:5050/tourism`.

## Usage

1. Log in with your user ID or create a new account.
2. Vote for attractions by searching for them and submitting your vote.
3. View your voting history to see attractions you've voted for.
4. Submit new attractions to be added to the system.
5. Analyze voting data to see the top attractions.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request.
