# Property Value Scraper
## Requirments

requires docker engine is installed

requires a .env file that has the following variables for your property

```
ZILLOW_URL=
REDFIN_URL=
```

## Build
```docker build -t property-scraper .```

## Run

```docker run --rm -d -v "$(pwd):/app/data" property-scraper```

this run command binds the data folder to the current running folder so that the output gets synced to the host machine.