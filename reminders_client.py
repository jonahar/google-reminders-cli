import reminders_client_utils as client_utils
from reminder import Reminder

URIs = {
    'create': 'https://reminders-pa.clients6.google.com/v1internalOP/reminders/create',
}

HEADERS = {
    'content-type': 'application/json+protobuf',
}

HTTP_OK = 200


class RemindersClient:
    def __init__(self):
        self.auth_http = client_utils.authenticate()

    def create_reminder(self, reminder: Reminder) -> bool:
        """
        send a 'create reminder' request.
        returns True upon a successful creation of a reminder
        """
        response, content = self.auth_http.request(
            uri=URIs['create'],
            method='POST',
            body=client_utils.create_req_body(reminder),
            headers=HEADERS,
        )
        if response.status == HTTP_OK:
            return True
        else:
            print('Error while trying to set a reminder:')
            print(f'    status code: {response.status}')
            print(f'    content: {content}')
            return False
