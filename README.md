# 445-WebApp

## Hosted
https://pac-app1.herokuapp.com/

## Development Team
    Back End- Biao Chen
    Front End- Adam Hinkle

## Requirements

- Node.js
- Python 3.7

## Run UI
```
npm install
npm install @material-ui/icons
npm install @material-ui/core
npm i firebase

```
## Setup


For Steps 1-2 you could follow this blog if you want:https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project

Step 1) Create Frontend React app (client = frontend)

Step 2) Create Flask Backend Server (server = backend)

1. Start with generating a virtual environment for our python install in **root directory**. This allows us to isolate this environment from our system. Especially useful if you need to install certain versions of packages on this project but different versions on another.

```bash
python3 -m venv [name]
python3 -m venv venv
```
or if you only have python3 installed, 
```bash
pyton -m venv [name]
python -m venv venv
```


2. To run the backend, you need to activate the python virtual environment. Make sure you are in **root folder**:

- Windows:
```bash
[name]\Scripts\activate.bat
venv\Scripts\activate.bat
```

- Linux:
```bash
source [name]/bin/activate
source venv/bin/activate
```

- MACOS:
```bash
. venv/bin/activate
```

3. Next we install our python packages from **requirements.txt**, make sure it's also in the **root folder**

```bash
pip3 install -r requirements.txt
```


## Get Ready for Testing Runing in Local Machine
- Backend:
    - Save the changes, and redeploy in heroku
    - If you made any changes to the structure of the database, or you don't have one yet,
      you need to reset/initialize the database
        - To initialize the database (for the first time):
            ```bash
            flask init-db
            ```
        - To reset the database:
            ```bash
            flask init-db --drop
            ``` 
  
- Frontend:
  - If you ever made any changes to the frontend, you will need to build the whole frontend again to reflect the change
  - In **root folder**:
  ```bash
  yarn build 
  ```
  - This will update the existing build folder with the changes you made
  

## Test Run In Local Machine
  Here is how you run the project in your local machine during development
  - In **root folder**:
    - Make sure you have a python virtual environment in **root folder**
    - Make sure the **.env** file is under the **root folder**
    - Activate your python virtual environment depending on your machine
    - Activate the backend (flask) :
    ```bash
    flask run
    ```
    - Open your browser, and enter http://127.0.0.1:5000 to access the page
    - Done
      
  - **Remainder**:
    - Everytime you want to reflect your changes when you run the application in local machine, make sure you follow the
        instructions in **Get Ready for Testing Running in Local Machine** to prepare for next run



## Flask Commands
  The are some helpful commands that can can be excuted for certain purpose
  - In order to get a list of commands that are available, run
    ```bash
    flask --help
    ```
    - Sample Output 
    ```bash
    Commands:
      add-admin
      all-admins
      remove-admin       
      routes             Show the routes for the app.
      run                Run a development server.
      shell              Run a shell in the app context.
    ```
  - The previous command does not display the full help messages, in order to get the full help message, run
    ```bash
    flask [command] --help
    ex:
    flasks remove-admin --help
    ```
    - Sample Output:
    ```bash
    Usage: flask remove-admin [OPTIONS] EMAIL

    Remove A User If The User Is An Admin__

    :param email: the email of the admin you want to remove
    ```
  - Examples:
    - Add an admin account:
    ```bash
        flask add-admin myemail@gmail.com
    ```
    
    - To remove an exising admin accout:
    ```bash
        flask remove-admin myemail@gmail.com
    ```
    
    - To display a list of all admins:
    ```bash
        flask all-admins
    ```
