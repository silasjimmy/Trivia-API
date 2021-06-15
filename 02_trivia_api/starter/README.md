# Full stack Udacitrivia web app

Udacitrivia is a platform made to hold trivial subjects and play word games.

## Getting started

### Installing dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **NPM** - This project uses NPM to manage software dependencies. From the frontend directory in the terminal, run:
```bash
npm install
```

3. **PIP** - In the terminal/cmd, naviagte to the `/backend` directory and run:
```bash
pip install -r requirements.txt
```
to install all of the required packages in the `requirements.txt` file.

## Backend setup

### Database

With Postgres installed and running:
- Make sure to create a database and name it `trivia`
- From the backend folder in the terminal run:
```bash
psql trivia < trivia.psql
```
to restore a database.

### Running the server

Still within the `/backend` directory from the terminal, run:
```bash
FLASK_APP=flaskr FLASK_DEBUG=True flask run
```

## Frontend setup

The frontend app is built using React. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

## URLs

- Backend Base URL: http://127.0.0.1:5000/
- Frontend Base URL: http://127.0.0.1:3000/

## API

The app uses the Trivia API for the backend. You can read more about the API in the README located at the `/backend` folder

## Deployment

The app can only be used locally for now.

## Authors
- Silas Jimmy: Implementation of the backend code

## Acknowledgments
- Udacity: For the boilerplate code
