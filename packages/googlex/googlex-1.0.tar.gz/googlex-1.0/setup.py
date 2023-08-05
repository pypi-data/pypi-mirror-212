from setuptools import setup, find_packages

setup(
    name = 'googlex',
    version = '1.0',
    author='mohammad saeed salari',
    author_email = 'salari601601@gmail.com',
    description = 'This is a powerful library for building self robots in Rubika',
    keywords = ['googlex', 'google', 'search', 'gogle', 'pyrubika',  'search google', 'google search'],
    long_description = open("README.md", encoding="utf-8").read(),
    python_requires="~=3.7",
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/mrsalari/googlex',
    packages = find_packages(),
    install_requires = ['pycryptodome', 'websocket-client', 'websockets', 'requests', 'aiohttp', 'pillow', 'mutagen', 'tinytag'],
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