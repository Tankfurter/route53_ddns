# Cloudflare Dynamic DNS Updater

This script automatically updates Cloudflare DNS records with your current public IP address. It's designed for use cases where your IP address changes frequently, such as when using a home internet connection with a dynamic IP.

## Features

- Automatically retrieves your current public IP address.
- Updates Cloudflare A records for specified domains.
- Caches the last known IP address to minimize unnecessary API calls.
- Simple configuration using environment variables for security.
- Automatically creates DNS records if they don't exist.
- Supports both proxied and non-proxied records.

## Requirements

- Python 3.6 or higher
- Cloudflare account with a domain configured
- Cloudflare API Token with DNS edit permissions

## Installation

1. Clone this repository
2. Install the required Python library:
   ```sh
   pip install requests
   ```
3. Schedule the script to run periodically using a cron job or other scheduling tool

## Configuration

To use this script, you need to set up your Cloudflare API token. Follow these steps to get the required information from Cloudflare and save it as environment variables for better security practices.

### Step 1: Obtain Cloudflare API Token

1. Sign in to the [Cloudflare Dashboard](https://dash.cloudflare.com/).
2. Navigate to **My Profile** (click on your profile icon in the top right).
3. Select the **API Tokens** tab.
4. Click **Create Token**.
5. Use the **Edit zone DNS** template or create a custom token with the following permissions:
   - **Zone** → **DNS** → **Edit**
6. Select the specific zone (domain) you want to manage, or select all zones.
7. Click **Continue to summary**, then **Create Token**.
8. Copy the API token immediately and store it securely. You won't be able to see it again.

### Step 2: Set Environment Variables

For better security practices, store your Cloudflare API token as an environment variable. You can do this by adding the following line to your shell profile file (e.g., `.bashrc`, `.zshrc`, or `.bash_profile`):

```sh
export CLOUDFLARE_API_TOKEN='YOUR_CLOUDFLARE_API_TOKEN'
```

Replace `'YOUR_CLOUDFLARE_API_TOKEN'` with the token you obtained in Step 1.

After adding this line, reload your shell profile:

```sh
source ~/.bashrc  # or ~/.zshrc, ~/.bash_profile depending on your shell
```

### Step 3: Obtain Your Zone ID

To update DNS records, you need to know the Zone ID for your domain in Cloudflare. Follow these steps to find it:

1. Sign in to the [Cloudflare Dashboard](https://dash.cloudflare.com/).
2. Select the domain you want to update.
3. Scroll down on the **Overview** page.
4. In the **API** section on the right side, you'll see your **Zone ID**. It will look something like `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`.

Make a note of this Zone ID, as you will need to update it in the `cloudflare_dns_update.py` script.

### Step 4: Configure the Script

Open the `cloudflare_dns_update.py` file and update the following variables:

1. **ZONE_ID**: Replace `"YOUR_ZONE_ID"` with your Cloudflare Zone ID from Step 3.
2. **domains**: Update the list with the domain names you want to update. For example:
   ```python
   domains = [
       "example.com",
       "www.example.com",
       "home.example.com"
   ]
   ```

### Optional Configuration

- **TTL**: The default TTL (Time To Live) is set to 300 seconds (5 minutes). You can modify this in the update/create functions if needed.
- **Proxied**: By default, records are not proxied through Cloudflare (set to `False`). If you want to enable Cloudflare's proxy (orange cloud), you can modify the `proxied` parameter in the update/create functions to `True`.
- **IP Cache File**: The script uses `last_ip_cloudflare.txt` to cache the last known IP. This is different from the AWS version to avoid conflicts if both scripts are used.

## Usage

Run the script manually:

```sh
python cloudflare_dns_update.py
```

### Setting up Automatic Updates with Cron

To automatically update your DNS records, you can schedule the script to run periodically using cron:

1. Open your crontab file:
   ```sh
   crontab -e
   ```

2. Add a line to run the script every 5 minutes (adjust the path as needed):
   ```cron
   */5 * * * * /usr/bin/python3 /path/to/cloudflare_dns_update.py >> /path/to/cloudflare_ddns.log 2>&1
   ```

3. Save and exit. The script will now run automatically every 5 minutes.

## How It Works

1. The script retrieves your current public IP address from `http://checkip.amazonaws.com`.
2. It compares this IP with the last known IP stored in `last_ip_cloudflare.txt`.
3. If the IP has changed:
   - For each domain in the list, it checks if an A record exists in Cloudflare.
   - If the record exists, it updates the record with the new IP.
   - If the record doesn't exist, it creates a new A record.
   - It updates the cache file with the new IP.
4. If the IP hasn't changed, no API calls are made to Cloudflare.

## Troubleshooting

- **Authentication errors**: Make sure your `CLOUDFLARE_API_TOKEN` environment variable is set correctly and the token has DNS edit permissions.
- **Zone not found**: Verify that your `ZONE_ID` is correct in the script.
- **Record not updating**: Check that the domain names in the `domains` list exactly match your DNS records in Cloudflare.
- **Permission denied**: Ensure your API token has the correct permissions for the zone you're trying to update.

## Security Notes

- Never commit your API token to version control.
- Use environment variables to store sensitive credentials.
- Limit your API token permissions to only what's necessary (DNS edit for specific zones).
- Regularly rotate your API tokens.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Badges

![GitHub license](https://img.shields.io/badge/license-GPLv3-blue.svg)
![Python version](https://img.shields.io/badge/python-3.6%2B-blue)
![Cloudflare](https://img.shields.io/badge/Cloudflare-DNS-orange)

## Comparison with AWS Route53 Version

This repository also contains an AWS Route53 version (`aws_dns_update.py`). Here are the key differences:

| Feature | AWS Route53 | Cloudflare |
|---------|-------------|------------|
| Authentication | AWS Access Key & Secret | API Token |
| Configuration | Hosted Zone ID | Zone ID |
| Dependencies | boto3, requests | requests only |
| Auto-create records | No (records must exist) | Yes |
| Proxy support | N/A | Yes (optional) |
| Cache file | last_ip.txt | last_ip_cloudflare.txt |

Both scripts can coexist in the same repository and run independently.
