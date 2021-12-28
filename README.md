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

`lines (AKA full text search)`
* `v1/lines?query={string}`  
Returns all lines matching your query sorted in their original order
* `v1/lines/random`  
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
  
## Authors and acknowledgements
* tal.noznisky@gmail.com
* University of Virgina Library Ovid Project
* A.L. Kline trans. of Ovid's The Metamorphoses  
`Labor ipse voluptas`

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
