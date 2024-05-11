from fastapi.requests import Request
import time
import os

def get_current_user(request: Request):
    return request.state.user_id


def current_milli_time():
    return round(time.time() * 1000)


def get_directory_in_project_root(directory):
    root_dir = os.path.abspath(os.curdir)
    temp_data_dir = os.path.join(root_dir, directory)
    return temp_data_dir


def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_folder_from_temp_data_directory(folder_name):
    temp_data_dir_name = 'temp_data'
    temp_data_dir = get_directory_in_project_root(temp_data_dir_name)
    create_directory_if_not_exists(temp_data_dir)
    folder_path = os.path.join(temp_data_dir, folder_name)
    return folder_path
