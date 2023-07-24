const mongoose = require('mongoose')

const RawReviewsSchema = new mongoose.Schema({
    productId: { type: Number, required: true, unique: true },
    username: { type: String, required: true },
    productName: { type: String, required: true },
    price: { type: Number, required: true},
    rawReviews: {type: Array, required:true }
}, {collection: 'rawReviews'})

const model = mongoose.model('RawReviewsSchema', RawReviewsSchema)

module.exports = model