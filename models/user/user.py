from typing import List, Dict
import uuid
from dataclasses import dataclass, field
from common.database import Database
from models.model import Model
from common.utils import Utils
import models.user.error as UserErrors


@dataclass
class User(Model):
    collection: str = field(init=False, default='users')
    email: str
    password: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    @classmethod
    def find_by_email(cls, email: str):
        try:
            return cls.find_one_by('email', email)
        except TypeError:
            raise UserErrors.UserNotFound("A user with this email was not found")

    @classmethod
    def register_user(cls, email: str, password: str) -> bool:
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("This e-mail does not exist")
        try:
            cls.find_by_email(email)
            raise UserErrors.UserAlreadyRegisteredError("The e-mail that you have entered is already registered")
        except UserErrors.UserNotFound:
            User(email, Utils.hash_password(password)).save_to_mongo()
        return True

    def json(self) -> Dict:
        return {
            '_id': self._id,
            'email': self.email,
            'password': self.password
        }
    @classmethod
    def login_valid(cls,email:str ,password : str):
        user = cls.find_by_email(email)
        if not Utils.check_hashed_password(password,user.password):
            raise UserErrors.IncorrectPasswordError("You have entered the wrong password.")
        return True