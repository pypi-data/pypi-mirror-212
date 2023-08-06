from setuptools import setup, find_packages

# Read the content of README file
with open("silicron/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="silicron",
    version="0.0.3",
    url="https://github.com/michaelliangau",
    author="Michael Liang",
    author_email="michaelliang15@gmail.com",
    packages=find_packages(),
    description="Give chatbots memory.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
)
