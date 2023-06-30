# Notify

This repository contains a web application built using Flask that predicts and sends messages to women about their period dates. The application utilizes the Twilio API for sending Whatsapp messages and includes authentication functionality to ensure privacy and security.

## Features

- Predicts period dates based on user input
- Sends Whatsapp messages to users as reminders about their upcoming periods
- User authentication for secure access to personal information
- Responsive web design for seamless usage on different devices
- Integration with the Twilio API for Whatsapp messaging

## Installation

To set up the Period Tracker website locally, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/DanielDominicSavioKennedy/notify.git
   ```

2. Change into the project directory:

   ```bash
   cd notify
   ```

3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - **Windows**:

     ```bash
     venv\Scripts\activate
     ```

   - **Unix or Linux**:

     ```bash
     source venv/bin/activate
     ```

5. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Set up the Twilio API:

   - Sign up for a Twilio account at [https://www.twilio.com](https://www.twilio.com) if you don't have one already.
   - Obtain your Twilio Account SID and Auth Token from the Twilio console.
   - Update the configuration with your Twilio Account SID and Auth Token.

7. Run the Flask application:

   ```bash
   flask run
   ```

8. Open your web browser and navigate to `http://localhost:5000` to access the application.

## Usage

1. Open the web application in your browser by visiting `http://localhost:5000`.

2. If you are a new user, click on the "Register" link to create an account. Provide the required information and submit the form.

3. If you are an existing user, click on the "Login" link and enter your credentials to access your account.

4. Once logged in, you will be able to enter your period start dates and track your cycle. The application will predict your future period dates based on your input.

5. If you have configured your Twilio API settings correctly, you will receive Whatsapp reminders about your upcoming periods.

## Customization

You can customize the behavior of the application by modifying the following files:

- `app.py`: This file contains the Flask application logic. You can modify the routes, add new features, or change the behavior to suit your requirements.

- `templates/`: This directory contains the HTML templates used for rendering the web pages. You can modify these templates to customize the look and feel of the application.


## Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. Make sure to follow the existing coding style and guidelines.


## Acknowledgments

- This project utilizes the Flask web framework, which provides a flexible and powerful environment for building web applications in Python.

- The Twilio API is used for sending Whatsapp messages. We appreciate Twilio's services for enabling seamless communication within the application.
