import json

from app.interfaces.command import Command
from app.interfaces.feedback import Feedback


class CommandTest(Command):

    def __init__(self, body_json):
        print("ComamndTest")

        self.body_json = body_json

    def execute(self) -> Feedback:
        command_entity = json.loads(self.body_json)
        pur = command_entity['purpose']
        user = command_entity['username']
        payload = self.body_json
        feed = Feedback(payload="CommandTest", ID_of_text=user, purpose=pur)
        print(f"RECIEVE TO CommandTest {self.body_json}")
        return feed
