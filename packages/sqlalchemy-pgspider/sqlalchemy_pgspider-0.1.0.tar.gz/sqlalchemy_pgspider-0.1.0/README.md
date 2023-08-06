# sqlalchemy-pgspider

A [SQLAlchemy](https://www.sqlalchemy.org/) Dialect for [PGSpider](https://github.com/pgspider/pgspider).

## Overview

This is a module that allows you to connect to PGSpider using SQLAlchemy's PostgreSQL Dialect.

SQLAlchemy PostgreSQL Dialect uses the string obtained from pg_catalog.version() to determine whether it is PostgreSQL or not, and Postgres Dialect cannot be used to connect to PGSpider.

sqlalchemy-pgspider inherits PostgreSQL Dialect and overrides the part that checks version information, so that it can connect to PGSpider while retaining PostgreSQL Dialect functionality.

> **note**  
> Only psycopg2 DBAPI is supported.

## Requirements

* SQLALchemy 1.4.27 or higher 
* psycopg2 (or psycopg2-binary) 2.9 or higher
* Python 3.7 or higher

Almost all features supported by PostgreSQL's psycopg2 in SQLAlchemy 1.4.28 are available.  
Other versions have not been tested.

## Installation

Packages can be installed from either PyPI or GitHub.

Install package from PyPI.

```
pip install sqlalchemy-pgspider
```

from GitHub.

```
pip install git+https://github.com/pgspider/sqlalchemy-pgspider
```

## Usage

To connect to PGSpider with SQLAlchemy, the following URL pattern can be used:

```
pgspider+psycopg2://<username>:<password>@<host>:<port>/<dbname>
```

Instead of the `pgspier+psycopg2:`, you can also use `pgspider:`.  
The behaviour is the same whichever you use.

```
pgspider://<username>:<password>@<host>:<port>/<dbname>
```

For more detailed usage, see the SQLAlchemy PostgreSQL psycopg2 documentation.  
Just change the drivername part of the URL pattern in the documentation from `postgresql+psycopg2` to `pgspider+psycopg2`(or `pgspider`) to work.

> **See Also:**  
> SQLAlchemy 1.4 Documentation Dialects PostgreSQL  
> https://docs.sqlalchemy.org/en/14/dialects/postgresql.html


## Sample code

```python
from sqlalchemy import create_engine, text

engine = create_engine("pgspider+psycopg2://pgspider:password@localhost:4813/pgspiderdb")

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE users (id SERIAL NOT NULL PRIMARY KEY, name text)"))
    conn.execute(text("INSERT INTO users (name) VALUES ('Bea'), ('Eddy'), ('Lily')"))

    result = conn.execute(text("SELECT * FROM users WHERE name='Lily'"))
    for row in result:
       print(row)

    conn.execute(text("DROP TABLE users"))
```

Running this code would output the following string.

```
(3, 'Lily')
```

Although not included in the sample code, the SQLAlchemy ORM can also be used.


## Testing 

### Requirements

* A PGSpider instance up and running
* pytest >= 7.1.1 installed on the testing machine

### Procedure

1. Clone this repository
2. Change [tests/conftest.py](tests/conftest.py) as appropriate
3. Run pytest
