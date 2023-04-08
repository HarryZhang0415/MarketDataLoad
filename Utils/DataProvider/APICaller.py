import threading
import requests
import time


class APICaller:
    def __init__(self, max_retries=3, timeout=5, limit_per_minute=700):
        self.max_retries = max_retries
        self.timeout = timeout
        self.calls_per_minute = 0
        self.last_call_time = time.time()
        self.limit_per_minute = limit_per_minute

    def _call_api(self, url):
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling API: {e}")
            return None

    def _call_api_with_retry(self, url):
        num_retries = 0
        while num_retries < self.max_retries:
            result = self._call_api(url)
            if result:
                return result
            else:
                num_retries += 1

        print(f"Failed to call API after {self.max_retries} retries.")
        return None

    def throttle(self, limit_per_minute):
        self.calls_per_minute += 1
        elapsed_time = time.time() - self.last_call_time
        if elapsed_time < 60:
            if self.calls_per_minute > limit_per_minute:
                sleep_time = 60 - elapsed_time
                print(f"API call limit exceeded, sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
                self.calls_per_minute = 1
        else:
            self.calls_per_minute = 1
        self.last_call_time = time.time()

    def call_api_in_parallel(self, urls, ):
        results = []
        threads = []

        for url in urls:
            t = threading.Thread(target=lambda: results.append(self._call_api_with_retry(url)))
            t.start()
            self.throttle(self.limit_per_minute)  # throttle after each API call

        t.join()
            
        return results