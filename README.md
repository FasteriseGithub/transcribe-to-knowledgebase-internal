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

### Prod
1. Set up ubuntu VM on your cloud provider
2. Install docker using apt repository: https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
3. Change domain in `docker-compose.prod.yml` to your domain + subdomain
4. Change email in `services/traefik/traefik.prod.toml` to the email you
   want managing the ssl certificate, make sure this is a valid email
5. Generate two uuids by running `uuidgen`
6. Edit `services/api/main.py` in the route where it says `
@app.post("/replace-with-your-uuid")` and paste your uuid in there
should look like this `
@app.post("/5553a929-c13d-47b6-8167-54b806e38d0d")`
7. Change `/etc/environment` on your VM and add in the following
environment variables
```
      - OPENAI_API_KEY=your-key
      - DISCORD_WEBHOOK_URL=your-webhook
      - API_KEY_INTERNAL=one-of-the-uuids-you-generated
      - PINECONE_API_KEY=your-pinecone-api-key
      - PINECONE_ENV=your-pinecone-environment-name
```
note: The API_KEY_INTERNAL is one of the uuids you generated.


8. Make sure you are in the root directory, the one that has the
   `docker-compose.prod.yml` file and run the following command.
    `docker-compose -f docker-compose.prod.yml up --build`


9. Do a smoke test with `curl https://sub.domain.com/ping` from another
   machine. Use postman if you don't have curl installed. It should
   return `pong`

All good you are all done, you can now make requests to the api using
the uuids you generated. Example below:

```
curl -X POST "https://api-internal.fasterise.com/replace-with-your-uuid?meeting_type=General&meeting_date=2024-01-01" \
     -H "access_token: replace-with-api-key-you-generated-and-put-in-environment" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/home/user/Downloads/the_audio_file_you_want_to_post_to_the_kb.m4a;type=audio/mpeg"

```

Todo: create a set-up script to help you with this process. Any
volunteers?



