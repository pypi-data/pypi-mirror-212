# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cqfbt']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=1.0.0,<2.0.0', 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'cqfbt',
    'version': '1.0.0',
    'description': '',
    'long_description': "# Cornell Quant Fund Backtester (cqfbt)\n\n## Engine\n\nAn `Engine` is the main component in our backtester. It accepts strategies and simulates them on the price data it is initialized with, and can output a variety of metrics on their performance.\n\nThe `Engine` is initialized with a start date and end date to pull data for, as well as the periodicity of the data. Price data is pulled from Yahoo Finance via the `yfinance` package. Optionally, the `Engine` can also be initialized with a list of Yahoo Finance tickers to load price data for.\n\nA feature of the `Engine` is the ability to set transaction costs. These must be set via the `Engine.set_transaction_costs` method, which takes either a float representing a uniform transaction cost or a list of floats for each portfolio asset.\n\nThe `Engine` also contains methods that compare portfolio returns to a market benchmark. This market benchmark is set to the `SPX`, `DJI`, or `NDAQ` ticker, depending on which one is included in the list of tickers to load price data for during initialization. If more than one benchmark ticker appears in the ticker list, the market benchmark is set to the benchmark ticker that appears last in the ticker list. If no benchmark ticker is included in the ticker list, the default is the `SPY` ticker.\n\n## Strategy\n\nA `Strategy` is an abstract class that requires the user of the backtester to implment the method 'execute()'. This function can access memory, and use incoming data to decide which orders the engine should to attempt to close.\n\nA `Strategy` should inherit the strategy interface defined in the strategy module, and define its 'execute()' function. The execute function should return a list of orders to the engine, which the engine will attempt to execute. An 'InsufficientFundsException' may arise if there is insufficient capital to complete a transaction. In this case, the order list will be cleared, and the 'error' parameter will be set to true, while the same data is passed to 'execute()'. If this error is not addressed, the engine will crash.\n\n## Order\n\nAn `Order` is an object that represents an order submitted to the engine. An order has a boolean value representing buy as True and sell as False, an asset number, a quantity, and optionally, a limit price.",
    'author': 'Jack Young',
    'author_email': '59127086+JackRYoung@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
