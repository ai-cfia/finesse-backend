import requests
from locust import HttpUser, task, events
from jsonreader import JSONReader
import os
import json
from collections import namedtuple


def is_host_up(host_url: str) -> bool:
    health_check_endpoint = f"{host_url}/health"
    try:
        response = requests.get(health_check_endpoint)
        return response.status_code == 200
    except requests.RequestException:
        return False

@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--engine", type=str, choices=["ai-lab", "azure", "static"], required=True, help="Pick a search engine.")
    parser.add_argument("--path", type=str, required=True, help="Point to the directory with files structured")
    parser.add_argument("--format", type=str, choices=["csv", "md"], default="md", help="Generate a CSV or Markdown document")
    parser.add_argument("--once", action="store_true", default=False, help="Set this flag to make the accuracy test non-repeatable.")
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        parser.error(f"The directory '{args.path}' does not exist.")

    if not is_host_up(args.host):
       parser.error(f"The backend URL '{args.host}' is either wrong or down.")

class FinesseUser(HttpUser):

    AccuracyResult = namedtuple("AccuracyResult", ["position", "total_pages", "score"])

    @task()
    def search_accuracy(self):
        try:
            json_data = next(self.qna_reader)
        except StopIteration:
            if not self.once:
                # Reset variables
                self.on_start()
                json_data = next(self.qna_reader)
                print("Restarting the running test")
            else:
                print("Stopping the running test")
                self.environment.runner.quit()

        question = json_data.get("question")
        expected_page = json_data.copy()
        del expected_page['question']
        del expected_page['answer']
        expected_url = json_data.get("url")
        file_name = self.qna_reader.file_name
        search_url = f"{self.host}/search/{self.engine}"
        data = json.dumps({'query': f'{question}'})
        headers = { "Content-Type": "application/json" }
        response_urls : list[str] = []

        response = self.client.post(search_url, data=data, headers=headers)
        if response.status_code == 200:
            response_pages = response.json()
            for page in response_pages:
                del page['content']
                response_urls.append(page.get("url"))
            accuracy_result = self.calculate_accuracy(response_urls, expected_url)
            time_taken = response.elapsed.microseconds/1000
            self.qna_results[file_name] = {
                "question": question,
                "expected_page": expected_page,
                "response_pages": response_pages,
                "position": accuracy_result.position,
                "total_pages": accuracy_result.total_pages,
                "accuracy": accuracy_result.score,
                "time": time_taken,
            }

    def calculate_accuracy(self, responses_url: list[str], expected_url: str) -> AccuracyResult:
        position: int = 0
        total_pages: int = len(responses_url)
        score: float = 0.0

        if expected_url in responses_url:
            position = responses_url.index(expected_url)
            score = 1 - (position / total_pages)

        return self.AccuracyResult(position, total_pages, score)

    def log_data(self):
        for key, value in self.qna_results.items():
            print("File:", key)
            print("Question:", value.get("question"))
            print(f'Accuracy Score: {value.get("accuracy")}%')
            print(f'Time: {value.get("time")}ms')
            print()

    def on_start(self):
        self.qna_reader = JSONReader(self.path)
        self.qna_results = dict()

    def on_stop(self):
        self.log_data()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = self.environment.parsed_options.path
        self.engine = self.environment.parsed_options.engine
        self.format = self.environment.parsed_options.format
        self.once = self.environment.parsed_options.once
