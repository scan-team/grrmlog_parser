[![License: MIT](https://img.shields.io/github/license/vintasoftware/django-react-boilerplate.svg)](LICENSE.txt)

# grrmlog_parser

This program converts output files of the GRRM program to a python object.

## Usage

Extracting GRRM-generated data can be done with:

```python3
import os
import pickle
from grrmlog_parser.core import parse

# Parse GRRM-generated map
fname_top_abs, _ = os.path.splitext("/path/to/map.com") # Absolute path to .com file, without the trailing ".com"
map_data = parse(fname_top_abs)

# Map data object can be saved...
with open("/path/to/save/file.pkl", 'wb') as pickle_file:
    pickle.dump(map_data, pickle_file)

# ...and loaded back for further processing
with open("/path/to/save/file.pkl", 'rb') as pickle_file:
    map_data = pickle.load(pickle_file)
```

For more details on the structure of the generated ```GRRMMap``` object, please refer to [the internal documentation](grrmlog_parser/models/__init__.py).

## License

[MIT License](LICENSE.txt)

Copyright (c) 2021-present Yu Harabuchi

