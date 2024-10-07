# RobloxUserInfoExtractor

## Introduction

RobloxUserInfoExtractor is a powerful tool designed to retrieve comprehensive information about Roblox users. This script is a must-have for researchers, developers, and investigators looking to gather detailed insights from the Roblox platform. With a simple command-line interface, the tool fetches and exports data about users, including their username history, groups, friends, followers, and much more. By leveraging the Roblox API and advanced web scraping techniques, RobloxUserInfoExtractor ensures that data retrieval is thorough and reliable.

## Telegram Bot Integration

For added convenience, a Telegram bot has been developed that automates the extraction of Roblox user data without the need to run the script manually. This bot can be accessed at https://t.me/RobloxUserInfoExtractor_bot. With this bot, users can retrieve user information quickly and efficiently by simply inputting the Roblox username or ID directly into the chat interface, making the process more user-friendly and accessible.

## Key Features

- **Comprehensive User Information**: Retrieves essential user data, including display names, usernames, description, account status (e.g., banned or verified), and account creation date.
- **Username History**: Fetches the complete history of usernames associated with a given user.
- **Group Membership**: Provides detailed information about a user’s group affiliations, including the group name, membership count, and a direct link to the group.
- **Social Network**: Exports lists of friends, followers, and followings, complete with links to their profiles.
- **Resilient Web Scraping**: Uses randomized user agents and retries mechanisms to handle rate limits and ensure successful data extraction.
- **CSV Export**: Automatically exports group details, friends, followers, and followings into CSV files for further analysis or archival purposes.

## Unique Strengths

- **Error Handling and Retries**: The script incorporates intelligent retries and waiting times, especially in response to HTTP 429 errors (Too Many Requests), ensuring robust operation even when the Roblox API limits requests.
- **Randomized User Agents**: By randomly selecting from multiple user agents, the tool minimizes the likelihood of being blocked by the server, enhancing the success rate of requests.
- **Modular Data Extraction**: Information is obtained in a modular fashion, allowing the user to gather only the specific data they need, from username history to friends and group memberships.
- **Automated Export**: Users benefit from automatic data export to CSV files, making it easy to integrate this data with other systems or analyze it further using external tools.

## API Limitations and Error Handling

One of the primary challenges when interacting with the Roblox API is the rate-limiting mechanism, which frequently returns error code 429 (Too Many Requests) if the requests exceed the allowed rate. This can result in delays or even temporary blocks when querying large volumes of data. To mitigate this, the script implements a retry mechanism that respects the Retry-After header sent by the server. Users should be aware of this limitation, especially when running the tool in environments where high-frequency requests are made. It is recommended to introduce adequate wait times between queries to avoid being throttled by Roblox's API.

## Usage Scenarios

RobloxUserInfoExtractor is perfect for a wide range of applications, including:
- **Cybersecurity Investigations**: Tracking changes in user identities or affiliations.
- **Data Archiving**: Preserving social connections and user data for historical analysis.
- **Research and Analysis**: Gaining insights into the structure and behavior of the Roblox community.
  
## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/N4rr34n6/RobloxUserInfoExtractor.git
   ```
2. Install the required dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

## Prerequisites

- **Python 3.x**: Ensure that Python 3 is installed on your system.
- **pip3**: Make sure to have `pip3` to install dependencies.
  
## Usage

To use RobloxUserInfoExtractor, simply provide a Roblox username or user ID as the identifier:
```bash
python3 RobloxUserInfoExtractor.py <identifier>
```

For example:
```bash
python3 RobloxUserInfoExtractor.py JohnDoe123
```

### Command-line Arguments:
- `<identifier>`: Roblox username or user ID.

### Example Output

```bash
User ID: 123456789
Alias: JohnDoe123
Display Name: John Doe
Description: Passionate Roblox developer!
Banned: No
Verified Badge: Yes
Friends: 150
Followers: 500
Following: 30
Join Date: 2020-01-15
Previous Usernames: JohnDoeDev, JDoe2020
...
```

The script will also export the following files:
- `groups.csv`: List of groups the user is affiliated with.
- `friends.csv`: List of the user’s friends.
- `followers.csv`: List of the user’s followers.
- `following.csv`: List of the users the person is following.

## Technical Details

- **Logging**: The script logs important events and errors to provide visibility into its operation, including request retries and export completion.
- **Web Scraping**: BeautifulSoup is used to extract data from user profiles, ensuring that all available information is retrieved accurately.

## Disclaimer

This tool is intended for educational and research purposes only. Users are responsible for ensuring that the use of this tool complies with Roblox’s terms of service and applicable laws. Use responsibly and ethically.

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). See the [LICENSE](LICENSE) file for more details.
