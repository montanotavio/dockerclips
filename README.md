# Django Website To Share Clips Utilizing Docker

This is a Django webapp I made to allow friends to share clips with each other! For quick setup, the app is containerized in docker. Supports uploading mp4, mkv, and webm files with custom passcode. Main page is sorted by most recent clips. Upload page has copy direct link button to the uploaded video for fast sharing!

![alt-text](https://github.com/montanotavio/dockerclips/blob/main/clips_demo.gif)

## Deployment

A sample compose file can be seen in the root folder. Necessary environment variables are as follows:

| Variable        | Purpose        |
| ------------- |:-------------:|
|DB_NAME| Name of postgres database |
|DB_USER| Username of postgres database |
|DB_PASS| Password of postgres database |
|HASH_SALT| String of characters appended before the hashed passcode |
|SHA256_PASS| SHA256 hash of passcode+salt to authorize clip upload |
|SECRET_KEY| Django secret key |
|TRUSTED_ORIGINS| Root url of website including protocol |
|ALLOWED_HOSTS| Same as TRUSTED_ORIGINS |
