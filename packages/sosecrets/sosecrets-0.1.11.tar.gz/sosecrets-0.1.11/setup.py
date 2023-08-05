# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sosecrets']

package_data = \
{'': ['*']}

install_requires = \
['sosecrets-core==1.0.20']

setup_kwargs = {
    'name': 'sosecrets',
    'version': '0.1.11',
    'description': 'Simple wrapper to secure your secrets.',
    'long_description': '# sosecrets\n\n`sosecrets` is a Python module that provides a secure way to handle sensitive data by encapsulating it and only exposing it through a controlled interface.\n\nVersion: 0.1.11\n\n[Documentation](https://sosecrets.readthedocs.io/en/latest/)\n\n## Installation\n\nTo install `sosecrets`, you can use pip:\n\n```bash\npip install sosecrets\n```\n\n## Usage\n\nHere\'s are the examples of how to use `sosecrets`:\n\n### Secret\n\nHere\'s an example of how to use `Secret`:\n\n```python\nfrom sosecrets import Secret\n\n# Create a secret value\nsecret_value = Secret("my secret value")\n\n# Use the secret value while keeping it encapsulated\nresult: Secret[T] = secret_value.apply(len)\nprint(result.expose_secret())  # Output: 14\n\n# Get the value of the secret\nvalue = secret_value.expose_secret()\nprint(value)  # Output: "my secret value"\n```\n\nIn this example, we create a `Secret` object with the value "my secret value". We then use the `apply` method to apply the `len` function to the secret value while keeping it encapsulated. Finally, we use the `expose_secret` method to retrieve the value of the secret.\n\n### ImmutableSecretMapping\n\nHere\'s an example of how to use `ImmutableSecretMapping`:\n\n```python\nfrom pathlib import Path\nfrom sosecrets import ImmutableSecretMapping\nfrom dotenv import dotenv_values\n\n# Define the path to the `.env` file\nTHIS_SCRIPT_FILE_PATH = Path(__file__)\nEXAMPLES = THIS_SCRIPT_FILE_PATH.parent / \'.env\'\n\n# Load the environment variables and store them securely\nsecret_env_dict = ImmutableSecretMapping.from_func(dotenv_values, dotenv_path=EXAMPLES)\n\n# Get a dictionary of the exposed values of the secret variables\nexposed_dict = secret_env_dict.expose_dict()\nprint("exposed_dict: ", exposed_dict)\n\n# Print the `ImmutableSecretMapping` object itself\nprint("secret_env_dict: ", secret_env_dict)\n\n# Get the value associated with a key using the `get()` method\nvalue0 = secret_env_dict.get(\'value0\')\nprint("value0: ", value0)\n\n# Get the exposed value of a key using the `get_exposed()` method\nvalue1 = secret_env_dict.get_exposed(\'value1\')\nprint("value1: ", value1)\n```\n\nThe output of the above codes is shown below:\n```\nexposed_dict = {\n    \'value0\': \'3c976b3c66a2aa1d440d3ad99a9653c7\',\n    \'value1\': \'8f7047cda0532a374dbc380edad96c25\',\n...\n    \'value14\': \'277103129cbf6050b7cbd6502eca9810\'}\n\nsecret_env_dict =  {\'value0\': <secrets.Secret object at 0x000002210A017540>, \n                    \'value1\': <secrets.Secret object at 0x000002210A017580>, \n                    ...\n                    \'value14\': <secrets.Secret object at 0x000002210A0178C0>}\n\nvalue0 = <secrets.Secret object at 0x000002210A017540>\nvalue1 = 8f7047cda0532a374dbc380edad96c25\n```\n\nThe example code does the following:\n\n1. Imports the necessary packages: `Path` from `pathlib`, `src` from the `sosecrets` module, `ImmutableSecretMapping` from `secretdicts` in the `sosecrets` module, and `dotenv_values` from the `dotenv` package.\n2. Defines the path to a `.env` file that contains environment variables to be loaded.\n3. Uses `ImmutableSecretMapping.from_func(dotenv_values, dotenv_path=EXAMPLES)` to load the environment variables from the `.env` file and store them in an instance of `ImmutableSecretMapping`.\n4. Prints the exposed dictionary of the `ImmutableSecretMapping` object using the `expose_dict()` method.\n5. Prints the `ImmutableSecretMapping` object itself.\n6. Gets a value from the `ImmutableSecretMapping` object using the `get()` method and prints it.\n7. Gets the exposed value of a key using the `get_exposed()` method\n\n### MutableSecretMapping\n\nSimilar to `ImmutableSecretMapping`.\n\n## Use Cases\nsosecrets can be used in a variety of scenarios where sensitive data needs to be securely handled. Here are some common use cases:\n\nStoring API keys, passwords, and other credentials: sosecrets can be used to securely store sensitive information such as API keys, passwords, and other credentials that are required for authentication or authorization in an application.\n\nHandling personal identifiable information (PII): sosecrets can be used to protect personal identifiable information (PII) such as names, addresses, social security numbers, and other sensitive data that needs to be kept confidential.\n\n## API Reference\n\n### `Secret`\n\nThe `Secret` class encapsulates a secret value and only exposes it through a controlled interface.\n\n```\nSecret(value: Optional[T] = None, func: Optional[Callable[..., T]] = None, func_args: Tuple[Any, ...] = tuple(), func_kwargs: Dict[str, Any] = dict()) -> Secret\n```\n\n- `value`: The secret value to encapsulate.\n- `func`: A function to generate the secret value.\n- `func_args`: The positional arguments to pass to the `func` function.\n- `func_kwargs`: The keyword arguments to pass to the `func` function.\n\n#### `apply`\n\nThe `apply` method applies a function to the secret value while keeping it encapsulated.\n\n```python\napply(self, func: Callable[[Any], Any], *args: Tuple[Any], **kwargs: Dict[str, Any]) -> SecretType:\n```\n\n- `func`: The function to apply to the secret value.\n- `args`: The positional arguments to pass to the `func` function.\n- `kwargs`: The keyword arguments to pass to the `func` function.\n\n#### `expose_secret`\n\nThe `expose_secret` method returns the value of the secret.\n\n```python\ndef expose_secret(self) -> T:\n```\n\n## Contributing\n\nContributions are welcome! Let me know if you need help with anything else.',
    'author': 'Jim Chng',
    'author_email': 'jimchng@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
