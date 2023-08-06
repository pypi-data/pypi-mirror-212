# Lamadava client, for Python 3

![PyPI](https://img.shields.io/pypi/v/lamadava)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lamadava)

[![Downloads](https://pepy.tech/badge/lamadava)](https://pepy.tech/project/lamadava)
[![Downloads](https://pepy.tech/badge/lamadava/month)](https://pepy.tech/project/lamadava)
[![Downloads](https://pepy.tech/badge/lamadava/week)](https://pepy.tech/project/lamadava)


## Installation

```
pip install lamadava
```

## Usage

Create token https://lamadava.com/tokens and copy "Access key"

```
from lamadava import Client
cl = Client(token="<ACCESS_KEY>")
user = cl.user_by_username_v2("instagram")
print(user)
```
