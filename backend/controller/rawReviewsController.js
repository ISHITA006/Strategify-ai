const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken')
const config = require('../auth.config')
const  Review  = require('../model/raw_reviews');

router.post('/api/addRawReview', async(req, res) => {
    const {token, username, review } = req.body
    console.log(req.body)
    try{
      
        //check if user is verified/logged in
       jwt.verify(token, config.secret)

       //check if user document already exists, if yes update tokens to be earned else create new document
       const user = await Review.findOne({ username }).lean()
       
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
        
            if(!review || typeof review !== 'string'){
                return res.json({status:'error', error:'Invalid review'})
            }

            const rawReviews = [review]
            
            const response = await Review.create({
                username, rawReviews
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


module.exports = router;