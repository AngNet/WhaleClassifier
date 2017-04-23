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


app.post('/testPost', function(req, res){
  'use strict';

      console.log('Data');
      res.json('send some DATA!');
});

app.post('/testPost', function(req, res){
  'use strict';

      console.log('Data');
      res.json('send some DATA!');
});

app.listen(port,'0.0.0.0',function(){console.log('!---- AWESOME SAUCE listening in '+ port+' ----!');});
