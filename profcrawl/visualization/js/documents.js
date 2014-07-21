/**
 * Responsible for visualizing a collection of documents and their statistics.
 */ 
var metaDataJson;
var keymap;
var docmap;
var currentKey;
var currentDataset;
/**
 * Return the url to the given bz.
 */
function constructUrl(id) {
	return docmap[id]['url'] + id;
}

function getIdsFromKey(key) {
	return keymap[key];
}

function makedocs(keys) {
	console.log('making docs table');
	var table = $('#docsmapBody');
	$.each(keys, function(i,el) {
        	makeDocEntry(table, el);
    	});
}

function loadDataset(dataset) {
 	var path = ' data/' + dataset + '/docmap.json';
 	console.log('Loading' + path);
 	if (docmap == null) {
	 	 $.getJSON(path,
	    	function(data) {
	        docmap = data;
	    });	
 	} else {
 		console.log('documents already loaded');
 	}
 	console.log(JSON.stringify(docmap, undefined, 2))
 	makedocs(Object.keys(docmap));
 }

function makeDocEntry(parent, element) {
	var doc = docmap[element];
	var id = doc['id'];
	var keywords = doc['keywords'];

	parent.append('<tr><th><a href="'+ 
		constructUrl(element) + '">' + 
		element +'</a></th><td id="' + element + '"></td></tr>');

	var top5 = makeTopWords(keywords.slice(0,5));
	parent.find('#' + element).append(top5);	
}

function makeTopWords(keywords) {
	var top = $('<table class="inner"></table>');
	for (var word in keywords) {
		var key = keywords[word][0];
		var score = keywords[word][1];

		var rowNode = $('<tr></tr>');

		var wordNode = $('<td id="' + 
			key + '" class="word"><a href="">' + 
			key + '</a></td>');

		var scoreNode = $('<td>' + 
			score + 
			'</td>');

		wordNode.on("click", function(){
			var word = $(this).attr('id');
			$(this).append(transitionToKeyMap(word));
		});

		rowNode.append(wordNode);
 		rowNode.append(scoreNode);
		top.append(rowNode);
	}
	return top;
}

function transitionToKeyMap(key) {
    localStorage.setItem('_current_key', key);
    console.log('hey:' + key);
	location.href = 'keyToId.html';
}

$(document).ready(function() {
	currentDataset = localStorage.getItem('_current_dataset');
	loadDataset(currentDataset);
});
