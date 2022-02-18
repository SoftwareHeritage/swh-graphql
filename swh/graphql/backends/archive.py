class Origin:
    def __init__(self, url, id):
        self.url = url
        self.id = id


def get_origins():
    return [
        Origin("test1.example.com", "1"),
        Origin("test2.example.com", "2"),
        Origin("test3.example.com", "3"),
        Origin("test4.example.com", "4"),
        Origin("test5.example.com", "5"),
        Origin("test6.example.com", "6"),
    ]
