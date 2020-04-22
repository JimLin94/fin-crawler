# FIN Crawler

## Milestone

 - [ ] KOSPI採用YAHOO FINANCE
 - [X] N225採用YAHOO FINANCE
 - [X] TOPIX採用YAHOO FINANCE
 - [X] SHCOMP
 - [X] TWSE
 - [X] TWOTC
 - [X] SXXP 有代碼

## Prerequisite

 - Python 3.7 >
 - Docker-compose v3


## Install

pip install -r requirements.txt

## How to start to parse?

python src/main.py `{spider_name}` e.g ewy, etc.

## Docker

docker-compose up -d

### MySQL NOTE

- (Create a user with remotely accessible connect)[http://itman.in/en/mysql-add-user-for-remote-access/]
- (Grant the user privileges)[https://chartio.com/resources/tutorials/how-to-grant-all-privileges-on-a-database-in-mysql/]

### env for the crawler container

DB_HOST=db
DB_PORT=3306
DB_USER=jim
DB_PASS=jim
DB_NAME=trading_club
WEB_DRIVER_HOST=selenium-hub
WEB_DRIVER_PORT=4444

