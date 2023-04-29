import discord
import openai
from api_keys import DISCORD_API_KEY, OPENAI_ORGANIZATION, OPENAI_API_KEY


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)

# OPENAI
# openai.organization = OPENAI_ORGANIZATION
openai.api_key = OPENAI_API_KEY

messages = [
    {"role": "system", "content": "From now on, the messages you recieve will be from Discord users, so you are a Discord bot, act as such, don't give answers that are too long, but you are still chatGPT."}
]


# Define the function that sends a message to OpenAI API to generate a response
async def generate_response(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            n=1, # number of chat completion choices to generate for each input message
            # max_tokens = 100
        )

        return completion.choices[0].message.content

    except openai.error.RateLimitError as e:
        return f"Rate limit exceeded: {e}"
    except openai.error.AuthenticationError as e:
        return f"Invalid API key or organization: {e}"
    except Exception as e:
        return f"An error occurred: {e}"


@client.event
async def on_ready():
    try:
        print("Logged in as {0.user}".format(client))
    except Exception as e:
        print(f"Error during login process: {e}")


@client.event
async def on_message(message):
    global messages
    try:
        # Condition to check that the message is not sent by the bot
        if message.author == client.user:
            return

        print("--Message Content--")
        print(message.content)

        if message.content.startswith("!c"):
            await message.channel.send("Waiting for ChatGPT response...")

            prompt = message.content[3:]
            print(prompt)

            messages.append({"role": "user", "content": prompt})

            response = await generate_response(prompt)

            messages.append({"role": "assistant", "content": response})

            await message.channel.send(response)

        elif message.content.startswith("!new"):
            print("--Conversation cleared--")
            messages = [
                {"role": "system", "content": "From now on, the messages you recieve will be from Discord users, so you are a Discord bot, act as such, don't give answers that are too long"}
            ]

    except Exception as e:
        await message.channel.send(
            f"There was an error trying to generate the response:\n {e}"
        )


client.run(DISCORD_API_KEY)
