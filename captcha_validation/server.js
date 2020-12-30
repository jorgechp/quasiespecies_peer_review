const config = require('./config');

const express = require('express');
const cors = require('cors');
const bodyParser = require("body-parser");
const request = require("request");
const app = express();
const port = config.port;

/** AUTHOR
* https://medium.com/@samuelhenshaw2020/recaptcha-v2-in-angular-8-with-back-end-verification-with-nodejs-9574f297fdef
*/

var corsOptions = {
  origin: config.cors_origin,
  optionsSuccessStatus: 200 // some legacy browsers (IE11, various SmartTVs) choke on 204
}
app.use(cors(corsOptions))
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.post('/token_validate', cors(corsOptions), (req, res)=>{

      
  let token = req.body.recaptcha;
  const secretKey = config.recaptcha_secret_key; //the secret key from your google admin console;
  
  //token validation url is URL: https://www.google.com/recaptcha/api/siteverify 
  // METHOD used is: POST
  
  const url =  `https://www.google.com/recaptcha/api/siteverify?secret=${secretKey}&response=${token}&remoteip=${req.connection.remoteAddress}`
   
  //note that remoteip is the users ip address and it is optional
  // in node req.connection.remoteAddress gives the users ip address
  
  if(token === null || token === undefined){
    res.status(201).send({success: false, message: "Token is empty or invalid"})
    return console.log("token empty");
  }
  
  request(url, function(err, response, body){
    //the body is the data that contains success message
    body = JSON.parse(body);

    //check if the validation failed
    if(body.success !== undefined && !body.success){
         res.send({success: false, 'message': "recaptcha failed"});
         return console.log("failed")
     }
    
    //if passed response success message to client
    console.log("success");
     res.send({"success": true, 'message': "recaptcha passed"});
    
  })

})


app.listen(port, ()=>{
    console.log(`connected on port ${port}`)
})
