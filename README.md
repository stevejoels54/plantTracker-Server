# plantTracker/README.md

# plantTracker

plantTracker Django Server is the backend server for the plantTracker mobile app. It is built using Django, a popular Python web framework, and is responsible for storing and retrieving data from the sensors connected to the Arduino-based hardware setup in real-time.

## Installation

### Prerequisites

- Python (version 3.6 or higher) installed on your system.
- pip package manager installed.

### Clone the Repository

    git clone

    cd plantTracker

### Create and Activate Virtual Environment

        python3 -m venv venv
        source venv/bin/activate

### Install Dependencies

        pip install -r requirements.txt

### Database Configuration

```python
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_username',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

```

### Run Migrations

    python manage.py migrate

This will create the necessary database tables for the server to store data.

### Run the Server

    python manage.py runserver

This will start the Django development server, and the server will be accessible at http://localhost:8000/ in your web browser.

## Contributing

Contributions to plantTracker Django Server are welcome! If you would like to contribute, please follow the guidelines in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is released under the MIT license.

## Documentation

For more information about the project, including API documentation, customization options, and additional features, please refer to the project documentation in at [https://techmasterevent.com/project/planttracker]

## Support

If you have any questions or need further assistance with plantTracker Django Server, please feel free to [open an issue]
