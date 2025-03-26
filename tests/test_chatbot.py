from chatterbot import ChatBot
import unittest

class ChatBotTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bot = ChatBot(
            "TestBot",
            logic_adapters=[
                "chatterbot.logic.MathematicalEvaluation",
                "chatterbot.logic.BestMatch"
            ],
            read_only=True
        )

    def test_greeting(self):
        response = self.bot.get_response("Hello")
        self.assertTrue(len(str(response)) > 0)

    def test_math(self):
        response = self.bot.get_response("What is 2 plus 2?")
        print("Math Response:", response)
        self.assertIn("4", str(response))

if __name__ == "__main__":
    unittest.main()
