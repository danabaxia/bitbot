# CS411 Database System Course Project Bitbot [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)]

## Introduction
This project is to design a web-based cryptocurrency trading bot. The website designed to recognize the crypto-market’s trends and automatically execute trades based on customer’s configurable trading algorithms.

## Motivation
### Booming market
Bitcoin is a purely peer-to-peer version of electronic cash that would allow online payments to be sent directly from one party to another without going through a financial institution. As the most acceptable digital currency, bitcoin’s price has skyrocketed, especially 2017 after bitcoin hit historical high peak at nearly $20,000, people all around the world have been clamoring to trade in bitcoin and other altcoins, investors continued to pump money into cryptocurrency and blockchain startups. 

### Problem and Solution
The problem with any commodity in the global marketplace is traders cannot be at their station 24 hours a day, 7 days a week. Apple co-founder and tech guru Steve Wozniak recently admitted that he had sold his entire holdings of bitcoin because he had grown tired of constantly looking to see what the price was. Even the most dedicated trader will not want to spend their entire life staring at cryptocurrency price charts either. Trading in cryptocurrencies is particularly addictive because the market is highly volatile. Bitcoin prices can and have dropped by as much as 25% in a day. While investors who are in for the long term might not worry about taking advantage of such fluctuations, cryptocurrency traders can make huge amounts of money from such volatility.

The solution to this problem is the automated trading bot. Such bots have been used by companies to set buy/sell commodities on global stock exchanges for decades. Trading bots help to automate the process and thereby relieving pressure on companies and traders. Trading bots are software programs that use API’s to interact with financial exchanges. They actively monitor exchanges around the clock and will react in accordance to whatever predetermined criteria they have been programmed with.

### Robinhood business model analysis
Robinhood is one of the most popular crypto and stock trading platform. It doesn’t charge any fees for trading stocks and ETFs, and claims to extend that facility to cryptocurrencies as well. However, several reviewers have pointed to Robinhood’s Crypto User Agreement where it notes that the platform will pass on any fees charged by intermediaries to the user. Users also claim that these fees are already included in the price of the cypto that’s displayed to the trader[2]. 
Anther downside of trading on Robinhood is that it lacks of automation algorithms which can help traders to protect from sharp loss. In another word, Robin hood doesn’t solve the problem of price volatility. 


### Our business model 
We, here, offer a trading web service that provide its own trading algorithms and portfolio management services for the customers to grow their cryptocurrency assets and value. By offering functions such as strategy automation, real-time event notifications, back testing, etc., 




## Table of Contents

### Contents
<!-- MarkdownTOC depth=4 -->
- [Database Design](#database)
- [Data Source](#data)
- [Front-End Design](#front)
- [Back-End Design](#end)
- [Deployment](#deployment)

### Reference
- [FLASK](#flask)
- [Python](#python)
- [MySQL](#mysql)
- [MongoDB](#mongodb)
- [AWS](#aws)
- [Others](#others)


### [Team](#team)

<!-- /MarkdownTOC -->

<a name="database"></a>
#### Database Design
* [Database Design](https://github.com/WEIQIAN17/bitbot/blob/main/design.jpeg)

Based on the schema above, we are going to create totally 5 tables:

###### User table
for storing user id, name, hashed password, etc. User_id is the primary key of User table and it is also the foreign key for Transaction table and Product table.

##### Transaction table
for storing the information for each transaction. There is a transaction id as the primary key here.

#####
Product Table
we persist product information here. Product id is the primary key for this table. It is also the primary key for Strategy table.

##### Bitcoin Table
we save the bitcoin data in this table, for example, the bitcoin date, the different prices and volumes. Bitcoin date is the primary key here.

##### Strategy table
here we persist the strategy information including strategy name and algorithm. In this table, product id is the primary key.

##### Tool to Use for Database:
We’ve decided to implement our project by using MySQL. There are some reasons for why we chose MySQL for this project:
MySQL is compatible to run on many operation systems, such as Windows, Unix, Linux. Compatibility is important for this web-based bitcoin trading application as we need to ensure the application can run perfectly and persistently on various operation systems that our users currently using.
MySQL allows transactions to be rolled back, commit, and crash recovery. As every transaction of the bitcoin trading application is money-related, crash recovery is an extremely critical feature for this application. This application needs to be robust thus enabling users to trade anytime without worrying about the application crush.
MySQL is very secure as it keeps passwords encrypted. There is no doubt that financial information of our application needed to be stored in a secure database, MySQL can guarantee the security as needed.
MySQL can be integrated with different development tools that we will use for this project.
MySQL is one of the great open-source RDBMS databases. In addition, it’s free to use without additional cost.
MySQL works very good with the open-source ecosystem, can match with most of the framework.


<a name="data"></a>
#### Data Source
The main dataset will be the 682544  date samples of bitcoin price change per minute

<a name="front"></a>
#### Front-End Design
Front-End (Clint-side) Design
Website’s front end is everything customers see and can interact with using a browser. HTML and CSS and JavaScript are main tools used for the development. HTML is used for basic page structure and content, CSS is for visual editing, and JavaScript is for making websites interactive.
Web pages for React framework

###### Frame 1: LANDING PAGE
• The user will be able to sign in or register for the site 

###### Frame 2: DASHBOARD
• The user can view the current price for bitcoin
• When the user clicks Buy/Sell a modal will appear (pictured on the right) so the user can make a transaction
• The user will be able to see the amount of bitcoin they currently have
• Graphs created with randomized seed data for visualization)

###### Frame 3: TRANSACTION INDEX PAGE
• The user will be able to view all transactions for bitcoin
• Sorting functionality (Stretch Goal) (Chart created with randomized seed data for visualization) 

##### Frame 4: PROFILE PAGE
• The user will be able to update their user information

<a name="end"></a>
#### Back-End Design
LAMP (Linux, Apache, MySQL, PHP/Perl/Python) is a complete web development stack which is used widely, the choice of web framework is Flask written in Python. Flask is an API of Python that allows us to build up web-applications. It was developed by Armin Ronacher. Flask's framework is more explicit than Django's framework and is also easier to learn because it has less base code to implement a simple web-Application.

<a name="deployment"></a>
#### Deployment
Amazon EC2 provides resizable compute capacity in the cloud. It is designed to make web-scale cloud computing easier for developers and allows maximum scalability and availability for websites and web applications. Amazon EC2 changes the economics of computing by allowing you to pay only for capacity that you actually use.


<a name="references"></a>
## Reference
<a name="flask"></a>
#### FLASK
* [The FLASK Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins) 
* [FLASK Tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/) 
* [FLASK Web Development](https://flask.palletsprojects.com/en/2.0.x/) 

<a name="python"></a>
#### Python
* [Python](https://www.python.org/) 

<a name="aws"></a>
#### AWS
* [AWS](https://docs.aws.amazon.com/) 

<a name="mysql"></a>
#### MySQL
* [MySQL](https://www.mysql.com/) 
* [MySQL Workbench](https://www.mysql.com/products/workbench/)

<a name="mongodb"></a>
#### MongoDB
* [MongoDB](https://www.mongodb.com/) 

<a name="others"></a>
#### Others
* [Bitcoin: A Peer-to-Peer Electronic Cash System](https://git.dhimmel.com/bitcoin-whitepaper/) 
* [Robinhood Crypto Trading Platform](https://www.techradar.com/reviews/robinhood-crypto-trading-platform) 

<a name="team"></a>
## Team
* [Jialiang](https://github.com/jzhu118/bitbot)
* [Wei](https://github.com/WEIQIAN17/bitbot)

