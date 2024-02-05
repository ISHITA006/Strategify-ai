const mongoose = require('mongoose')

const RawReviewsSchema = new mongoose.Schema({
    productId: { type: Number, required: true },
    username: { type: String, required: true },
    productCategory: { type: String, required: true },
    reviewerAge: { type: Array, required: true},
    upvotes: { type: Array, required: true},
    recommend: { type: Array, required: true},
    ratings: { type: Array, required: true},
    rawReviews: {type: Array, required:true },
    cleanReviews:{type:Array},
    summary:{type:Object}
}, {collection: 'rawReviews'})

const model = mongoose.model('RawReviewsSchema', RawReviewsSchema)

module.exports = model