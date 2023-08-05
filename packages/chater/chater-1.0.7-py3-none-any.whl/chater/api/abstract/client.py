from requests import Session, Response


class HttpClient:
    def __init__(self):
        self.session = Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        })

    def get(self, url: str, **kwargs) -> Response:
        return self.session.get(url, **kwargs)

    def post(self, url: str, **kwargs) -> Response:
        return self.session.post(url, **kwargs)
