var jsdom = require('jsdom');

//example ASIN
//fill in id for the Amazon product
//page for initial page to begin grabbing reviews from
//page for last page to grab reviews up to
//sort is either bySubmissionDate or byPopularity and can be Ascending or Descending
var id = "B008CS5ZRU",
    page = 1,
	endPage = 1,
	sort = "bySubmissionDateDescending";

var scrape = function(page, endPage) {
	var temp = "";
	var num = 1;
    jsdom.env(
        "http://www.amazon.com/product-reviews/" + id + 
        "/? ie=UTF8&showViewpoints=0&pageNumber=" + page +
        "&sortBy="+sort,
        ["http://code.jquery.com/jquery.js"],
        function (errors, window) {
            var $ = window.jQuery;  
            var productReviews = $('#productReviews');
			if(productReviews.length > 0){
				productReviews.find('td').children('div:lt(10)').each(function() {
					var starRating = $(this).find('span:first').text();
					if(starRating != ""){
					var helpful = $(this).find('span:first').parent().prev().text();
					var date = $(this).find('span:first').next().find('nobr').text();
					var title = $(this).find('span:first').next().find('b').text();
					var reviewerName = $(this).children().next().find('a:first').find('span').text();

					var reviewBlock = $(this).find("[class='reviewText']").text();
					var review = $.trim(reviewBlock);
					$(this).children().remove();
					
				
				  console.log('-----------------------');
				  console.log('Title: ' + title  + '\nDate: ' + date + '\nHelpfulness:' + $.trim(helpful) + '\nReviewer:' + reviewerName + '\nRating: ' + starRating + '\nReview:' + review + '\n\n');
				 // temp += parseReview(title, date, helpful, starRating, review, num, page, endPage);
				 //temp += parseAverageReview(date, starRating, num, page, endPage);
				  }
				  num++;
            });}
			console.log(temp);
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
if(num == 10 && page == endPage)
	output +=  ' }]}';
else
	output +=  ' } , ';
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
	if(num == 10 && page == endPage)
		output +=  ' }]}';
	else
		output +=  ' } , ';
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

//loop until all pages have been parsed
while(page <= endPage){ 
	scrape(page, endPage);
	page++;
}