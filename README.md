# Ovid as a Service
This API provides programmatic access to Ovid's The Metamorphoses.

## Description
Ovid as a Service provides secure endpoints for:
* Full text search
* Entire books and chapters by number
* Random line, chapter, and book

The full text was scraped and cleaned from UVA's Ovid Project using `BeautifulSoup` and `spacy.` It is indexed line-by-line in a local `Whoosh` instance. The API was developed in the `FastAPI` framework. The whole thing is Dockerized and served from a free EC2 instance.

## Endpoints
`Base URL`
* `https://api.ovidasaservice.com`

`text`
* `v1/text?query={string}`  
Returns all lines matching your query sorted in their original order
* `v1/text/random`  
Returns a random line

`chapter`
* `v1/chapter?query={int}`  
Returns all chapters matching `int` value
* `v1/chapter/random`  
Returns a random chapter

`book`
* `v1/book?query={int}`  
Returns entirety of the book matching `int` value, sorted in its order order 
* `v1/book/random`  
Returns entirety of a random book  

`Example`:  
>`curl -X  GET 'https://api.ovidasaservice.com/v1/text?query=io'`  

Returns:
>`{"count":61,"results":[{"book":"1","chapter":"24","chapter_name":"Inachus mourns for Io","line":"247","text":"There is a grove in Haemonia, closed in on every side by wooded cliffs."}...],"credits":"This A.S. Kline translation of Ovid's The Metamorphoses was scraped from University of Virginia Library's Ovid Collection. See more: https://ovid.lib.virginia.edu/about.html. Labor ipse voluptas."}`
  
## Authors and acknowledgements
* tal.noznisky@gmail.com
* University of Virgina Library Ovid Project
* A.L. Kline trans. of Ovid's The Metamorphoses  

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
