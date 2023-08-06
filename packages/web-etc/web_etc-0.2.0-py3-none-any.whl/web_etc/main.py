from fastapi import FastAPI, Request, Form, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException
from dotenv import dotenv_values, load_dotenv
import logging
import json
import pkg_resources
import os
import pam

# Load environment variables from .env file
load_dotenv()

# Get the directory to scan from the MY_APP_DIR environment variable,
# defaulting to /usr/local/etc if the variable is not set
dir = os.getenv("MY_APP_DIR", "/usr/local/etc")

HOME_DIR = os.path.expanduser("~")
CACHE_DIR = os.path.join(HOME_DIR, ".cache", "web_etc")
ORIGINAL_VALUES_LOG_PATH = os.path.join(CACHE_DIR, 'original_values_log.json')

# You may want to create the directory if it does not exist
os.makedirs(CACHE_DIR, exist_ok=True)

app = FastAPI()
# Specify the directory where the Jinja2 templates are located
templates_dir = pkg_resources.resource_filename('web_etc', 'templates')
templates = Jinja2Templates(directory=templates_dir)
print(templates)



security = HTTPBasic()

@app.middleware("http")
async def debug_middleware(request: Request, call_next):
    print(request.cookies)
    response = await call_next(request)
    return response

async def get_current_user(request: Request):
    print(request)
    print("+++++++++")
    session_token = request.cookies.get("session")
    print(session_token)
    print("==================")
    return session_token
    # return "TEST"

def authenticate(username: str, password: str):
    # If the TESTING environment variable is set, bypass authentication
    if os.getenv("TESTING"):
        return True

    logger.debug(f"Authenticating user: {username}")
    p = pam.pam()
    authenticated = p.authenticate(username, password)
    if authenticated:
        logger.debug(f"User {username} authenticated successfully.")
        return True
    else:
        logger.warning(f"Failed to authenticate user: {username}")
        return False



@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    logger.debug(f"Login attempt with username: {username}")
    user = authenticate(username, password)
    if not user:
        logger.warning(f"Incorrect username or password for username: {username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    logger.debug(f"Successful login for username: {username}. Setting session cookie.")
    session_token = "sessiontoken" # nosec
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="session", value=session_token, httponly=True)
    return response



@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, current_user: str = Depends(get_current_user)):
    if current_user:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
async def read_env(request: Request, search: str = "", current_user: str = Depends(get_current_user)):
    print(current_user)
    print("------------")
    if not current_user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    """Return a list of environment variables in .env and .json files in the specified directory."""

    # Dictionary to store file paths and their environment variables
    files_dict = {}

    # Recursively scan the directory
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.env'):
                env_path = os.path.join(root, file)
                # Get a dictionary of the environment variables in the .env file
                env_dict = dotenv_values(env_path)
                files_dict[env_path] = env_dict
            elif file.endswith('.json'):
                json_path = os.path.join(root, file)
                with open(json_path, 'r') as json_file:
                    # Load the JSON file into a dictionary
                    json_dict = json.load(json_file)
                files_dict[json_path] = json_dict

    # If a search term is provided, filter the environment variables
    if search:
        files_dict = {
            file_path: {key: value for key, value in env_dict.items() if search.lower() in key.lower() or search.lower() in value.lower()}
            for file_path, env_dict in files_dict.items()
        }

    # Return a TemplateResponse with the request and environment variables
    return templates.TemplateResponse("index.html", {"request": request, "files_dict": files_dict})

# Create a logger object
logger = logging.getLogger("web-etc")
logger.setLevel(logging.DEBUG)

# Create a file handler
handler = logging.FileHandler("web-etc.log")
handler.setLevel(logging.DEBUG)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(handler)

@app.post("/update", response_class=HTMLResponse)
async def update_env(request: Request):
    form_data = await request.form()
    file_path = form_data.get('file_path')
    key = form_data.get('key')
    value = form_data.get('value')

    # Load the original values log or create a new one if it doesn't exist
    try:
        with open(ORIGINAL_VALUES_LOG_PATH, 'r') as log_file:
            original_values_log = json.load(log_file)
    except FileNotFoundError:
        original_values_log = {}

    logger.debug(f"Received form data: file_path={file_path}, key={key}, value={value}")

    try:
        # If the file is a .env file
        if file_path.endswith('.env'):
            # Open the file and read all the lines
            with open(file_path, 'r') as file:
                lines = file.readlines()
            # Open the file again to write the updated lines
            with open(file_path, 'w') as file:
                for line in lines:
                    # If the line starts with the environment variable key, replace the line with the updated value
                    if line.startswith(key + '='):
                        # Log the original value if it's not already logged
                        if key not in original_values_log:
                            original_values_log[key] = line[len(key + '='):].strip()
                        file.write(key + '=' + value + '\n')
                    else:
                        file.write(line)
        # If the file is a .json file
        elif file_path.endswith('.json'):
            # Open the file and load the JSON into a dictionary
            with open(file_path, 'r') as json_file:
                json_dict = json.load(json_file)
            # Update the value of the environment variable in the dictionary
            json_dict[key] = value
            # Log the original value if it's not already logged
            if key not in original_values_log:
                original_values_log[key] = json_dict[key]
            # Open the file again to write the updated JSON
            with open(file_path, 'w') as json_file:
                json.dump(json_dict, json_file)

        # Write the updated original values log to the file
        with open(ORIGINAL_VALUES_LOG_PATH, 'w') as log_file:
            json.dump(original_values_log, log_file)

        # Return the updated list of environment variables
        return await read_env(request)
    except Exception as e:
        logger.error(f"Error updating env: {e}")
        raise

@app.get("/reset_defaults", response_class=HTMLResponse)
async def reset_defaults(request: Request):
    """Reset all environment variables to their original values using the log."""

    # Load the original values log
    try:
        with open(ORIGINAL_VALUES_LOG_PATH, 'r') as log_file:
            original_values_log = json.load(log_file)
    except FileNotFoundError:
        logger.error(f"Original values log file not found at {ORIGINAL_VALUES_LOG_PATH}")
        raise

    logger.debug(f"Resetting all environment variables to their original values")

    try:
        # Recursively scan the directory
        for root, dirs, files in os.walk(dir):
            for file in files:
                file_path = os.path.join(root, file)
                # If the file is a .env file
                if file.endswith('.env'):
                    # Open the file and read all the lines
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                    # Open the file again to write the updated lines
                    with open(file_path, 'w') as file:
                        for line in lines:
                            # If the line starts with an environment variable key that is in the log, replace the line with the original value
                            for key, original_value in original_values_log.items():
                                if line.startswith(key + '='):
                                    file.write(key + '=' + original_value + '\n')
                                else:
                                    file.write(line)
                # If the file is a .json file
                elif file.endswith('.json'):
                    # Open the file and load the JSON into a dictionary
                    with open(file_path, 'r') as json_file:
                        json_dict = json.load(json_file)
                    # Restore the original value of each environment variable that is in the log
                    for key, original_value in original_values_log.items():
                        if key in json_dict:
                            json_dict[key] = original_value
                    # Open the file again to write the updated JSON
                    with open(file_path, 'w') as json_file:
                        json.dump(json_dict, json_file)

        # Return the updated list of environment variables
        return await read_env(request)
    except Exception as e:
        logger.error(f"Error resetting env variables to default: {e}")
        raise
