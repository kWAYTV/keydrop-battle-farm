# CaseBattle Bot

This bot is designed to monitor and join available battles on the [Key-Drop](https://kdrp2.com/CaseBattle/) platform.

## Features

- Continuously monitor active battles
- Automatically join available free battles
- Adjustable sleep intervals and ticket cost threshold
- Error handling for network requests
- Logging system to track activity and errors

## Getting Started

1. Clone this repository: `git clone https://github.com/kWAYTV/keydrop-battle-farm.git`
2. Navigate into the project directory: `cd casebattle-bot`
3. Install the required Python packages: `pip install -r requirements.txt`
4. Obtain your Key-Drop Bearer token:

   - Go to [Key-Drop.com](https://key-drop.com/)
   - Inspect the website in the network tab (right-click on the page, select "Inspect" or "Inspect Element", then go to the "Network" tab)
   - Search for "token" in the network tab
   - If you can't find it, refresh the page once
   - You should see something like `token?t=12345`. This is your token.
  
5. Replace `"your_token_here"` in the main script with your actual token.
6. Run the script: `python main.py`

## Configuration

The `CaseBattle` class can be initialized with the following optional parameters:

- `token` (str): Your Key-Drop token for API requests. **(Required)**
- `sleep_interval` (int): The number of seconds the bot should sleep between checking battles. Default is 1.
- `ticket_cost_threshold` (int): The maximum ticket cost that the bot should consider for free battles. Default is 1000.

Example:

    ```python
    cb = CaseBattle(token="your_token_here", sleep_interval=2, ticket_cost_threshold=500)
    ```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://github.com/kWAYTV/keydrop-battle-farm/blob/main/LICENSE)
