# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['video_streamer', 'video_streamer.core']

package_data = \
{'': ['*'], 'video_streamer': ['ui/static/*', 'ui/template/*']}

install_requires = \
['fastapi>=0.92.0,<0.93.0',
 'jinja2>=3.1.2,<4.0.0',
 'pillow>=9.4.0,<10.0.0',
 'pydantic>=1.10.5,<2.0.0',
 'uvicorn>=0.20.0,<0.21.0',
 'websockets>=10.4,<11.0']

entry_points = \
{'console_scripts': ['video-streamer = video_streamer.main:run']}

setup_kwargs = {
    'name': 'mxcube-video-streamer',
    'version': '0.0.0',
    'description': 'FastAPI Based video streamer',
    'long_description': '# video-streamer\nVideo streamer to be used with MXCuBE. The streamer currently suports streaming from Tango (Lima) devices but can be extened to used with other camera solutons aswell. The output streams are either MJPEG or MPEG1.\n\n![Screenshot from 2023-03-03 14-36-02](https://user-images.githubusercontent.com/4331447/222733892-c7d3af26-26ca-4a3c-b9f4-ab56fc91e390.png)\n\n### Installation\n\n```\ngit clone https://github.com/mxcube/video-streamer.git\ncd video-streamer\n\n# optional \nconda env create -f conda-environment.yml\n\n# For development\npip install -e .\n\n# For usage \npip install .\n```\n\n### Usage\n```\nusage: video-streamer [-h] [-c CONFIG_FILE_PATH] [-tu TANGO_URI] [-hs HOST] [-p PORT] [-q QUALITY] [-s SIZE] [-of OUTPUT_FORMAT] [-id HASH] [-d]\n\nmxcube-web Backend server command line utility.\n\noptions:\n  -h, --help            show this help message and exit\n  -c CONFIG_FILE_PATH, --config CONFIG_FILE_PATH\n                        Configuration file path\n  -tu TANGO_URI, --tango-uri TANGO_URI\n                        Tango device URI\n  -hs HOST, --host HOST\n                        Host name to listen on for incomming client connections defualt (0.0.0.0)\n  -p PORT, --port PORT  Port\n  -q QUALITY, --quality QUALITY\n                        Compresion rate/quality\n  -s SIZE, --size SIZE  size\n  -of OUTPUT_FORMAT, --output-format OUTPUT_FORMAT\n                        output format, MPEG1 or MJPEG1\n  -id HASH, --id HASH   Sream id\n  -d, --debug           Debug true or false\n```\n\nThere is the possibility to use a configuration file instead of command line arguments. All  command line arguments except debug are ignored if a config file is used. The configuration  file also makes it possible to configure several sources while the command line only allows  configuration of a single source.\n\n### Example command line (for testing):\n```\nvideo-streamer -d -of MPEG1 -tu test\n```\n\n#### Example configuration file (config.json):\nThe configuration file format is JSON. A test image is used when the input_uri is set to "test". The example below creates one MPEG1 stream and one MJPEG stream from the test image. There is a defualt test/demo UI to see the video stream on http://localhost:[port]/ui. In example below case:\n  \n MPEG1: http://localhost:8000/ui\n \n MJPEG: http://localhost:8001/ui\n\n\n```\nvideo-streamer -c config.json\n\nconfig.json:\n{\n    "sources": {\n        "0.0.0.0:8000": {\n            "input_uri": "test",\n            "quality": 4,\n            "format": "MPEG1"\n        },\n        "0.0.0.0:8000": {\n            "input_uri": "test",\n            "quality": 4,\n            "format": "MJPEG"\n        }\n    }\n}\n```\n  \n',
    'author': 'Marcus Oskarsson',
    'author_email': 'oscarsso@esrf.fr',
    'maintainer': 'Marcus Oskarsson',
    'maintainer_email': 'oscarsso@esrf.fr',
    'url': 'http://github.com/mxcube/fast-api-streamer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
