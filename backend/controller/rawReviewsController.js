const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken')
const config = require('../auth.config')
const  Review  = require('../model/raw_reviews');
// let fashionData = require('../womens_clothing_reviews_clean.json');


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

router.get('/api/getRawReviews/:productId/:token', async (req, res)=>{
    const productId = req.params.productId
    const token = req.params.token
    try{
        jwt.verify(token, config.secret)
        const doc = await Review.findOne({ productId }).lean()
        return res.send(doc.rawReviews);
    }
    catch(err){
        console.log(err)
        res.json({status:'error', error: err})
    } 
});

router.post('/api/createDatabase', async(req, res) => {
    const { username, data } = req.body
    fashionData = JSON.parse(data)
    try{
            if(!username || typeof username !== 'string'){
                return res.json({status:'error', error:'Invalid username'})
            }

            for (var key in fashionData) {
                value = fashionData[key];
                var ages = value.reviewer_age
                var upvotes = value.upvotes
                var recommend = value.recommend
                var ratings = value.ratings
                var productCategory = value.product_category
                var reviews = value.reviews
                const response = await Review.create({
                    "username": username, "productId":key, "productCategory": productCategory, 
                    "reviewerAge":ages, "upvotes":upvotes,"recommend":recommend,"ratings":ratings, 
                    "rawReviews":reviews
                    })
                console.log(response)
            }
            return res.json({ status: 'ok' })
        }
    
    catch(error){
        console.log(error)
            res.json({status:'error', error:'Error'})
        }
})


module.exports = router;