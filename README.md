# Shor10

This is an extremely simple personal-use link shortener. It's designed to have only one user submit links to shorten. It stores the url mapping in a simple json file on disk. Maybe I'll upgrade to sqlite in the future, especially if I want to start tracking every click.

# Dependencies

This app uses `uv` for dependency management. You can get the exact versions used to build the application by running `uv sync`.

# Configuration

It is recommended to use a `.env` file to set the following random values for the application.

- `FLASK_SECRET_KEY`
- `SHOR10_PASSWORD`

To set these values, it is recommended to use the python `secrets` module.

```
python3  -c "import secrets; print(secrets.token_urlsafe(64))"
```

Optionally, you can set `SHOR10_URLS` if you'd like to change where the data gets saved.

# Deploying



# License

Copyright 2024 0xdade

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
