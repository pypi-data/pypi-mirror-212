from setuptools import setup, find_packages

setup(
    name = 'pyrubi',
    version = '2.1.0',
    author='Ali Ganji zadeh',
    author_email = 'ali.ganji.za@gmail.com',
    description = 'This is a powerful and easy library for building self Bots in Rubika',
    keywords = ['rubika', 'rubino', 'pyrubi', 'pyrubika', 'rubx', 'rubika.ir', 'bot', 'chat'],
    long_description = open("README.md", encoding="utf-8").read(),
    python_requires="~=3.6",
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/AliGanji1/pyrubi',
    packages = find_packages(),
    install_requires = ['pycryptodome', 'websocket-client', 'requests', 'aiohttp', 'urllib3', 'pillow', 'mutagen', 'tinytag'],
    classifiers = [
    	"Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ]
)