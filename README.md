# Travel Record Keeping System Project

This project is a Flask-based web application that allows users to record and maintain travel expenses funded by the firm, and generate an accounting summary at the end of each month. It provides CRUD (Create, Read, Update, Delete) functionalities for managing the travel records in a database. The project is built using the Flask web framework and MySQL-connnector, an MySQL library for Python.

## Installation

To install and run the project, follow these steps:

1. Clone the repository to your local machine:

2. Navigate to the project directory:

``` 
cd Travel-Record-Keeping-System
```

3. Create a virtual environment and activate it:

```
python -m venv venv
source venv/bin/activate
```


4. Install the project dependencies:

``` 
pip install flask 
pip install mysql-connector
pip install mysql-connector-python
pip install mysql-connector-python-rf

```


5. Start the development server:

``` 
flask --app travel_sys init-db
flask --app travel_sys run --debug
```


You should now be able to access the application at `http://localhost:5000` in your web browser.