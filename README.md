# DiscordGPT Assistant Bot

#### Invite GPT bots into your Discord server!

## Getting Started

You can create a Docker image for your bot and host it on ECS or on your server locally. A Dockerfile is provided in this repo for you to build.

Make sure to create a DynamoDB table on your AWS account first then configure your AWS credentials on your local environment before building the bot.

### Option 1: Running with Docker

Build the Docker image
```
docker build -t discord-gpt-bot .
```
Run the Docker container
```
docker run -d --name discord-gpt-bot -e DISCORD_API_KEY=<your_token> OPENAI_API_KEY=<your_api_key> OPENAI_ASSISTANTS_ID=<your_assistants_id> DYNAMODB_TABLE_NAME=<your_table_name> discord-gpt-bot
```

### Option 2: Running Locally with a Virtual Environment

Create a virtual environment
```
python3 -m venv venv
```
Activate the virtual environment
```
source venv/bin/activate  # On macOS/Linux
.\venv\Scripts\activate  # On Windows
```
Install the required dependencies
```
pip install -r requirements.txt
```
Run the bot
```
python bot.py
```

## Configuration

- **DISCORD_API_KEY:** Your Discord bot token.
- **OPENAI_API_KEY:** Your API key from OpenAI.
- **OPENAI_ASSISTANTS_ID:** Your Assistants ID from OpenAI. Make sure to create an Assistants first on the Platform.
- **DYNAMODB_TABLE_NAME:** Your table name on DynamoDB.
- **AWS Credentials:** Make sure your environment has access to AWS credentials.

## Features

- **Channel-Specific Permissions:** Administrators can allow or disallow the bot to respond in specific channels using $allow_channel and $disallow_channel.
- **GPT Integration:** The bot interacts with OpenAI's GPT API to generate responses based on the user's input.
- **Retry Logic:** Handles API retries to ensure reliability.

## DynamoDB Integration

The bot uses AWS DynamoDB to store and manage conversation threads for different guilds.

- **Table Name:** `your-dynamodb-table-name`
- **Primary Key:** `guild_id`

## Contribution

Feel free to contribute to this project by submitting issues or pull requests.

## License

This project is licensed under the MIT License.