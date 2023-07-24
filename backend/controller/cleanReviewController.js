const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken')
const config = require('../auth.config')
const  Review  = require('../model/raw_reviews');
const { Configuration, OpenAIApi } = require("openai");


router.post('/api/obtainCleanReview', async(req, res) => {
    const { token, productId } = req.body
    console.log(req.body)
    try{
        //check if user is verified/logged in
       jwt.verify(token, config.secret)

       //check if document already exists, if yes update tokens to be earned else create new document
       const doc = await Review.findOne({ productId }).lean()
       
       if(doc){
        const _id = doc._id;
        var rawReviews = doc.rawReviews
        var newReviews = []
        const configuration = new Configuration({
            apiKey: process.env.OPENAI_API_KEY,
          });
        const openai = new OpenAIApi(configuration);  

        var resp = [];

        for (var i in rawReviews) {
            var review = rawReviews[i]
            console.log(review)
            const item_quality_response = await openai.createChatCompletion({
                model: "gpt-3.5-turbo",
                "messages": [{"role": "system", "content": "Classify the item quality in one word based on its review  into one of the categories:'extremely poor', 'not bad', 'fair', 'good'. 'good' category means there are no flaws in the item and the customer  is completely satisfied with it.'fair' category means there are 1-2 flaws in the item but customer is overall satisfied with it.  'not bad' category means there are 1-2 flaws or more with the product and the customer expresses slight but not complete dissatisfaction from the tone of the review. 'poor' category means the product has multiple flaws and the customer expresses dissatisfaction and an overall negative perspective on his/her purchase. output format: [category]"}, {"role": "user", "content": review}]
              });
            const style_response = await openai.createChatCompletion({
                model: "gpt-3.5-turbo",
                "messages": [{"role": "system", "content": "Rate how stylish the product is from 1 to 5  based on the customer's review and feedback on how the clothing item looks on them. Increase the rating if the customer uses positive adjectives to describe the overall look and appearance of the item. Decrease the rating if the customer expresses negative feedback on the aspects of how the item has been crafted or it didnt look attractive .Your response should be an integer along with the negative aspect of the item that brought down its rating if there is any in 2-3 words . (for example , if review says the seams were unfinished ,the negative aspect should be 'unfinished seams'). Output format: [integer from 1 to 5]/5, [unfinished seams]"}, {"role": "user", "content": review}]
              });
            const fit_response = await openai.createChatCompletion({
                model: "gpt-3.5-turbo",
                "messages": [{"role": "system", "content": "classify the fit of the clothing item on the customer into one of the following categories: 'too loose', 'little loose', 'true to size', 'little tight', 'extremely tight' based on the review . If the customer does not give any feedback on the fit of the clothing , classify the fit as 'true to size' . Else, for example, if the customer mentions a top being lose for her, based on the tone and degree of adjectives used for expressing this negative aspect, classify it as 'too loose' or 'little loose'. output format : [1 of the 5 categories] do not provide any reasoning"}, {"role": "user", "content": review}]
              });
              item_quality = item_quality_response.data.choices[0].message.content
              style = style_response.data.choices[0].message.content
              fit = fit_response.data.choices[0].message.content
              resp.push(item_quality)
              resp.push(style)
              resp.push(fit)
              break
        }

        console.log(resp)

        // add logic to summon chatGPT APIs to get clean review given a raw review
        
        // await Review.updateOne({_id},
        //     { $set: { cleanReviews:  newReviews}})
        //     return res.json({status:'ok'})
        }
        else{   
            return res.json({status:'error', error:'Product not found'})
        }
    } catch(error){
        console.log(error)
            res.json({status:'error', error:'User token not verified'})
        } 
})

module.exports = router;