# comentariosg1

Spider to scrape comments of G1 news.

# Run

## Create a virtualenv and source it (recommended)

`python -m venv .venv`

`source .venv/bin/activate`

## Install dependencies

`pip install -r requirements.txt`

## Run the spider

`scrapy crawl g1comments -o comments.jsonlines`

The data will be available on a new file called `comments.jsonlines`.

### Spider parameters

You can pass some parameter to choose which urls/categories you want to scrape.

Use the parameter `-a` to pass these parameters to the spider.

`scrapy crawl g1comments -o comments.jsonlines -a PARAMETER_NAME=PARAMETER_VALUE`

Available parameters:

`max_pages` - Limits the number of page with news to be scraped. (Default is 10 pages with 10 news each)

`category_url` - Category url to be scraped (Eg: `https://g1.globo.com/planeta-bizarro/`)

`news_url` - Single news url to be scraped

# Analyse scraped data

To import the data to further analysis I suggest using Pandas, it is not covered on this README as I am no expert in this area.

## Create a dataframe with the scraped data

```
import pandas as pd
df = pd.read_json('comments.jsonlines', lines=True).set_index('id').fillna('')
```

Variable `df` will contain the dataframe with comments.

Enjoy!
