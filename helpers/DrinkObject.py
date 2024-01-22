from dataclasses import dataclass


@dataclass
class Drink:
    href: str
    name: str
    producer: int
    description: str = " "
    image_url: str = ""

    def __iter__(self):
        yield "href", self.href
        yield "name", self.name
        yield "producer", self.producer
        yield "description", self.description
        yield "image_url", self.image_url
