from locust import HttpUser, task, events
from jsonreader import JSONReader
import os
import json
from accuracy_functions import save_to_markdown, save_to_csv, log_data, calculate_accuracy
from utils import is_host_up

@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--engine", type=str, choices=["ai-lab", "azure", "static", "llamaindex"], required=True, help="Pick a search engine.")
    parser.add_argument("--path", type=str, required=True, help="Point to the directory with files structured")
    parser.add_argument("--format", type=str, choices=["csv", "md"], default="md", help="Generate a CSV or Markdown document")
    parser.add_argument("--once", action="store_true", default=False, help="Set this flag to make the accuracy test non-repeatable.")
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        parser.error(f"The directory '{args.path}' does not exist.")

    if not is_host_up(args.host):
       parser.error(f"The backend URL '{args.host}' is either wrong or down.")

class FinesseUser(HttpUser):

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

        if self.engine in ["ai-lab", "azure", "static"]:
            question = json_data.get("question")
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
                    response_urls.append(page.get("url"))
                accuracy_result = calculate_accuracy(response_urls, expected_url)
                time_taken = response.elapsed.microseconds/1000

                expected_page = json_data.copy()
                del expected_page['question']
                del expected_page['answer']
                self.qna_results[file_name] = {
                    "question": question,
                    "expected_page": expected_page,
                    "response_pages": response_pages,
                    "position": accuracy_result.position,
                    "total_pages": accuracy_result.total_pages,
                    "accuracy": accuracy_result.score,
                    "time": time_taken,
                }

    def on_start(self):
        self.qna_reader = JSONReader(self.path)
        self.qna_results = dict()

    def on_stop(self):
        log_data(self.qna_results)
        if self.format == "md":
            save_to_markdown(self.qna_results, self.engine)
        elif self.format == "csv":
            save_to_csv(self.qna_results, self.engine)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = self.environment.parsed_options.path
        self.engine = self.environment.parsed_options.engine
        self.format = self.environment.parsed_options.format
        self.once = self.environment.parsed_options.once
