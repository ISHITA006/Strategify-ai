const mongoose = require('mongoose')

const RawReviewsSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true },
    rawReviews: {type: Array, required:true }
}, {collection: 'rawReviews'})

const model = mongoose.model('RawReviewsSchema', RawReviewsSchema)

module.exports = model