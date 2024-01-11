import aiohttp
import json

async def post_to_discord_webhook_async(webhook_url, message):
    data = {
        "content": message,
        "username": "fasterise-internal"
    }
    headers = {"Content-Type": "application/json"}

    print("Sending to discord")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, data=json.dumps(data), headers=headers) as response:
                response_text = await response.text()  # Get response text for detailed error message

                if response.status == 204:
                    print("Message posted successfully")
                else:
                    print(f"Failed to post message. Status code: {response.status}, Response: {response_text}")
    except Exception as e:
        print(f"An error occurred: {e}")

