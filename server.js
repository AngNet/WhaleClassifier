//include requirement
var express = require('express');
var bodyParser = require('body-parser');

var port = process.env.PORT || 3000;

var app = express();
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

app.use('/', express.static('public'));


app.get('/testGet', function(req, res){
  'use strict';
  console.log('score');
  res.json({'this':'is A test'});

});

//------update score all the user score---------------
//IN: {userName:’someone’, score:1000}
app.post('/testPost', function(req, res){
  'use strict';

      console.log('Data');
      res.json('send some DATA!');
});//end score update

app.listen(port,'0.0.0.0',function(){console.log('!---- AWESOME SAUCE listening in '+ port+' ----!');});
