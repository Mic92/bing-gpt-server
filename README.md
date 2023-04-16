# Webfrontend/API for BingGPT

1. Log into BingGPT (if you are not using Microsoft Edge you will need to spoof your useragent)
2. Export your sessions cookies as json.
  - In Firefox: Open the developer tools, go to the Network tab, and refresh the page.
  - Click on a request in the Tab "Cookies", do a right click on a cookie and select "Copy all"
  - use this value for `COOKIE_PATH`


```
pip install -e . 
```

```
COOKIE_PATH=/tmp/cookies.json python -m bing_gpt_server
```

# Demo

[Screenshot](./screenshot.jpg)
