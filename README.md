# Crawling Engineer Challenge

This repository extract data from two clothing websites [Adidas](https://www.adidas.es/) and [Puma](https://eu.puma.com/) using the python framework Scrapy. This scraper has two spiders, and extracts the same data from both websites, i.e.:
- Product title
- Product brand
- Product description.
- Product current price
- Product original price
- Product availability
- A list of all the image URLs
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
Finally to run the scraper we make
- Adidas scraper
```
scrapy crawl adidas
```
- Puma scraper
```
scrapy crawl puma
```
## Dataset
The final extrated data is located in the folder [retailing](https://github.com/jpradas1/Crawling_Engineer_Challenge/tree/main/retailing) in json format ([adidas.json](https://github.com/jpradas1/Crawling_Engineer_Challenge/blob/main/retailing/adidas.json) & [puma.json](https://github.com/jpradas1/Crawling_Engineer_Challenge/blob/main/retailing/puma.json))
