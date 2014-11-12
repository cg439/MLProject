MLProject
=========
To use the scraper, set the amazon product id, begin page and end page fields in the script.

Then run:

node scraper.js > outputFileName.txt

This will run the script, and pipe any console output to a txt file with the given name.

If you just want to test that it works just run

node scraper.js

Note it takes some time to do the HTTP requests so if you try to parse a lot of pages it will take a little while.
