const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs')
const jwt = require('jsonwebtoken')
const config = require('../auth.config')
const  User  = require('../model/user');

router.post('/api/register', async (req, res) => {
    console.log(req.body)
    const { username, email, password: plainTextPassword } = req.body

    if(!username || typeof username !== 'string'){
        return res.json({status:'error', error:'Invalid username'})
    }

    if(!email || typeof email !== 'string'){
        return res.json({status:'error', error:'Invalid email'})
    }

    if(!plainTextPassword || typeof plainTextPassword !== 'string'){
        return res.json({status:'error', error:'Invalid password'})
    }

    if(plainTextPassword.length<7){
        return res.json({status:'error', error:'Password must contain at least 8 characters!'})
    }
    
    password = await bcrypt.hash(plainTextPassword, 10)
    try{
        const response = await User.create({
            username, email, password
        })
        console.log("User registered successfully: "+ response)
    }
    catch(error){
        if (error.code === 11000){
            return res.json({status:'error', error: 'Username, email address already in use!'})
        }
        throw error
    }
      
    res.json({ status: 'ok' })
})


router.post('/api/login', async(req, res) => {
    
    const {email, password} = req.body
    const user = await User.findOne({ email }).lean()
    
    if(!user){
        return res.json({status:'error', error:'Email not found!'})
    }

    console.log(bcrypt.compare(password, user.password))

    const verified = await bcrypt.compare(password, user.password);

    if(verified){
        //username password combination is successful
        
        const token = jwt.sign({
            id: user._id,
            username: user.username}, config.secret, {expiresIn: '1h'})
        
        const response = {"token": token, "username": user.username}
        
        return res.json({status:'ok', data: response})
    }
    res.json({status:'error', error:'Invalid username/password!' })
})

router.post('/api/change-password', async(req, res) => {
    const { token, newpassword: plainTextPassword } = req.body
    try{
      
       const user = jwt.verify(token, config.secret)
       const _id = user.id

       if(!plainTextPassword || typeof plainTextPassword !== 'string'){
        return res.json({status:'error', error:'Invalid password'})
    }

    if(plainTextPassword.length<7){
        return res.json({status:'error', error:'Password must contain at least 8 characters!'})
    }

       const password = await bcrypt.hash(plainTextPassword, 10)
       await User.updateOne({_id},
        { $set: { password: password }})
        res.json({status:'ok'})
    } catch(error){
        res.json({status:'error', error:'User token not verified'})
    }
    
})

router.post('/api/change-email', async(req, res) => {
    const { token, newemail } = req.body
    try{
      
       const user = jwt.verify(token, config.secret)
       const _id = user.id

       if(!newemail || typeof newemail !== 'string'){
        return res.json({status:'error', error:'Invalid Email'})
    }

       await User.updateOne({_id},
        { $set: { email: newemail }})
        res.json({status:'ok'})
    } catch(error){
        res.json({status:'error', error:'User token not verified'})
    }
})


module.exports = router;