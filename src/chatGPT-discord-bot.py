import discord
import openai
from api_keys import DISCORD_API_KEY, OPENAI_ORGANIZATION, OPENAI_API_KEY


class ChatGPTBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = [{
            "role": "system",
            "content": "From now on, the messages you recieve will be from Discord users, so you are a Discord bot, act as such, give answers that are as short as possible, but you are still chatGPT.",
        }]
        openai.api_key = OPENAI_API_KEY

    async def generate_response(self):
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages,
                n=1
            )
            return completion.choices[0].message.content

        except openai.error.RateLimitError as e:
            return f"Rate limit exceeded: {e}"
        except openai.error.AuthenticationError as e:
            return f"Invalid API key or organization: {e}"
        except Exception as e:
            return f"An error occurred: {e}"

    async def on_ready(self):
        print("Logged in as {0.user}".format(self))

    async def on_message(self, message):
        try:
            # Condition to check that the message is not sent by the bot
            if message.author == self.user:
                return

            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)
            print(f" {username} said: '{user_message}' ({channel})")

            if message.content.startswith("!c") or message.content.startswith(f"<@{self.user.id}>"):
                async with message.channel.typing():  # Display "ChatGPT is typing..." message
                    prompt = message.content[3:] if message.content.startswith(
                        "!c") else message.content.replace(f"<@{self.user.id}>", "").strip()

                    self.messages.append({
                        "role": "user",
                        "content": prompt
                    })

                    response = await self.generate_response()

                    self.messages.append({
                        "role": "assistant",
                        "content": response
                    })

                    await message.channel.send(response)

            elif message.content.startswith("!new"):
                print("--Conversation cleared--")
                self.messages = [
                    {
                        "role": "system",
                        "content": "From now on, the messages you recieve will be from Discord users, so you are a Discord bot, act as such, don't give answers that are too long",
                    }
                ]

            elif message.content.startswith("!help"):
                help_text = """
                **Commands:**
                `!c <prompt>` - Ask a question or start a conversation
                `!new` - Clear the current conversation
                `!help` - Show this help message
                """
                await message.channel.send(help_text)

        except Exception as e:
            await message.channel.send(
                f"There was an error trying to generate the response:\n {e}"
            )


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
client = ChatGPTBot(intents=intents)
client.run(DISCORD_API_KEY)
