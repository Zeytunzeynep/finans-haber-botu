from dataclasses import dataclass


@dataclass
class News:  # bu sınıf haberin sistemdeki kimliğidir
    title: str
    content: str
    source: str
    url: str
    author: str = "Bilinmiyor"
