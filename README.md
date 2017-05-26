OpenCTF
=======

Clone this repository. Make a .env file that looks like this:

```
# environment = { test | development | production }
ENVIRONMENT=development

# for database container
MYSQL_ROOT_PASSWORD=password

# for openctf container
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=openctf
```

Run these commands.

```bash
git submodule update --init
docker-compose up -d
```