//include requirement
var express = require('express');
var fileUpload = require('express-fileupload');
var bodyParser = require('body-parser');
var router = express.Router();

var port = process.env.PORT || 80;

var app = express();

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(fileUpload());

app.use('/', express.static(__dirname + '/public'));

// simple get method
app.get('/testGet', function(req, res){
  'use strict';
  res.json({'this':'is A test'});

});

// post image to server and save it as filename.jpg
app.post('/upload', function(req, res) {
	console.log(req.files);
  if (!req.files)
  {
  	console.log("no file");
    return res.status(400).send('No files were uploaded.');
 	}
  // The name of the input field (i.e. "sampleFile") is used to retrieve the uploaded file 
  var sampleFile = req.files.sampleFile;
 
  // Use the mv() method to place the file somewhere on your server 
  sampleFile.mv('./imgs/filename.jpg', function(err) {
    if (err)
      return res.status(500).send(err);
 
    res.send('File uploaded!');
  });
});



app.listen(port,'0.0.0.0',function(){console.log('!---- AWESOME SAUCE listening in '+ port+' ----!');});
