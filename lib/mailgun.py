import os
from typing import List
from requests import Response, post


class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


"""
class Mailgun:
    FROM_TITLE = 'Pricing Service'
    FROM_EMAIL = f'Do-not-reply@{MAILGUN_DOMAIN}'

    @classmethod
    def send_mail(
            cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:
        api_key = os.environ.get('MAILGUN_API_KEY', None)
        domain = os.environ.get('MAILGUN_DOMAIN', None)
        if api_key is None:
            raise MailGunException('mailgun_failed_load_api_key')

        if domain is None:
            raise MailGunException('mailgun_failed_load_domain')

        response = post(
            f'https://api.mailgun.net/v3/{domain}/messages',
            auth=('api', api_key),
            data={
                'from': f'{cls.FROM_TITLE} <{cls.FROM_EMAIL}>',
                'to': email,
                'subject': subject,
                'text': text,
                'html': html,
            },
        )
        if response.status_code != 200:
            # print(response.status_code)
            # print(response.json())
            raise MailGunException('An error occurred while sending e-mail.')
        return response
"""


class Mailgun:
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY', None)
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN', None)

    FROM_TITLE = 'Pricing Service'
    FROM_EMAIL = f'do-not-reply@{MAILGUN_DOMAIN}'

    @classmethod
    def send_mail(
            cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:
        api_key = os.environ.get('MAILGUN_API_KEY', None)
        domain = os.environ.get('MAILGUN_DOMAIN', None)
        if api_key is None:
            raise MailGunException('mailgun_failed_load_api_key')

        if domain is None:
            raise MailGunException('mailgun_failed_load_domain')
        response = post(
            f'https://api.mailgun.net/v3/{domain}/messages',
            auth=('api', api_key),
            data={
                'from': f'{cls.FROM_TITLE} <{cls.FROM_EMAIL}>',
                'to': email,
                'subject': subject,
                'text': text,
                'html': html,
            },
        )
        if response.status_code != 200:
            # print(response.status_code)
            # print(response.json())
            raise MailGunException('An error occurred while sending e-mail.')
        return response
