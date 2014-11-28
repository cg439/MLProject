var jsdom = require('jsdom');
//first argument is the mode of scraping, value inputted should be either "-p" or "-r" for product scraping or review scraping respectively
//second argument must be Amazon Product ID
//third argument is the first page to begin scraping from, a numerical number is expected > 0 but less than the last page of available reviews
//fourth argument is last page to scrape up to for the product review, must be greater than begin page value
//fifth argument is the ranking criteria for ordering pages when scraping, "-d" for date, "-p" for popularity
//sixth argument is the order in which the criteria is ordered, either "-a" for ascending or "-d" for descending
var id, mode, page, endPage, sortMethod, sortOrder;

function die(message) {
	console.log(message);
	throw '';
}

function printHelpMessage() {
	console.log("Expected usage follows following format");
	console.log("node scraper.js [mode = -r || -h] [Amazon Product ID] [entryPageNumber] [exitPageNumber] [sortCriteria = -d || -p] [sortOrder = -a || -d]");
	console.log('First argument is the mode of scraping, value inputted should be either "-p" or "-r" for product scraping or review scraping respectively');
	console.log("Second argument must be Amazon Product ID");
	console.log("Third argument is the first page to begin scraping reviews from");
	console.log("Fourth argument is last page to scrape up to for the product review, must be greater than begin page value");
	console.log('Fifth argument is the ranking criteria for ordering pages when scraping, "-d" for date, "-p" for popularity');
	console.log('Sixth argument is the order in which the criteria is ordered, either "-a" for ascending or "-d" for descending');
	die('Incorrect parameters, please try again. Exiting...');
}

function processInputs() {
	if (process.argv.length < 4 || process.argv[2] == "-h") {
		printHelpMessage();
	}
	else {
		mode = process.argv[2];
		id = process.argv[3];
		if (mode == "-r") {
			page = process.argv[4];
			endPage = process.argv[5];
			sortMethod = process.argv[6];
			sortOrder = process.argv[7];
			if (sortMethod == "-d") {
				sortMethod = "bySubmissionDate";
			}
			else if (sortMethod == "-p"){
				sortMethod = "byPopularity";
			}
			else {
				printHelpMessage();
			}
			if (sortOrder == "-d") {
				sortOrder = "Descending";
			}
			else if (sortOrder == "-a") {
				sortOrder = "Ascending";
			}
			else {
				printHelpMessage();
			}
		}
		else if (mode != "-p") {
			printHelpMessage();
		}
	}
};




processInputs();

var	reviewURL = "http://www.amazon.com/product-reviews/" + id + 
        "/?ie=UTF8&showViewpoints=0&pageNumber=",
	productURL = "http://www.amazon.com/dp/" + id;
	
var scrapeReviews = function(page, endPage) {
	var temp = "";
	var num = 1;
    jsdom.env(
        reviewURL + page +
        "&sortBy="+sortMethod+sortOrder,
        ["http://code.jquery.com/jquery.js"],
        function (errors, window) {
            var $ = window.jQuery;  
            var productReviews = $('#productReviews');
			if (productReviews.length > 0) {
				productReviews.find('td').children('div:lt(10)').each(function() {
					var starRating = $(this).find('span:first').text();
					if (starRating != "") {
						var helpful = $(this).find('span:first').parent().prev().text();
						var date = $(this).find('span:first').next().find('nobr').text();
						var title = $(this).find('span:first').next().find('b').text();
						var reviewerName = $(this).children().next().find('a:first').find('span').text();

						var reviewBlock = $(this).find("[class='reviewText']").text();
						var review = $.trim(reviewBlock);
						$(this).children().remove();
						
					
					//console.log('-----------------------');
					//console.log('Title: ' + title  + '\nDate: ' + date + '\nHelpfulness:' + $.trim(helpful) + '\nReviewer:' + reviewerName + '\nRating: ' + starRating + '\nReview:' + review + '\n\n');
					console.log(review);
					// temp += parseReview(title, date, helpful, starRating, review, num, page, endPage);
					//temp += parseAverageReview(date, starRating, num, page, endPage);
					}
				num++;
				});
			}
			console.log(temp);
            window.close();
        }
    )        
};


var scrapeProductDescription = function() {
    jsdom.env(
        productURL,
        ["http://code.jquery.com/jquery.js"],
        function (errors, window) {
            var $ = window.jQuery;  
            var product = $('#productDescription');
			var wrapper = product.find("[class='productDescriptionWrapper']");
			console.log(wrapper.text());
            window.close();
        }
    )        
};


var parseAverageReview = function(date, star, num, page, endPage){
	//begin bracket for review
	var output = "{ ";

	//splits date which is in format 'month day, year' around spaces for easy access to month and year
	var dateSplit = date.split(" ");

	//outputs the month and year variables in accordance with json
	output += '"month": "' + dateSplit[0] +'", ';
	output += '"year": ' + dateSplit[2] + ', ';

	//outputs rating
	output += '"rating": ' + star.substring(0,1);
	if (num == 10 && page == endPage) {
		output +=  ' }]}';
	}
	else {
		output +=  ' } , ';
	}
	return output;
}


var parseReview = function (title, date, helpful, rating, review, num, page, endPage){
	var output = "{ ";
	//output += '"title": "' + title +'", ';
	output += '"date": "' + date +'", ';
	var begin = helpful.indexOf("of");
	var end = helpful.indexOf("people");
	var impact = parseFloat(helpful.substring(begin+3, end-1));
	var helpful = parseFloat(helpful.substring(0, begin-1));
	var helpfulRatio = helpful/impact;
	output += '"impact": ' + impact + ', "helpful": ' + helpfulRatio + ', ';
	output += '"rating": ' + rating.substring(0,1);
	//output += '"review": "' + review.replace('"', '');
	if (num == 10 && page == endPage) {
		output +=  ' }]}';
	}
	else {
		output +=  ' } , ';
	}
	return output;
}

//Text for parsing reviews already existing in a separate file
var parse = function(str) {
	if(str.indexOf("Title:") != -1)
		return '"title": "' + str.trim(str.substring(6))+'", ';
	else if(str.indexOf("Date:") != -1)
		return '"date": "' + str.trim(str.substring(5)) +'", ';
	else if(str.indexOf("Helpfulness:") != -1){
		var output = "";
		var temp = str.trim(str.substring(12));
		var begin = temp.indexOf("of");
		var end = temp.indexOf("people");
		var impact = temp.substring(begin+3, end-1);
		var helpful = temp.substring(0, begin-1);
		var helpfulRatio = parseInt(helpful)/parseFloat(impact);
		return '"impact" : ' + impact + ', "helpful" : ' + helpfulRatio + ', ';
	}
	else if(str.indexOf("Rating:") != -1)
		return '"rating" : ' + str.substring(8,9) + ', ';
	else if(str.indexOf("Review:") != -1)
		return '"review" : "' + str.substring(7) + '" } , '
	else if(str.indexOf("-----------------------") != -1)
		return "{";
	else
		return "";
}


//insert initial text for the block
//console.log('{ "reviews": ['); 
if (mode == "-r") {
	//loop until all pages have been parsed
	while(page <= endPage){ 
		scrapeReviews(page, endPage);
		page++;
	}	
}
else {
	scrapeProductDescription();
}
