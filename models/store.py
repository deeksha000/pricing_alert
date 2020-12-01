import uuid
import re
from typing import Dict
from models.model import Model
from common.database import Database
from dataclasses import dataclass,field


@dataclass(eq=False)
class Store(Model):
    name: str
    url_prefix: str
    tag_name: str
    query: Dict
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)
    collection: str = field(init=False, default="stores")

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_name(cls, store_name: str) -> "Store":
        return cls.find_one_by("name", store_name)

    @classmethod
    def get_by_url_prefix(cls, url_prefix: str) -> "Store":
        url_regex = {"$regex": '^{}'.format(url_prefix)}
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url: str) -> "Store":
        """
        Return a store from a url like "http://www.johnlewis.com/item/sdfj4h5g4g21k.html"
        :param url: The item's URL
        :return: a Store
        """
        pattern = re.compile(r"(https?:\/\/.*?\/)")
        match = pattern.search(url)
        url_prefix = match.group(1)
        return cls.get_by_url_prefix(url_prefix)

    # https://www.johnlewis.com/2020-apple-ipad-pro-12-9-inch-a12z-bionic-ios-wi-fi-1tb/p4949115
