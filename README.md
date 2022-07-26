# logger-manager


package build

* python setup.py sdist bdist_wheel
* python -m twine upload dist/*

reference
* https://wikidocs.net/78954


guide
* pip install pizza-logger-manager-g


How to use
```python
from logger_manager import LoggerManager

logger_manager_obj = LoggerManager.LoggerManager(logger_name='hello')
```