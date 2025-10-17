# Flask Microservice

This project is a simple Flask microservice that handles user registration, login, token generation, and fetching book data from a database.

## Project Structure

```
flask-microservice
├── app.py                # Main application file containing the Flask logic
├── requirements.txt      # Dependencies required for the project
├── Dockerfile            # Instructions to build a Docker image for the microservice
├── .gitignore            # Files and directories to be ignored by Git
├── templates             # Directory containing HTML templates
│   └── login.html       # Simple HTML page for user login
├── static               # Directory containing static files
│   └── books.xsl        # XSL stylesheet for transforming XML output
├── tests                # Directory containing unit tests
│   └── test_app.py      # Unit tests for the application
└── README.md            # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd flask-microservice
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   python app.py
   ```

## Usage

- Access the login page at `http://localhost:5000/login`.
- Use the form to input your username and password.
- Upon successful login, a JWT token will be displayed.

## Testing

To run the unit tests, execute the following command:
```
python -m unittest discover -s tests
```

## Docker

To build and run the Docker container, use the following commands:
```
docker build -t flask-microservice .
docker run -p 5000:5000 flask-microservice
```

## License

This project is licensed under the MIT License.