# Strategify.AI

Companies or brands that sell their products online receive a large number of customer reviews and feedback.

Customer feedback can be a valuable tool to improve the product and curate effective marketing campaigns that would greatly improve their product sales.

However, the huge volume of feedbacks makes it difficult for humans to go through and draw overall insights about customer's perception of the product, features that are favourable and features that are not.

Strategify.AI (finetuned for the case of a women's clothing company), can do this hefty task for such businesses.

It analyses reviews to understand the customer's sentiment regarding 6 crucial parameters: quality, style, fit, delivery time, customer service and pricing.

After understanding the overall product sentiment, Strategify.AI will present feedback analytics in the form of useful charts, use it to suggest a comprehensive marketing strategy, generate campaign posters and product inspiration ideas.

Demo instructions:

Try out our app here: __________________
Upload "data.csv" file when prompted to upload data on the app. You can use any other women's fashion reviews dataset following the same format as "data.csv" to test our app
Hackathon Challenges Tackled:

AI Agent - PaLM 2 Model
Text/Content generation - PaLM 2 Model
Image generation - Stable Diffusion Model ( V3 and XL )
Components:

Streamlit frontend (Hosted on ______ )
Node.js backend (Hosted on Render)
MongoDB database (Hosted on MongoDB Atlas)
How to run our code

Backend set up:

Install nodejs on your PC
cd /Marketing-Assist-Dashboard/backend
npm install
node server.js
Frontend set up:

Install python on your PC
cd /Marketing-Assist-Dashboard/Streamlit
pip install -r requirements.txt
streamlit run Strategify.AI.py
