import io
import re
from setuptools import setup, find_packages

with io.open("README.md") as f:
    long_description = f.read()

with io.open("mail_notification/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="mouritech-mail-notification",
    version=version,
    description="Sending mails",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.mouritech.com/mt-digital-core-platform/"
        "python/mail-notification",
    author="Venkatesh Areti",
    author_email="venkateshar.in@mouritech.com",
    license="MIT",
    packages=find_packages(),
    install_requires=['pika'],
    extras_require={
        "dev": [
            "pytest",
            "flake8"
        ]
    },
    project_urls={
        "Source": "https://gitlab.mouritech.com/mt-digital-core-platform/"
                  "python/mail-notification",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    zip_safe=False,
    python_requires=">=3",
)
