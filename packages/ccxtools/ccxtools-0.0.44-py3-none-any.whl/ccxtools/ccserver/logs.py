import requests


class Logger:
    server_url = 'http://ec2-3-38-108-243.ap-northeast-2.compute.amazonaws.com'

    # server_url = 'http://127.0.0.1:8000'

    def __init__(self, token, program):
        self.token = token
        self.program = program

    def request_post(self, url, data):
        return requests.post(url, json=data, headers={
            'Authorization': f'Token {self.token}',
            'Content-Type': 'application/json',
        })

    def log_error(self, exception, traceback):
        return self.request_post(f'{self.server_url}/logs/errors/', {
            'program': self.program,
            'exception': exception,
            'traceback': traceback,
        })
