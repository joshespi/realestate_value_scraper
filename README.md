# Property Value Scraper
## Requirments

requires docker engine is installed

requires a .env file that has the following variables with URLs to the property you're wanting to track on Zillow and Redfin.

```
ZILLOW_URL=
REDFIN_URL=
```

## Build
```docker build -t property-scraper .```

## Run

```docker run --rm -d -v "$(pwd):/app/data" property-scraper```

this run command binds the data folder to the current running folder so that the output gets synced to the host machine.


## Notes

Looks like Zillow is changing the span classes so i'll need to think through a solution to handle that automagically. 