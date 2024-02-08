import requests
from locust import HttpUser, task, events
from jsonreader import JSONReader
import os
import json

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
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        parser.error(f"The directory '{args.path}' does not exist.")

    if not is_host_up(args.host):
       parser.error(f"The backend URL '{args.host}' is either wrong or not up.")

class FinesseUser(HttpUser):
    @task
    def search_accuracy(self):
        # Reset the JSON itterator at the end of the itteration
        try:
            question_data = next(self.qna_reader)
        except StopIteration:
            self.qna_reader = JSONReader(self.path)
            question_data = next(self.qna_reader)
            print("Restarting test")

        question = question_data.get("question")
        expected_page_title = question_data.get("title")

        search_url = f"{self.host}/search/{self.engine}"
        data = {'query': f'{question}'}

        # Headers
        headers = {'Content-Type': 'application/json'}

        response = self.client.post(search_url, params={"query": question}, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            response_pages = response.json()
            print(response_pages)

            #accuracy = self.calculate_accuracy(response, expected_page_title)
            #print(f"The accuracy of the question: {question} is {accuracy}%")

    def on_start(self):
        self.qna_reader = JSONReader(self.path)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = self.environment.parsed_options.path
        self.engine = self.environment.parsed_options.engine
        self.format = self.environment.parsed_options.format

    def calculate_accuracy(self, response_pages: dict, expected_title: str) -> float:
        response_titles: list[str] = [page.get("title") for page in response_pages]
        if expected_title in response_titles:
            index = response_titles.index(expected_title)
            accuracy = 100 - (index / len(response_titles)) * 100
        else:
            accuracy = 0
        return accuracy
