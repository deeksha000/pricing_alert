from typing import List, Dict
import uuid
from dataclasses import dataclass, field
from common.database import Database
from models.item import Item
from models.model import Model
from models.user import User
from lib.mailgun import Mailgun


@dataclass(eq=False)
class Alert(Model):
    name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)
    collection: str = field(init=False, default="alerts")

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "item_id": self.item._id,
            "price_limit": self.price_limit,
            "user_email": self.user_email

        }

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self) -> None:
        """ if self.item.price < self.price_limit:
            print(f"Item {self.item} has reached a price under {self.price_limit}. Latest price: {self.item.price}.")
        else:
            print("Item's price has not reached below the desired price")

        if self.item.load_price() < self.price_limit:
            print(f"Item{self.item} has reached a price under {self.price_limit}.Latest price is {self.item.price}.")
            Mailgun.send_mail(
                [self.user_email],
                f'Notification for {self.name}',
                f'Your alert {self.name} has reached a price under {self.price_limit}.Latest price is: {self.item.price}'
                f'Go to this address to check your item {self.item.url}.',
                f'<p> Your alert {self.name} has reached a price under {self.price_limit}.</p><p> The latest price is '
                f'{self.item.price}</p><p>Click <a href = "{self.item.url}">here</a> to purchase your item.</p>'

            )
        """
        if self.item.price < self.price_limit:
            print(
                f"Item {self.item} has reached a price under {self.price_limit}. Latest price: {self.item.price}."
            )
            Mailgun.send_mail(
                email=[self.user_email],
                subject=f"Notification for {self.name}",
                text=f"Your alert {self.name} has reached a price under {self.price_limit}. The latest price is {self.item.price}. Go to this address to check your item: {self.item.url}.",
                html=f'<p>Your alert {self.name} has reached a price under {self.price_limit}.</p><p>The latest price is {self.item.price}. Check your item out <a href="{self.item.url}>here</a>.</p>',
            )