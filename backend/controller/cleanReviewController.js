const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken')
const config = require('../auth.config')
const  Review  = require('../model/raw_reviews');
// const { Configuration, OpenAIApi } = require("openai");
const { TextServiceClient } = require("@google-ai/generativelanguage").v1beta2;
const { GoogleAuth } = require("google-auth-library");




router.post('/api/obtainCleanReview', async(req, res) => {
    const { username, productId } = req.body
    console.log(req.body)
    try{
        //check if user is verified/logged in
      //  jwt.verify(token, config.secret)

       //check if document already exists, if yes update tokens to be earned else create new document
       const doc = await Review.findOne({ username, productId }).lean()
       
       if(doc){
        if(doc.summary){
          const response = {"cleanReviews": doc.cleanReviews, "summary": doc.summary}
          return res.json(response)
        }
        const _id = doc._id;
        var rawReviews = doc.rawReviews
        var ratings = doc.ratings
        var upvotes = doc.upvotes
        var recommend = doc.recommend
        var newReviews = []
        const MODEL_NAME = "models/text-bison-001";
        const API_KEY = process.env.PALM_API_KEY;
        const base_prompt = "You are a customer feedback interpreter. When the user provides a customer review for a women's clothing product as an input, you are to perform the following tasks using it to help the user understand the review: \n\n 1. Classify the material quality of the item into one of the categories: 'extremely poor', 'not bad', 'fair', 'good', 'excellent'. If the customer does not mention anything regarding the fabric or material of the product, classify material quality as 'NA'. Else, in the above mentioned order, the 5 categories reflect low to high level of satisfaction with the material of the item. 'excellent' category means that the customer is extremely satisfied with the fabric or the material of the item and is indicated by very positive comments about the fabric. 'good' category means that the customer is happy with the fabric or the material of the item and is indicated by moderately positive comments about the fabric. 'fair' category means that the customer is neither too happy not too disappointed with the fabric or the material of the item; there might be some flaws as well as some positive feedback about the fabric, but the customer is overall satisfied with the product. 'not bad' category means there are 1-2 flaws or more with the material of the product and the customer expresses slight but not complete dissatisfaction from the tone of the review. 'poor' category means the fabric has multiple flaws and the customer expresses dissatisfaction and an overall negative perspective on her purchase. \n output format: [category] or 'NA' \n\n 2. Rate how stylish the product is from 1 to 5 based on the customer's review and feedback on how the clothing item looks on them. If the customer does not mention anything about the style of the item or it looks on them, output 'NA'. Else, increase the rating if the customer uses positive adjectives to describe the overall look and appearance of the item. Decrease the rating if the customer expresses negative feedback on the aspects of how the item has been crafted or it didn't look attractive. Your response should be an integer along with the aspect of the item that brought  its rating up or down in 2-3 words . (for example , if review says the seams were unfinished ,the aspect should be 'unfinished seams'). this aspect can be positive or negative. \n Output format: [integer from 1 to 5] & [aspect] or 'NA' \n\n 3. classify the fit of the clothing item on the customer into one of the following categories: 'too loose', 'little loose', 'true to size', 'little tight', 'extremely tight' based on the review . If the customer does not give any feedback on the fit of the clothing , classify the fit as 'NA' . Else, for example, if the customer mentions a top being lose for her, based on the tone and degree of adjectives used for expressing this negative aspect, classify it as 'too loose' or 'little loose'. If the customer expresses that the product fits perfectly and expresses a positive review about the fit , classify as 'true to size'. \n output format: [1 of the 5 categories] or 'NA' \n\n 4. classify the delivery times of the product based on its review into one of the following categories: 'early', 'on-time', 'late'. If the customer does not mention anything regarding the delivery of product aspect, classify delivery time as 'NA'. Else, based on the feedback and adjectives used , classify as 'early' or 'late'. But if the customer expresses a positive review about the delivery time , then classify as 'on time'. \n output format : [1 of the 3 categories] or 'NA' \n\n 5. Classify whether a product was a value for money purchase for a customer as 'yes' or 'no' categories based on its review. If the customer mentions a significant flaw in the making of the item that may make it impractical to use with a very negative tone and expresses repeated dissatisfaction with the product's appearance and feel using strong adjectives, classify it as 'no'. feedback on the fit of the item is not a factor to consider. Give importance to the tone of the review and how positive the overall feedback is. Most important factor is whether the particular customer would buy such a suit again or would recommend it to others. \n output format : [yes or no category] or 'NA' \n\n 6. Rate the customer service of the clothing company based on its product reviews on a scale of 1 to 5 if the customer gives any feedback on it in the review, else if it is not mentioned , output should be 'NA'. Customer service includes any feedback on the responsiveness and helpfulness of staff to customer enquiries post purchase of the item. The more negative the feedback on customer service: the lower is the rating. If the customer praises the customer service and expresses a completely positive feedback , rate it as 5. assess the degree of adjectives and tone of the description. the output should include one aspect the customer mentioned about the customer service, positive or negative in 2-3 words if there is any. \n output format: [integer between 1 to 5] & [aspect] or 'NA' \n\n perform these 6 tasks one by one for the user input and just give the output in the format as mentioned, without any additional reasoning. \n\n Here are 2 examples of the task: \n\n Review - 'Love this dress!  it's sooo pretty.  i happened to find it in a store, and i'm glad i did bc i never would have ordered it online bc it's petite.  i bought a petite and am 5'8.  i love the length on me- hits just a little below' \n Output - '1. good \n 2. 5 & pretty and petite \n 3. true to size \n 4. NA \n 5. yes \n 6. NA \n \n\n Review - 'Material and color is nice.  the leg opening is very large.  i am 5'1 (100#) and the length hits me right above my ankle.  with a leg opening the size of my waist and hem line above my ankle, and front pleats to make me fluffy, i think you can imagine that it is not a flattering look.  if you are at least average height or taller, this may look good on you.' \n Output - '1. good \n 2. 1 & leg opening too big, fluffy look \n 3. too loose \n 4. NA \n 5. no \n 6. NA \n \n\n Generate an output in the same format as explained for the following review: Review - '"
        var summary = {
        "quality": {"extremely poor":0, "not bad":0, "fair":0, "good":0, "excellent":0, "NA":0},
        "style": {"0":0, "1": 0, "2": 0, "3": 0, "4":0, "5":0, "recurring_keywords": []},
        "fit": {"too loose":0, "little loose":0, "true to size":0, "little tight":0, "extremely tight":0, "NA":0},
        "delivery": {"early":0, "on-time":0, "late":0, "NA":0},
        "valueForMoney": {"yes": 0, "no":0, "NA":0},
        "customerService": {"0":0, "1": 0, "2": 0, "3": 0, "4":0, "5":0, "recurring_keywords": []},
        "ratings": {"1": 0, "2": 0, "3": 0, "4":0, "5":0},
        "recommend": {"yes": 0, "no": 0}
        }
        for (var j=0; j<rawReviews.length;j++){
          var review = rawReviews[j]
          var upvote = upvotes[j]
          var recommendation = recommend[j]
          var rating = ratings[j]
          const prompt = base_prompt + review + "'"
          const client = new TextServiceClient({
            authClient: new GoogleAuth().fromAPIKey(API_KEY),
          });
          
          const result = await client.generateText({model: MODEL_NAME, temperature:0, prompt: {text: prompt,},});
          if (result[0]['safetyFeedback'].length){
            continue
          }
          const output = result[0]["candidates"][0]["output"];
            var myArray = output.split("\n");
            const startInd1 = [0,1,2,3,4,5]
            const startInd2 = [1,2,3,4,5,6]
            var startInd = []
            if (myArray[0]== ""){
              startInd = startInd2 
            }
            else{
              startInd = startInd1
            }
            var newReview = {}
            //
            quality = myArray[startInd[0]].split("1. ")[1]
            quality = quality.trim()
            //
            style = myArray[startInd[1]].split("2. ")[1]
            if (style.includes('NA')){
              style_rating = 0
              style_aspect = 'NA'
              summary["style"]["0"]= summary["style"]["0"]+1+upvote
            }
            else{
              style_rating = style.split(" & ")
              style_aspect = style_rating[1]
              summary["style"][style_rating[0]]= summary["style"][style_rating[0]]+1+upvote
              summary["style"]["recurring_keywords"].push(style_aspect)
              style_rating  = Number(style_rating[0])
            }
            //
            fit = myArray[startInd[2]].split("3. ")[1]
            fit = fit.trim()
            //
            delivery = myArray[startInd[3]].split("4. ")[1]
            delivery = delivery.trim()
            //
            valueForMoney = myArray[startInd[4]].split("5. ")[1]
            valueForMoney = valueForMoney.trim()
            //
            customerService = myArray[startInd[5]].split("6. ")[1]
            if (customerService.includes('NA')){
              customerService_rating = 0
              customerService_aspect = 'NA'
              summary["customerService"]["0"]= summary["customerService"]["0"]+1+upvote
            }
            else{
              customerService_rating = customerService.split(" & ")
              customerService_aspect = customerService_rating[1]
              summary["customerService"][customerService_rating[0]]= summary["customerService"][customerService_rating[0]]+1+upvote
              summary["customerService"]["recurring_keywords"].push(customerService_aspect)
              customerService_rating  = Number(customerService_rating[0])
            }

            newReview["quality"] = quality
            summary["quality"][quality] = summary["quality"][quality] +1 + upvote
            newReview["style"] = {"rating": style_rating, "aspect": style_aspect}
            newReview["fit"] = fit
            summary["fit"][fit] = summary["fit"][fit] +1 + upvote
            newReview["delivery"] = delivery
            summary["delivery"][delivery] = summary["delivery"][delivery] +1 + upvote
            newReview["valueForMoney"] = valueForMoney
            summary["valueForMoney"][valueForMoney] = summary["valueForMoney"][valueForMoney] +1 + upvote
            newReview["customerService"] = {"rating": customerService_rating, "aspect": customerService_aspect}
            summary["recommend"][recommendation] = summary["recommend"][recommendation] + 1 + upvote
            summary["ratings"][rating] = summary["ratings"][rating] + 1 + upvote
            newReviews.push(newReview)
        }
        
        await Review.updateOne({_id},
            { $set: { cleanReviews:  newReviews, summary: summary}})
            const response = {"cleanReviews": newReviews, "summary": summary}
            return res.json(response)
        }
        else{   
            return res.json({status:'error', error:'Product not found'})
        }
    } catch(error){
        console.log(error)
            res.json({status:'error', error:error})
        } 
})

// router.post('/api/obtainAllCleanReviews', async(req, res) => {
//   const { username } = req.body
//   console.log(req.body)
//   try{
//       //check if user is verified/logged in
//      //jwt.verify(token, config.secret)

//      //check if document already exists, if yes update tokens to be earned else create new document
//      const docs = await Review.find({username})

//      if (docs.length){
//       for (var i=0; i<docs.length;i++){
//         console.log("Obtaining cleaned reviews for doc "+i);
//         try{
//         doc = docs[i]
//         const _id = doc._id;
//         var rawReviews = doc.rawReviews
//         var ratings = doc.ratings
//         var upvotes = doc.upvotes
//         var recommend = doc.recommend
//         var newReviews = []
//         const MODEL_NAME = "models/text-bison-001";
//         const API_KEY = process.env.PALM_API_KEY;
//         const base_prompt = "You are a customer feedback interpreter. When the user provides a customer review for a women's clothing product as an input, you are to perform the following tasks using it to help the user understand the review: \n\n 1. Classify the material quality of the item into one of the categories: 'extremely poor', 'not bad', 'fair', 'good', 'excellent'. If the customer does not mention anything regarding the fabric or material of the product, classify material quality as 'NA'. Else, in the above mentioned order, the 5 categories reflect low to high level of satisfaction with the material of the item. 'excellent' category means that the customer is extremely satisfied with the fabric or the material of the item and is indicated by very positive comments about the fabric. 'good' category means that the customer is happy with the fabric or the material of the item and is indicated by moderately positive comments about the fabric. 'fair' category means that the customer is neither too happy not too disappointed with the fabric or the material of the item; there might be some flaws as well as some positive feedback about the fabric, but the customer is overall satisfied with the product. 'not bad' category means there are 1-2 flaws or more with the material of the product and the customer expresses slight but not complete dissatisfaction from the tone of the review. 'poor' category means the fabric has multiple flaws and the customer expresses dissatisfaction and an overall negative perspective on her purchase. \n output format: [category] or 'NA' \n\n 2. Rate how stylish the product is from 1 to 5 based on the customer's review and feedback on how the clothing item looks on them. If the customer does not mention anything about the style of the item or it looks on them, output 'NA'. Else, increase the rating if the customer uses positive adjectives to describe the overall look and appearance of the item. Decrease the rating if the customer expresses negative feedback on the aspects of how the item has been crafted or it didn't look attractive. Your response should be an integer along with the aspect of the item that brought  its rating up or down in 2-3 words . (for example , if review says the seams were unfinished ,the aspect should be 'unfinished seams'). this aspect can be positive or negative. \n Output format: [integer from 1 to 5] & [aspect] or 'NA' \n\n 3. classify the fit of the clothing item on the customer into one of the following categories: 'too loose', 'little loose', 'true to size', 'little tight', 'extremely tight' based on the review . If the customer does not give any feedback on the fit of the clothing , classify the fit as 'NA' . Else, for example, if the customer mentions a top being lose for her, based on the tone and degree of adjectives used for expressing this negative aspect, classify it as 'too loose' or 'little loose'. If the customer expresses that the product fits perfectly and expresses a positive review about the fit , classify as 'true to size'. \n output format: [1 of the 5 categories] or 'NA' \n\n 4. classify the delivery times of the product based on its review into one of the following categories: 'early', 'on-time', 'late'. If the customer does not mention anything regarding the delivery of product aspect, classify delivery time as 'NA'. Else, based on the feedback and adjectives used , classify as 'early' or 'late'. But if the customer expresses a positive review about the delivery time , then classify as 'on time'. \n output format : [1 of the 3 categories] or 'NA' \n\n 5. Classify whether a product was a value for money purchase for a customer as 'yes' or 'no' categories based on its review. If the customer mentions a significant flaw in the making of the item that may make it impractical to use with a very negative tone and expresses repeated dissatisfaction with the product's appearance and feel using strong adjectives, classify it as 'no'. feedback on the fit of the item is not a factor to consider. Give importance to the tone of the review and how positive the overall feedback is. Most important factor is whether the particular customer would buy such a suit again or would recommend it to others. \n output format : [yes or no category] or 'NA' \n\n 6. Rate the customer service of the clothing company based on its product reviews on a scale of 1 to 5 if the customer gives any feedback on it in the review, else if it is not mentioned , output should be 'NA'. Customer service includes any feedback on the responsiveness and helpfulness of staff to customer enquiries post purchase of the item. The more negative the feedback on customer service: the lower is the rating. If the customer praises the customer service and expresses a completely positive feedback , rate it as 5. assess the degree of adjectives and tone of the description. the output should include one aspect the customer mentioned about the customer service, positive or negative in 2-3 words if there is any. \n output format: [integer between 1 to 5] & [aspect] or 'NA' \n\n perform these 6 tasks one by one for the user input and just give the output in the format as mentioned, without any additional reasoning. \n\n Here are 2 examples of the task: \n\n Review - 'Love this dress!  it's sooo pretty.  i happened to find it in a store, and i'm glad i did bc i never would have ordered it online bc it's petite.  i bought a petite and am 5'8.  i love the length on me- hits just a little below' \n Output - '1. good \n 2. 5 & pretty and petite \n 3. true to size \n 4. NA \n 5. yes \n 6. NA \n \n\n Review - 'Material and color is nice.  the leg opening is very large.  i am 5'1 (100#) and the length hits me right above my ankle.  with a leg opening the size of my waist and hem line above my ankle, and front pleats to make me fluffy, i think you can imagine that it is not a flattering look.  if you are at least average height or taller, this may look good on you.' \n Output - '1. good \n 2. 1 & leg opening too big, fluffy look \n 3. too loose \n 4. NA \n 5. no \n 6. NA \n \n\n Generate an output in the same format as explained for the following review: Review - '"
//         var summary = {
//           "quality": {"extremely poor":0, "not bad":0, "fair":0, "good":0, "excellent":0, "NA":0},
//           "style": {"0":0, "1": 0, "2": 0, "3": 0, "4":0, "5":0, "recurring_keywords": []},
//           "fit": {"too loose":0, "little loose":0, "true to size":0, "little tight":0, "extremely tight":0, "NA":0},
//           "delivery": {"early":0, "on-time":0, "late":0, "NA":0},
//           "valueForMoney": {"yes": 0, "no":0, "NA":0},
//           "customerService": {"0":0, "1": 0, "2": 0, "3": 0, "4":0, "5":0, "recurring_keywords": []},
//           "ratings": {"1": 0, "2": 0, "3": 0, "4":0, "5":0},
//           "recommend": {"yes": 0, "no": 0}
//           }
//           for (var j=0; j<rawReviews.length;j++){
//             var review = rawReviews[j]
//             var upvote = upvotes[j]
//             var recommendation = recommend[j]
//             var rating = ratings[j]
//             const prompt = base_prompt + review + "'"
//             const client = new TextServiceClient({
//               authClient: new GoogleAuth().fromAPIKey(API_KEY),
//             });
            
//             const result = await client.generateText({model: MODEL_NAME, temperature:0, prompt: {text: prompt,},});
//               const output = result[0]["candidates"][0]["output"];
//               var myArray = output.split("\n");
//               var newReview = {}
//               //
//               quality = myArray[1].split("1. ")[1]
//               quality = quality.trim()
//               //
//               style = myArray[2].split("2. ")[1]
//               if (style.includes('NA')){
//                 style_rating = 0
//                 style_aspect = 'NA'
//                 summary["style"]["0"]= summary["style"]["0"]+1+upvote
//               }
//               else{
//                 style_rating = style.split(" & ")
//                 style_aspect = style_rating[1]
//                 summary["style"][style_rating[0]]= summary["style"][style_rating[0]]+1+upvote
//                 summary["style"]["recurring_keywords"].push(style_aspect)
//                 style_rating  = Number(style_rating[0])
//               }
//               //
//               fit = myArray[3].split("3. ")[1]
//               fit = fit.trim()
//               //
//               delivery = myArray[4].split("4. ")[1]
//               delivery = delivery.trim()
//               //
//               valueForMoney = myArray[5].split("5. ")[1]
//               valueForMoney = valueForMoney.trim()
//               //
//               customerService = myArray[6].split("6. ")[1]
//               if (customerService.includes('NA')){
//                 customerService_rating = 0
//                 customerService_aspect = 'NA'
//                 summary["customerService"]["0"]= summary["customerService"]["0"]+1+upvote
//               }
//               else{
//                 customerService_rating = customerService.split(" & ")
//                 customerService_aspect = customerService_rating[1]
//                 summary["customerService"][customerService_rating[0]]= summary["customerService"][customerService_rating[0]]+1+upvote
//                 summary["customerService"]["recurring_keywords"].push(customerService_aspect)
//                 customerService_rating  = Number(customerService_rating[0])
//               }
  
//               newReview["quality"] = quality
//               summary["quality"][quality] = summary["quality"][quality] +1 + upvote
//               newReview["style"] = {"rating": style_rating, "aspect": style_aspect}
//               newReview["fit"] = fit
//               summary["fit"][fit] = summary["fit"][fit] +1 + upvote
//               newReview["delivery"] = delivery
//               summary["delivery"][delivery] = summary["delivery"][delivery] +1 + upvote
//               newReview["valueForMoney"] = valueForMoney
//               summary["valueForMoney"][valueForMoney] = summary["valueForMoney"][valueForMoney] +1 + upvote
//               newReview["customerService"] = {"rating": customerService_rating, "aspect": customerService_aspect}
//               summary["recommend"][recommendation] = summary["recommend"][recommendation] + 1 + upvote
//               summary["ratings"][rating] = summary["ratings"][rating] + 1 + upvote
//               newReviews.push(newReview)
//           }
//         await Review.updateOne({_id},
//             { $set: { cleanReviews:  newReviews, summary: summary}})

//         const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))
//         await sleep(10000)

//         }

//         catch(error){
//           console.log(error)
//           console.log("Error found in product "+i)
//         }
//         finally{
//           continue
//         }

//       }
//       return res.json({status:'ok'})
//     }
//       else{   
//           return res.json({status:'error', error:'No products found'})
//       }
//   } catch(error){
//       console.log(error)
//           res.json({status:'error', error:error})
//       } 
// })

router.get('/api/getCleanReviews/:productId/:username', async (req, res)=>{
  const productId = req.params.productId
  const username = req.params.username
  try{
      // jwt.verify(token, config.secret)
      const doc = await Review.findOne({ username, productId }).lean()
      response = {"cleanReviews": doc.cleanReviews, "rawReviews": doc.rawReviews, 
      "reviewer_age": doc.reviewerAge, }
      return res.send(response);
  }
  catch(err){
      console.log(err)
      res.json({status:'error', error: err})
  } 
});

router.get('/api/getInsights/:productId/:token', async (req, res)=>{
  const productId = req.params.productId
  const token = req.params.token
  try{
      jwt.verify(token, config.secret)
      const doc = await Review.findOne({ productId }).lean()
      return res.send(doc.summaryInsights);
  }
  catch(err){
      console.log(err)
      res.json({status:'error', error: err})
  } 
});

module.exports = router;


// const response = await openai.createChatCompletion({
        //   model: "gpt-3.5-turbo",
        //   temperature: 0.0, top_p: 0.95, frequency_penalty: 0, presence_penalty: 0,
        //   messages: [{"role": "system", "content": "You are a customer feedback interpreter. When the user provides a customer review for a women's clothing product as an input, you are to perform the following tasks using it to help the user understand the review: \n\n 1. Classify the material quality of the item into one of the categories: 'extremely poor', 'not bad', 'fair', 'good', 'excellent'. If the customer does not mention anything regarding the fabric or material of the product, classify material quality as 'NA'. Else, in the above mentioned order, the 5 categories reflect low to high level of satisfaction with the material of the item. 'excellent' category means that the customer is extremely satisfied with the fabric or the material of the item and is indicated by very positive comments about the fabric. 'good' category means that the customer is happy with the fabric or the material of the item and is indicated by moderately positive comments about the fabric. 'fair' category means that the customer is neither too happy not too disappointed with the fabric or the material of the item; there might be some flaws as well as some positive feedback about the fabric, but the customer is overall satisfied with the product. 'not bad' category means there are 1-2 flaws or more with the material of the product and the customer expresses slight but not complete dissatisfaction from the tone of the review. 'poor' category means the fabric has multiple flaws and the customer expresses dissatisfaction and an overall negative perspective on her purchase. \n output format: [category] or 'NA' \n\n 2. Rate how stylish the product is from 1 to 5 based on the customer's review and feedback on how the clothing item looks on them. If the customer does not mention anything about the style of the item or it looks on them, output 'NA'. Else, increase the rating if the customer uses positive adjectives to describe the overall look and appearance of the item. Decrease the rating if the customer expresses negative feedback on the aspects of how the item has been crafted or it didn't look attractive. Your response should be an integer along with the aspect of the item that brought  its rating up or down in 2-3 words . (for example , if review says the seams were unfinished ,the aspect should be 'unfinished seams'). this aspect can be positive or negative. \n Output format: [integer from 1 to 5] & [aspect] or 'NA' \n\n 3. classify the fit of the clothing item on the customer into one of the following categories: 'too loose', 'little loose', 'true to size', 'little tight', 'extremely tight' based on the review . If the customer does not give any feedback on the fit of the clothing , classify the fit as 'NA' . Else, for example, if the customer mentions a top being lose for her, based on the tone and degree of adjectives used for expressing this negative aspect, classify it as 'too loose' or 'little loose'. If the customer expresses that the product fits perfectly and expresses a positive review about the fit , classify as 'true to size'. \n output format: [1 of the 5 categories] or 'NA' \n\n 4. classify the delivery times of the product based on its review into one of the following categories: 'early', 'on-time', 'late'. If the customer does not mention anything regarding the delivery of product aspect, classify delivery time as 'NA'. Else, based on the feedback and adjectives used , classify as 'early' or 'late'. But if the customer expresses a positive review about the delivery time , then classify as 'on time'. \n output format : [1 of the 3 categories] or 'NA' \n\n 5. Classify whether a product was a value for money purchase for a customer as 'yes' or 'no' categories based on its review. If the customer mentions a significant flaw in the making of the item that may make it impractical to use with a very negative tone and expresses repeated dissatisfaction with the product's appearance and feel using strong adjectives, classify it as 'no'. feedback on the fit of the item is not a factor to consider. Give importance to the tone of the review and how positive the overall feedback is. Most important factor is whether theparticular customer would buy such a suit again or would recommend it to others. \n output format : [yes or no category] or 'NA' \n\n 6. Rate the customer service of the clothing company based on its product reviews on a scale of 1 to 5 if the customer gives any feedback on it in the review, else if it is not mentioned , output should be 'NA'. Customer service includes any feedback on the responsiveness and helpfulness of staff to customer enquiries post purchase of the item. The more negative the feedback on customer service: the lower is the rating. If the customer praises the customer service and expresses a completely positive feedback , rate it as 5. assess the degree of adjectives and tone of the description. the output should include one aspect the customer mentioned about the customer service, positive or negative in 2-3 words if there is any. \n output format: [integer between 1 to 5] & [aspect] or 'NA' \n\n perform these 6 tasks one by one for the user input and just give the output in the format as mentioned, without any additional reasoning."}, {"role": "user", "content": review}]
        // });
        
        // message = response.data.choices[0].message.content
        // console.log(message)



// const configuration = new Configuration({
        //     apiKey: process.env.OPENAI_API_KEY,
        //   });
        // const openai = new OpenAIApi(configuration);  
