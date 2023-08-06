from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name= "pymigratedb",
    packages=find_packages(),
    version="1.3.0",
    license="Apache License",
    description="This is a package to help you to migrate your database. It will be useful when you work on frameworks or programming languages that don't have a built-in tool to do it or it's little hard to setup.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Indico Innovation",
    author_email="dev@indicoinnovation.pt",
    url="https://github.com/INDICO-INNOVATION/py-migrate-db",
    keywords=["migrate", "migration", "database", "db"],
    install_requires=[
        'greenlet==1.1.2',
        'psycopg2-binary==2.9.3',
        'python-dotenv==0.19.2',
        'SQLAlchemy==1.4.31'
    ],
    entry_points={
        'console_scripts': [
            'migrate = src.migrate:main'
        ]
    },
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        # "Topic :: Software Development :: Build Tools",
        # "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        # "Programming Language :: Python :: 3.4",
        # "Programming Language :: Python :: 3.5",
        # "Programming Language :: Python :: 3.6",
    ],
)
