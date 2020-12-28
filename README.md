# hollingsbot
GPT-2 bot for discord. Once the bot is added to a server, prefixing any message with a `!` will prompt the bot to generate text using the message text.

# Installation
Install requirements: ```pip install -r requirements.txt```

Add a GPT-2 model to the `models` folder. ```python download_model.py 124M```

See this Google Colab project for how to train a new GPT-2 model https://colab.research.google.com/drive/1VLG8e7YSEwypxU-noRNhsv5dW4NfTGce.

Register a Discord bot (https://discord.com/developers/applications/) and add the bot token to `config/conf.json`

Run: ```python bot.py```
