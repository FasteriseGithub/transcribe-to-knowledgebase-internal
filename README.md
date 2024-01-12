### Dev
Execute in the root directory:

`docker compose up --build` \

Make sure all your Environment variables are set up correctly see the
docker-compose.yml file for the ones you need.

#### To upload a recording
```
curl -X 'POST' \
  'http://0.0.0.0:81/upload' \
  -H 'accept: application/json' \
  -H 'access_token: your_actual_api_key' \
  -H 'Host: fastapi.localhost' \
  -F 'file=@/path/to/your/speech.mp3;type=audio/mpeg'
  ```

This will create a timestamped transcript, remove the greetings and
banter, then create a conversation analysis + summary and post to the
discord webhook.
