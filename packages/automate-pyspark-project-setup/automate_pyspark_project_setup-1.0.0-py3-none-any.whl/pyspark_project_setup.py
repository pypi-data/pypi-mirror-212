import click
import os
import requests

@click.command()
def init():
    main_dir = ["data", "logs", "app", "utils", "tests", "conf", "lib"]

    # iterate through the main folders and create folders one by one
    for folder in main_dir:
        try:
            os.mkdir(folder)
        except FileExistsError:
            pass

    # create main.py in the app folder
    try:
        with open("app/main.py", "w") as f:
            pass
    except FileExistsError:
        pass

    # create functions.py in the utils folder
    try:
        with open("utils/functions.py", "w") as f:
            url = "https://raw.githubusercontent.com/sagarlakshmipathy/pyspark-starter-repo/main/functions.py"
            save_path = "utils/functions.py"
            download_file(url, save_path)
    except FileExistsError:
        pass

    # create log4j.properties in the conf folder
    try:
        url = "https://raw.githubusercontent.com/sagarlakshmipathy/pyspark-starter-repo/main/log4j.properties"
        save_path = "conf/log4j.properties"
        download_file(url, save_path)
    except FileExistsError:
        pass

    # create spark.conf in the conf folder
    try:
        url = "https://raw.githubusercontent.com/sagarlakshmipathy/pyspark-starter-repo/main/spark.conf"
        save_path = "conf/spark.conf"
        download_file(url, save_path)
    except FileExistsError:
        pass

    # create test_utils.py in the tests folder
    try:
        with open("tests/test_utils.py", "w") as f:
            pass
    except FileExistsError:
        pass

    # create logger.py in the lib folder
    try:
        with open("lib/logger.py", "w") as f:
            url = "https://raw.githubusercontent.com/sagarlakshmipathy/pyspark-starter-repo/main/logger.py"
            save_path = "lib/logger.py"
            download_file(url, save_path)
    except FileExistsError:
        pass

def download_file(url, save_path):
    response = requests.get(url)

    with open(save_path, 'wb') as file:
        file.write(response.content)

if __name__ == '__main__':
    init()
