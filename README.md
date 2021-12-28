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
* `v1/text?query={str}`  
Returns all lines matching your query sorted in their original order

`chapter`
* `v1/chapter?query={str}`  
Returns all chapters with titles matching `str` value

`book`
* `v1/book/int`  
* Note: `book` can also accept optional text and chapter query params to search for text and/or chapter number within a book
`v1/book/{int}?query={str}&chapter={int}`

`random`
* `v1/random/{resource}`  
`resource` param can be one of the following values: `line`, `chapter`, or `book`

## Example  
`book` endpoint:
>`curl -X  GET 'https://api.ovidasaservice.com/v1/book/1?query=io&chapter=24'`  

Returns:
>`{"count":9,"results":[{"book":"1","chapter":"24","chapter_name":"Inachus mourns for Io","line":"247","text":"There is a grove in Haemonia, closed in on every side by wooded cliffs."}...],"credits":"This A.S. Kline translation of Ovid's The Metamorphoses was scraped from University of Virginia Library's Ovid Collection. See more: https://ovid.lib.virginia.edu/about.html. Labor ipse voluptas."}`

`random` endpoint:
>`curl -X  GET 'https://api.ovidasaservice.com/v1/random/line'`

Returns:
>`{"count":1,"results":[{"book":"2","chapter":"33","chapter_name":"Aglauros is turned to stone","line":"763","text":"Nor was she white stone:"}],"credits":"This A.S. Kline translation of Ovid's The Metamorphoses was scraped from University of Virginia Library's Ovid Collection. See more: https://ovid.lib.virginia.edu/about.html. Labor ipse voluptas."}`

## Authors and acknowledgements
* tal.noznisky@gmail.com
* University of Virginia Library Ovid Collection - thank you for the transcription!
* A.L. Kline trans. of Ovid's The Metamorphoses  

## License
This project is licensed under the MIT License - see the LICENSE.md file for details
