const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken')
const config = require('../auth.config')
const  Review  = require('../model/raw_reviews');
let jsonData = require('../reviews_clean.json');


router.post('/api/addRawReview', async(req, res) => {
    const {token, username, productName, productId, review } = req.body
    console.log(req.body)
    try{
        //check if user is verified/logged in
       jwt.verify(token, config.secret)

       //check if user document already exists, if yes update tokens to be earned else create new document
       const user = await Review.findOne({ productId }).lean()
       
       if(user){
        const _id = user._id;
        var oldReviews = user.rawReviews
        oldReviews.push(review)
        await Review.updateOne({_id},
            { $set: { rawReviews:  oldReviews}})
            return res.json({status:'ok'})
        }
        else{

            if(!username || typeof username !== 'string'){
                return res.json({status:'error', error:'Invalid username'})
            }

            if(!productName || typeof productName !== 'string'){
                return res.json({status:'error', error:'Invalid productName'})
            }

            if(!productId || typeof productId !== 'number'){
                return res.json({status:'error', error:'Invalid productId'})
            }
        
            if(!review || typeof review !== 'string'){
                return res.json({status:'error', error:'Invalid review'})
            }

            var rawReviews;

            if (typeof review == 'string'){
                rawReviews = [review]
            }
            else{
                rawReviews = review
            }
            
            
            const response = await Review.create({
                username, productName, productId, rawReviews
            })
            console.log(response);
            return res.json({ status: 'ok' })
        }
    
    } catch(error){
        console.log(error)
            res.json({status:'error', error:'User token not verified'})
        } 
})

router.get('/:username', (req, res)=>{
    const username = req.params.username
    
    Review.findOne(username, (err, doc) => {
        if(!err){ res.send(doc.rawReviews); }
        else{ console.log('Error in Retreiving student :' + JSON.stringify(err, undefined, 2)); }
    });
});


router.post('/api/createTempDatabase', async(req, res) => {
    const { username } = req.body
    try{
            if(!username || typeof username !== 'string'){
                return res.json({status:'error', error:'Invalid username'})
            }

            for (var key in jsonData) {
                value = jsonData[key];
                var price = Number(value.price)
                var id =value.id
                var reviews = value.reviews
                const response = await Review.create({
                    "username": username, "productId":id, "productName":key,  "price":price, "rawReviews":reviews
                    })
                console.log(response)
            }
            return res.json({ status: 'ok' })
        }
    
    catch(error){
        console.log(error)
            res.json({status:'error', error:'User token not verified'})
        } 
})


module.exports = router;