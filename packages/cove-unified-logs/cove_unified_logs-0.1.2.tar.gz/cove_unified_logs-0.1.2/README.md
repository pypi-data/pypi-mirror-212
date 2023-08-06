
# Cove Unified Logs

Cove Unified Logs is a Python library for handling logs in various environments (Django, AWS Lambda, Google Cloud) and pushing them to AWS CloudWatch in an asynchronous way.

## Author

**SARVPRIYE SONI**

- Github: [@Cove-Identity](https://github.com/Cove-Identity/cove-unified-logs)
- Email: sarvpriye.soni@coveidentity.com




## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Cove Unified Logs.

```bash
pip install cove_unified_logs
```



# AWS Credentials Configuration

To interact with AWS services, Cove Unified Logs uses boto3, the AWS SDK for Python. You need to configure your AWS credentials for use with boto3. Here's how:

1) **Environment Variables:** Set the `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_SESSION_TOKEN` (optional for when you are using AWS STS temporary credentials) environment variables.
2) **Shared Credential File (~/.aws/credentials):** Use an AWS credentials file to specify your credentials. The default location is `~/.aws/credentials`.
3) **AWS Config File (~/.aws/config):** Similar to the credentials file, you can also have a configuration file. The default location is ~/.aws/config. This file allows you to specify your region along with your credentials. 
4) **IAM Role:** If your application is running on an EC2 instance, you can assign an IAM role to the instance with the necessary permissions, and the boto3 client will automatically use the credentials from the IAM role.

For more information, check the [official Boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration).

#Usage
To use Cove Unified Logs in a Python application, first create an instance of the UnifiedLogger class:


```python
from cove_unified_logs import UnifiedLogger

logger = UnifiedLogger('your-app-name', config='all')
```
You can then use this logger to log messages at different levels:


```python
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
```    

Each log message is automatically annotated with metadata including the app name, timestamp, and log level.

##Django Middleware
To use Cove Unified Logs as middleware in a Django application, first add the middleware to your `MIDDLEWARE` setting:

```
# settings.py
MIDDLEWARE = [
    ...
    'cove_unified_logs.middleware.LoggingMiddleware',
    ...
]

```

Next, add the log level to your settings:

```python
# settings.py
LOG_LEVEL = 'debug'  # or 'info', 'warning', 'error', 'critical'
```
Finally, in the module where you initialize your `UnifiedLogger`, set the log level from your settings:

```python
# your file where UnifiedLogger is used
from django.conf import settings
from cove_unified_logs import UnifiedLogger

app_name = apps.get_app_config(__package__.split('.')[0]).verbose_name
logger = UnifiedLogger(app_name, config='all')
logger.set_level(settings.LOG_LEVEL)
```

Remember to replace 'your-app-name' with the name of your application, and to adjust the apps.get_app_config(__package__.split('.')[0]).verbose_name line as necessary for your project structure.


All logs from your Django application will then be sent to both the console and AWS CloudWatch.


##Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

# Confidentiality Notice

This software, including all the code, scripts, features, and documentation associated with it, is a proprietary product of Coveidentity Tech Private Limited, and is confidential in nature. It is only intended for use within Coveidentity Tech Private Limited, by employees or authorized collaborators who have been granted access. 

# License

This project is licensed under the terms of the Proprietary License. Unauthorized copying, distribution, modification, public display, or public performance of this proprietary software, or any subset of the proprietary software, is strictly prohibited. 

# Disclaimer

The software is provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of
