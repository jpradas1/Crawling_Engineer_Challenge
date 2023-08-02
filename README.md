# Crawling Engineer Challenge

This repository extract data from the clothing website [Puma](https://eu.puma.com/) using the python framework Scrapy. This scraper has one spiders, and extracts the following data, i.e.:
- Product id
- Product title
- Product brand
- Product description.
- Product current price
- Product original price
- Product availability
- A list of all the image URLs
- Product URL
- All available colors for the product
- All available sizes for the product
- Category paths leading to the product (e.g. Women > Footwear > Running)

## Running the Code
To run this scraper properly, follow these steps.
### Virtual Environment
First we need a virtual environment to display this project. We could use conda or the python module venv. We use the last one.
```
python -m venv venv
```
To active this environment
- Linux case:
```
source venv/bin/activate
```
- Windows case:
```
venv\Scripts\activate
```
### Installing Libraries
```
pip install scrapy pymongo
```
### Ride Spiders
Before to run any spider we need a MongoDB server in order to store our data. This server could be local or on cloud. To create a local one, use docker.
```
sudo docker pull mongo
sudo docker run -d -p 27017:27017 --name mongodb mongo
```
- Puma scraper.
Because puma crawler needs the Mongo server, we run:
```
scrapy crawl -s MONGODB_URI="mongodb://localhost:27017/" -s MONGODB_DATABASE="Products" puma
```
And to ignore the log output
```
scrapy crawl -s MONGODB_URI="mongodb://localhost:27017/" -s MONGODB_DATABASE="Products" puma 2>/dev/null
```
## Dataset
The final extrated data is located in the compress file [products](https://github.com/jpradas1/Crawling_Engineer_Challenge/blob/main/products.tar.gz) which contains all data extracted from the website, storing 24544 items.
```
tar -xzvf products.tar.gz
```
