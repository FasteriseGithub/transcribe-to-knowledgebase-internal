import aiohttp
import json

async def post_to_discord_webhook_async(webhook_url, message):
    # Data payload to be sent to Discord
    data = {
        "content": message,
        "username": "GrimoireAsyncBot"
    }

    # Headers for the HTTP request
    headers = {
        "Content-Type": "application/json"
    }

    # Using aiohttp to make an asynchronous HTTP POST request
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, data=json.dumps(data), headers=headers) as response:
            # Checking if the request was successful
            if response.status == 204:
                print("Message posted successfully")
            else:
                print(f"Failed to post message. Status code: {response.status}")
