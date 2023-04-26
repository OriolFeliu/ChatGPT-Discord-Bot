import discord
import openai


DISCORD_API_KEY = (
    "MTEwMDQyNTUzMTg2Mzg1OTMwMQ.GDFs7u.C7OoeIkc9THHpuQAUzcg-aukBdJCEZJVChUQxM"
)
OPENAI_ORGANIZATION = "org-3K7RgRFjDSc7DT0PxzX4uMyj"
OPENAI_API_KEY = "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"

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)

# OPENAI
openai.organization = OPENAI_ORGANIZATION
openai.api_key = OPENAI_API_KEY


# Define the function that sends a message to OpenAI API to generate a response
async def generate_response(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
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
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
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
            response = await generate_response(prompt)

            await message.channel.send(response)

    except Exception as e:
        await message.channel.send(
            f"There was an error trying to generate the response:\n {e}"
        )


client.run(DISCORD_API_KEY)
