import json
import logging
from app.Commands.Command_test import CommandTest
from app.Commands.MultiTranslate import MultiTranslate

# Initialize the logger
logger = logging.getLogger('app.Factory')


class Factory:
    def lifeCheck(self):
        logger.info("Factory lifeCheck called.")
        return [True, "factory"]

    def __init__(self):
        # purpose -> is type of command
        self.commands = {
            'test': CommandTest,
            'multitranslate': MultiTranslate,
            # etc
            # Add other commands as needed
        }
        logger.info("Factory initialized with commands: %s", ', '.join(self.commands.keys()))

    def execute_command(self, cmd):
        try:
            logger.info(f"Executing command with input: {cmd}")
            command_entity = json.loads(cmd)
            cmd_type = command_entity['purpose']
            logger.info(f"Command type: {cmd_type}")

            command_class = self.commands.get(cmd_type)
            if command_class is None:
                logger.error(f"Unknown command type: {cmd_type}")
                raise ValueError(f"Unknown command type: {cmd_type}")

            if not callable(command_class):
                logger.error(f"Command {cmd_type} is not callable.")
                raise TypeError(f"Command {cmd_type} is not callable.")

            command = command_class(cmd)
            result = command.execute()
            logger.info(f"Command executed successfully. Result: {result}")
            return result
        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode error: {str(e)}. Input: {cmd}")
            raise
        except Exception as e:
            logger.error(f"Error executing command: {str(e)}")
            raise
