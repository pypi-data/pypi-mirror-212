import os
import subprocess
import argparse
from datetime import datetime as dt
# def load_python_files(directory):
#     file_paths = []
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file.endswith(".py"):
#                 file_path = os.path.join(root, file)
#                 file_paths.append(file_path)
#     return file_paths

# def execute_python_files(file_paths):
#     for file_path in file_paths:
#         subprocess.run(["python", file_path])


def load():
    return

def execute():
    return

def schedule():
    return 

def now():
    current_time = dt.now().strftime("%H:%M:%S")
    return current_time

def date():
    current_date = dt.now()
    year = current_date.year
    month = current_date.month
    day = current_date.day
    weekday = current_date.weekday()
    return 

def weekday():
    weekday = dt.now().weekday()
    return weekday
    
def datetime():
    return

def cron():
    return



def time():
    return

def interval():
    return

