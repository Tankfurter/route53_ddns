# AWS Route 53 Dynamic DNS Updater

This script automatically updates AWS Route 53 DNS records with your current public IP address. It's designed for use cases where your IP address changes frequently, such as when using a home internet connection with a dynamic IP.

## Features

- Automatically retrieves your current public IP address.
- Updates AWS Route 53 A records for specified domains.
- Caches the last known IP address to minimize unnecessary API calls.
- Simple configuration using environment variables for security.

## Requirements

- Python 3.6 or higher
- AWS account with Route 53 hosted zone
- AWS credentials with appropriate permissions (Route 53 access)

## Installation

1. Clone this repository
2. Schedule the script to run periodically using a cron job or other scheduling tool

## Configuration

To use this script, you need to set up your AWS credentials. Follow these steps to get the required information from AWS and save it as environment variables for better security practices.

### Step 1: Obtain AWS Credentials

1. Sign in to the [AWS Management Console](https://aws.amazon.com/console/).
2. Navigate to the [IAM (Identity and Access Management) Dashboard](https://console.aws.amazon.com/iam/).
3. In the left sidebar, click on "Users" and then select your IAM user.
4. Go to the "Security credentials" tab.
5. Click on "Create access key" to generate a new access key ID and secret access key. Make sure to download the `.csv` file or copy the keys to a secure location.

### Step 2: Set Environment Variables

For better security practices, store your AWS credentials as environment variables. You can do this by adding the following lines to your shell profile file (e.g., `.bashrc`, `.zshrc`, or `.bash_profile`):

```sh
export AWS_ACCESS_KEY_ID='YOUR_AWS_ACCESS_KEY_ID'
export AWS_SECRET_ACCESS_KEY='YOUR_AWS_SECRET_ACCESS_KEY'
```

Replace `'YOUR_AWS_ACCESS_KEY_ID'` and `'YOUR_AWS_SECRET_ACCESS_KEY'` with the values you obtained in Step 1.

After adding these lines, reload your shell profile:

```sh
source ~/.bashrc  # or ~/.zshrc, ~/.bash_profile depending on your shell
```

### Step 3: Obtain Your Hosted Zone ID

To update DNS records, you need to know the Hosted Zone ID for your domain in Route 53. Follow these steps to find it:

1. Sign in to the [AWS Management Console](https://aws.amazon.com/console/).
2. Navigate to the [Route 53 Dashboard](https://console.aws.amazon.com/route53/).
3. In the left sidebar, click on "Hosted zones."
4. Find the domain you want to update and click on its name.
5. The Hosted Zone ID will be displayed in the "Hosted Zone Details" section at the top. It will look something like `Z1D633PJN98FT9`.

Make a note of this Hosted Zone ID, as you will need it for the script configuration.
## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Badges

![GitHub license](https://img.shields.io/badge/license-GPLv3-blue.svg)
![Python version](https://img.shields.io/badge/python-3.6%2B-blue)
![AWS Route 53](https://img.shields.io/badge/AWS-Route%2053-orange)
