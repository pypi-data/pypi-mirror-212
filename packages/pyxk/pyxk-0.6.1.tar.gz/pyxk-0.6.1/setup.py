from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyxk",
    version="0.6.1",
    author="pengke",
    install_requires=[
        "requests",
        "pycryptodome",
        "rich",
        "m3u8",
        "aiohttp",
        "aiofiles",
        "click",
    ],
    entry_points={
        'console_scripts': [
            'm3u8 = pyxk.m3u8.enter_point:main',
            'req = pyxk.requests.entry_point:main'
        ],
    },
    author_email="925330867@qq.com",
    description="pyxk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
