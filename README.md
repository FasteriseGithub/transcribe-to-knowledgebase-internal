### Dev
`docker compose up --build` \
In root directory

#### To upload a file
```
curl -X 'POST' \
  'http://0.0.0.0:81/upload' \
  -H 'accept: application/json' \
  -H 'access_token: your_actual_api_key' \
  -H 'Host: fastapi.localhost' \
  -F 'file=@/path/to/your/speech.mp3;type=audio/mpeg'
  ```
