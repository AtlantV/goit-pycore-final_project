from setuptools import setup, find_packages

setup(
    name="personal-assistant",
    version="1.0.0",
    description="Personal Assistant CLI - Contact and Notes Manager",
    author="GoIT Student",
    python_requires=">=3.10",
    py_modules=["main", "address_book", "notes", "storage"],
    entry_points={
        "console_scripts": [
            "personal-assistant=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
)
