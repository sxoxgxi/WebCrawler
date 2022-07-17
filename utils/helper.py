import os
from urllib.parse import urlparse

# parent_dir = "D:\Projects\Side Projects\Crawler"

# domain name parsing to prevent crawler from moving out to a different domain


def domain(url: str) -> str:
    try:
        res = sub_domain(url)
        raw_output = res.split('.')
        return f"{raw_output[-2]}.{raw_output[-1]}"
    except Exception as uwu:
        return ""


def sub_domain(url: str) -> str:
    try:
        return urlparse(url).netloc
    except Exception as uwu:
        return ""


# helper functions to manage crawling
def create_dir(task_dir: str) -> None:
    if not os.path.exists(task_dir):
        print(f"{task_dir} created")
        os.makedirs(task_dir)
    else:
        print(f"{task_dir} already exists")


def write_data(path: str, data: str) -> None:
    with open(path, 'w') as file:
        file.write(data)


def create_task(task_dir: str, base_url: str) -> None:
    pending = task_dir + "\pending.txt"
    crawled = task_dir + "\crawled.txt"
    if not os.path.exists(pending):
        write_data(pending, base_url)
    if not os.path.exists(crawled):
        write_data(crawled, "")


def append_task(path: str, data: str) -> None:
    with open(path, 'a') as file:
        file.write(data, '\n')


def delete_task(file: str) -> None:
    with open(file, 'w') as file:
        print(f"Deleting task on {file}")


def file_to_set(file_name: str) -> set:
    result = set()
    with open(file_name, 'rt') as file:
        for line in file:
            data = line.strip('\n')
            result.add(data)
    return result


def set_to_file(datas: str, file: set) -> None:
    with open(file, 'w') as file:
        for data in datas:
            file.write(data + '\n')
