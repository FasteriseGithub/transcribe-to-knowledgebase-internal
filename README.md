#### To upload a file:
```
curl -X 'POST' \
  'http://0.0.0.0:81/ping' \
  -H 'accept: application/json' \
  -H 'access_token: your_actual_api_key' \
  -H 'Host: fastapi.localhost' \
  -F 'file=@path_to_your_file'
  ```
