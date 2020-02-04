# FIN Crawler

## Milestone

 - [ ] KOSPI採用YAHOO FINANCE
 - [ ] N225採用YAHOO FINANCE
 - [ ] TOPIX採用YAHOO FINANCE
 - [ ] SHCOMP
 - [ ] TWSE
 - [ ] TWOTC
 - [X] SXXP 有代碼

## Prerequisite

 - Python 3.7 >
 - (Chromedriver >= 79)[https://chromedriver.chromium.org/downloads]


## Install

pip install -r requirements.txt

## How to start to parse?

python src/main.py `{spider_name}` e.g ewy, etc.

## Docker

### MySQL

- (Create a user with remotely accessible connect)[http://itman.in/en/mysql-add-user-for-remote-access/]
- (Grant the user privileges)[https://chartio.com/resources/tutorials/how-to-grant-all-privileges-on-a-database-in-mysql/]

### env for the crawler container

DB_NAME=trading_club
DB_USER=xxx
DB_PASS=xxx
DB_HOST=db
DB_PORT=3306
