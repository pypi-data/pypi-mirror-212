# Choclo Checker

Choclo Checker is a comprehensive status checker library for various systems including databases, applications, APIs, and servers. It can be used to quickly check and monitor the status of these systems, making it a great tool for system administrators and developers alike.

## Features

- Database checks for MySQL, Oracle, Postgres, Influx, Redis, MongoDB, SQL, and DynamoDB.
- Application checks for Web (HTML, CSS, JavaScript), Mobile (Android, iOS), and Desktop (Windows, macOS, Linux) applications.
- API checks for REST, SOAP, and GraphQL APIs.
- Server connectivity checks using ping.

## Installation

You can install Choclo Checker using pip:

```
pip install choclo_checker
```

## Usage

After installation, you can import the choclo_checker package and use its various modules to check the status of your systems.

Here is an example:

```python
from choclo_checker.db import choclocheck_mysql

# Check MySQL status
status = choclocheck_mysql.check_status()
print(status)
```

## Dependencies

Choclo Checker requires the following Python libraries:

- PyMySQL
- PyMongo
- requests
- ping3

Please make sure to install these libraries before using Choclo Checker.

## Contributing

Contributions are welcome! Please submit a pull request with any enhancements or bug fixes.

## License

Choclo Checker is open-source and licensed under the MIT License.
