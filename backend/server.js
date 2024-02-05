const express = require('express')
const path = require('path')
const bodyParser = require('body-parser')
const mongoose = require('mongoose')
const userController = require('./controller/userController.js');
const rawReviewsController = require('./controller/rawReviewsController.js');
const cleanReviewsController = require('./controller/cleanReviewController.js');
require('dotenv').config();


mongoose.connect('mongodb+srv://ishita201:techfest2024@cluster0.u4xfcnl.mongodb.net/Market_Assist?retryWrites=true&w=majority',
 { serverApi: { version: '1', strict: true, deprecationErrors: true } });
const app = express()

app.use('/', express.static(path.join(__dirname, 'static')))
app.use(bodyParser.json({limit: '200mb'}))

app.use('/users', userController);
app.use('/rawReviews', rawReviewsController);
app.use('/cleanReviews', cleanReviewsController);

app.listen(9999, () =>{
    console.log('Server up at 9999')
})