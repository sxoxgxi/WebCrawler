import os
from queue import Queue
import threading

from utils.helper import *
from crawler import Crawler

# PARENT_DIR = 'D:\Projects\Side Projects\Crawler'
BASE_URL = input('Website URL to crawl: ')
DOMAIN = domain(BASE_URL)
VALUE = DOMAIN.find('.')
TASK_DIR = DOMAIN[0:VALUE]
# print(TASK_DIR)
DOMAIN_NAME = domain(BASE_URL)
PENDING_FILE = TASK_DIR + '\pending.txt'
CRAWLED_FILE = TASK_DIR + '\crawled.txt'
# print(PENDING_FILE)
WORKERS = 4  # number of threads
queue = Queue()
Crawler(TASK_DIR, BASE_URL, DOMAIN_NAME)


def work():
    while 1:
        url = queue.get()
        Crawler.crawl(threading.current_thread().name, url)
        queue.task_done()


def create_jobs():
    for link in file_to_set(PENDING_FILE):
        queue.put(link)
    queue.join()
    jobs()


def jobs():
    pending_tasks = file_to_set(PENDING_FILE)
    if len(pending_tasks) > 0:
        print(f"{len(pending_tasks)} links to be crawled")
        create_jobs()


def recruitment():
    for _ in range(WORKERS):
        master = threading.Thread(target=work)
        master.daemon = True
        master.start()


recruitment()
jobs()
