const express = require('express')
const path = require('path')
const bodyParser = require('body-parser')
const mongoose = require('mongoose')
const userController = require('./controller/userController.js');
const rawReviewsController = require('./controller/rawReviewsController.js');
const cleanReviewsController = require('./controller/cleanReviewController.js');
require('dotenv').config();


mongoose.connect('mongodb://localhost:27017/Marketing_Assist_Dashboard', {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
const app = express()

app.use('/', express.static(path.join(__dirname, 'static')))
app.use(bodyParser.json())

app.use('/users', userController);
app.use('/rawReviews', rawReviewsController);
app.use('/cleanReviews', cleanReviewsController);

app.listen(9999, () =>{
    console.log('Server up at 9999')
})