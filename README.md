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

# Analyse scraped data

To import the data to further analysis I suggest using Pandas, it is not covered on this README as I am no expert in this area.

## Create a dataframe with the scraped data

```
import pandas as pd
df = pd.read_json('comments.jsonlines', lines=True).set_index('id').fillna('')

```

Variable `df` will contain the dataframe with comments.

Enjoy!
