import requests
from utils.tasks import GetTasks
from utils.helper import *


class Crawler:
    task_dir = ''
    #
    base_url = ''
    domain_name = ''
    pending_file = ''
    crawled_file = ''
    pending = set()
    crawled = set()

    def __init__(self, task_dir, base_url, domain_name):
        Crawler.task_dir = task_dir
        Crawler.base_url = base_url
        Crawler.domain_name = domain_name
        Crawler.pending_file = f'{Crawler.task_dir}/pending.txt'
        Crawler.crawled_file = f'{Crawler.task_dir}/crawled.txt'
        self.start()
        self.crawl('Worker 1', Crawler.base_url)

    @staticmethod
    def collect_task(url):
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
            'Referer': 'https://google.com',
        }
        try:
            response = requests.get(url, headers=headers)
            # print(response.headers)
            if 'text/html' in response.headers['Content-Type']:
                raw_bytes = response.content
                raw_response = raw_bytes.decode('utf8')
                # print(raw_response)
            task = GetTasks(Crawler.base_url, url)
            task.feed(raw_response)
        except Exception as uwu:
            print(uwu)
            return set()
        return task.page_urls()

    @staticmethod
    def add_task_pending(urls):
        for url in urls:
            if url in Crawler.pending:
                continue
            if url in Crawler.crawled:
                continue
            # makes crawler stay in the base domain only
            # if Crawler.domain_name != domain(url):
            #     continue
            Crawler.pending.add(url)

    @staticmethod
    def save_task():
        set_to_file(Crawler.pending, Crawler.pending_file)
        set_to_file(Crawler.crawled, Crawler.crawled_file)

    @staticmethod
    def start():
        create_dir(Crawler.task_dir)
        create_task(Crawler.task_dir, Crawler.base_url)
        Crawler.pending = file_to_set(Crawler.pending_file)
        Crawler.crawled = file_to_set(Crawler.crawled_file)

    @staticmethod
    def crawl(name, url):
        if url not in Crawler.crawled:
            print(f"{name} crawling {url}")
            print(
                f"Pending: {str(len(Crawler.pending))} and Crawled: {str(len(Crawler.crawled))}")
            Crawler.add_task_pending(Crawler.collect_task(url))
            Crawler.pending.remove(url)
            Crawler.crawled.add(url)
            Crawler.save_task()
