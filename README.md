#### To upload a file:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/upload/' \
  -H 'accept: application/json' \
  -H 'access_token: your_actual_api_key' \
  -F 'file=@path_to_your_file'
  ```
