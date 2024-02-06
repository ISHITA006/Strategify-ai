import pandas as pd
import requests
import streamlit as st
import json
import google.generativeai as palm
from IPython.display import display
from PIL import Image
import io

PALM_API_KEY = 'AIzaSyDM8Zj7ADY9WbOEAdxNpxoLZsrMlab39Vo'
API_KEYS =  ['Vby8kQmxsuYjDy0HEJUF7tdqzwXYY7yNjLhV2jTGdwVoK8N1aFapzI5l4LXO', 'EoNYR0G0GBkgshFeXr7nLX2JApM2XLXv2am5XcN7CB1yDTPhF0ayT0Boxwvy', 'vfVp9CXAqjtqXTuwNBBKGnEwt105cRtzCzEJXSfHN9ezl3tCfJQ0QSawiObf','EFfV391kRoWL7kXghi5a5HNBABykD2EgcjkpHSKnQ2ueip8KJUqknCpU4wRq', 'iFkgfYTlWjcVzXu78CIZKrt9IgoiZiLXH4aWvWPTMTZKaoT1NXLLGeSmVK6I', 'HmWCKSf20bdBBtTcs7bAg28WW9A1yOVRscWCIIuNZIdUcw1A1t2Dz1QDQBeY', 'kyT0nlIrhsiioQJH9K4tJDF62Ip9ZR88VCwH7VlxY5r93FNcqxa4Vz8iDmRW', 'x0pY02E8IdzkPph8QEH0lCo4qF4lPUvSfku3htjFQKOEsVUgG9BqH0VHbeAr', 'cngBNlxCKhNQtgU8rD3hjybotBQFoLOTdpyMcTArx8inQCw7IwnuUGwXjcUf','o0WALNcOcLk1X2WotTUgOCImLGtO1J8yOInk9jcnMDus3O8RM1tbLhUmWBqs', 'Z5Skxx65v2CugIPkmbpimVGI80oHbxq8ISZoY3YOUH5gbS4mgxy5K0N9hefH' ]
CLIPDROP_API_KEY = 'aa4e3893cb1f686af8852cd6a842d874717a639c3b6a395a38cad2270d0955574a893c8220e3db8663d0ea37a1bfeed9'


def register_user(username, email, password):
    url = 'https://market-assist-backend.onrender.com/users/api/register'
    data = {'username':username, 'email': email, 'password': password}
    response = requests.post(url, json=data).json()
    if 'error' in response.keys():
        if response['error'] == 'Password must contain at least 8 characters!':
            return 'password'
        elif response['error'] == 'Username, email address already in use!':
            return 'email'
        elif response['error'] == 'Invalid username':
            return 'email'
    else:
        return 'success'


def validate_user(email, password):
    url = 'https://market-assist-backend.onrender.com/users/api/login'
    data = {'email': email, 'password': password}
    response = requests.post(url, json=data).json()
    if 'error' in response.keys():
        if response['error'] == 'Invalid username/password!':
            return 'password'
        else:
            return 'username'
    else:
        return 'success', response['data']['username']

def upload_data(data, username):
    url = 'https://market-assist-backend.onrender.com/rawReviews/api/createDatabase'
    data = {'username': username, 'data': data}
    response = requests.post(url, json=data).json()
    if 'error' in response.keys():
        return 'error'
    else:
        return 'success'
    
def get_product_insights(username, product_id):
    url = 'https://market-assist-backend.onrender.com/cleanReviews/api/obtainCleanReview'
    data = {'username': username, 'productId': int(product_id)}
    response = requests.post(url, json=data).json()
    if 'error' in response.keys():
        return response
    else:
        return response['summary']
    
def check_data_exists(username):
    url = f'https://market-assist-backend.onrender.com/rawReviews/api/getProductIds/{username}'
    response = requests.get(url).json()
    try:
        if response['error'] == 'No data found':
            pass
        return 'error'
    except:
        return 'success'
    
def reupload_dataset(data, username):
    url = 'https://market-assist-backend.onrender.com/rawReviews/api/reuploadDatabase'
    data = {'username': username, 'data': data}
    response = requests.post(url, json=data).json()
    if 'error' in response.keys():
        return 'error'
    else:
        return 'success'

def download_dataset(username):
    url = f'https://market-assist-backend.onrender.com/rawReviews/api/getDatabase/{username}'
    response = requests.get(url).json()
    return response

def generate_image(var_summary, class_name):
    
    
    model_name = 'models/text-bison-001'
    
    palm.configure(api_key=PALM_API_KEY)
    
    initial_prompt =f'''
Based on the following customer feedback summary for a product, please provide an overall sentiment analysis. The summary data includes various aspects such as quality, style, fit, delivery, value for money, and customer service. Each aspect has been rated or commented on by customers, as shown:
{var_summary}
Please analyze this data to determine if the overall sentiment towards the product is positive, negative, or mixed. Highlight key strengths or areas for improvement based on the ratings and comments. This sentiment analysis will be used to inform our next steps, which may include creating targeted marketing campaigns to highlight the product's strengths or developing plans to address any areas of concern and improve customer satisfaction.
'''

    def generate_text(prompt):
        try:
            completion = palm.generate_text(
                model=model_name,
                prompt=prompt,
                temperature=0.5,
                max_output_tokens=800,
            )
            return completion.result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    sentiment_analysis_output = generate_text(initial_prompt)
    if "positive" in sentiment_analysis_output.lower():
        sentiment = "positive"

    elif "negative" in sentiment_analysis_output.lower():
        sentiment = "negative"

    else:
        sentiment = "negative"

    bard_prompt_3_positive =f''' The product which is {class_name}, has received high ratings for quality, style, fit, delivery, and value for money. Customers have also commented positively on the product's style and customer service.
Incorporate these insights to craft a one or two-line description that vividly highlights these attributes, specifically mentioning the type of product along with enriching adjectives that enhance its appeal. This detailed and imaginative description will be used to create product highlight images that visually showcase the best features loved by our customers, making the product irresistible in our marketing campaign.
Ensure the description is specific, mentioning the product explicitly (e.g., "an elegant dress," "a rugged backpack") and using adjectives that elevate the imagery, reflecting the positive sentiments and qualities such as improved fit, amazing quality, and the joy of using or wearing the product.
The goal is for this description to directly inspire text-to-image generation, resulting in captivating visuals that accurately represent the product's praised features in a way that resonates with potential buyers.'''

    bard_prompt_3_negative =f'''  The product which is {class_name}, has received negative feedback summary and the subsequent improvements we've made to our product dress, please synthesize this information into one or two sentences. These sentences should succinctly highlight the key improvements and positive changes made in response to customer feedback. The focus should be on visual and impactful aspects that can be easily translated into engaging and informative Product Highlight Images for our marketing campaign.

The goal is to communicate the positive evolution of our product. This concise summary will be used as input for a text-to-image generation model to create visuals that highlight these improvements, helping to visually convey our commitment to quality and customer satisfaction in our marketing materials.'''

    if sentiment == "positive":
        # bard_prompt_2 = bard_prompt_2_positive
        bard_prompt_3 = bard_prompt_3_positive
    else:
        # bard_prompt_2 = bard_prompt_2_negative
        bard_prompt_3 = bard_prompt_3_negative

    # bard_prompt_2_output = generate_text(bard_prompt_2)
    bard_prompt_3_output = generate_text(bard_prompt_3)

    url = "https://stablediffusionapi.com/api/v3/text2img"
    headers = {'Content-Type': 'application/json'}

    for key in API_KEYS:
        payload = json.dumps({
            "key": key,
            "prompt": bard_prompt_3_output,
            "negative_prompt": "close up",
            "width": 512,
            "height": 512,
            "samples": 4,
            "num_inference_steps": 20,
            "guidance_scale": 7.5
        })
        try:
            response = requests.post(url, headers=headers, data=payload)
            # Check if the request was successful
            if response.status_code == 200:
                response_dict = json.loads(response.text)
                if response_dict['status'] != 'error':
                # Assuming 'output' is the correct key in the response JSON for the image link
                    image_link = response_dict['output']
                    return image_link
                else:
                    print(f"Error with rate limit ")
            else:
                print(f"Error with API key {key}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for API key {key}: {e}")

    # If all keys fail, return a meaningful message or None
    return "All API keys failed, unable to generate image"

    # payload = json.dumps({
    #   "key": IMAGE_API_KEY,
    #   "prompt": bard_prompt_3_output,
    #   "negative_prompt": "close up",
    #   "width": 512,
    #   "height": 512,
    #   "samples": 1,
    #   "num_inference_steps": 20,
    #   "guidance_scale": 7.5
    # })
    # headers = {'Content-Type': 'application/json'}
    # response = requests.request("POST", url, headers=headers, data=payload)
    # response_dict = json.loads(response.text)
    # image_link = response_dict['output']

    # return image_link



def generate_marketing_campaign_and_poster(var_summary, class_name, customizations):
    
    model_name = 'models/text-bison-001'
    
    palm.configure(api_key=PALM_API_KEY)
    
    initial_prompt =f'''
Based on the following customer feedback summary for a product, please provide an overall sentiment analysis. The summary data includes various aspects such as quality, style, fit, delivery, value for money, and customer service. Each aspect has been rated or commented on by customers, as shown:
{var_summary}
Please analyze this data to determine if the overall sentiment towards the product is positive, negative, or mixed. Highlight key strengths or areas for improvement based on the ratings and comments. This sentiment analysis will be used to inform our next steps, which may include creating targeted marketing campaigns to highlight the product's strengths or developing plans to address any areas of concern and improve customer satisfaction.
'''

    def generate_text(prompt):
        try:
            completion = palm.generate_text(
                model=model_name,
                prompt=prompt,
                temperature=0.5,
                max_output_tokens=800,
            )
            return completion.result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    sentiment_analysis_output = generate_text(initial_prompt)
    summary = sentiment_analysis_output.split('\n', 1)
    if "positive" in sentiment_analysis_output.lower():
        sentiment = "positive"

    elif "negative" in sentiment_analysis_output.lower():
        sentiment = "negative"

    else:
        sentiment = "negative"
    # print(sentiment)

    bard_prompt_2_positive =f'''Based on a sentiment analysis, we have identified that our product has received positive feedback in several key areas.  {summary[1]}

Given this positive sentiment, please develop a comprehensive and actionable marketing campaign plan with the following objectives:

1. *Increase Awareness*: Propose strategies to boost product visibility and awareness among potential new customers. Detail the channels and methods to be employed, such as social media platforms, influencer collaborations, or digital advertising.

2. *Drive Sales*: Outline promotional tactics or offers that could incentivize purchases, such as limited-time discounts, bundle deals, or loyalty programs. Include suggestions for targeted messaging that highlights the product's benefits as identified in the sentiment analysis.

3. *Actionable Implementation Plan*:
   - Target Audience: Describe the ideal customer profiles most likely to be attracted to the product's strengths. Include demographics, interests, and buying behaviors.
   - Promotional Strategies:
     - Suggest specific content ideas for social media marketing, focusing on engaging formats like testimonials, product demos, or user-generated content campaigns.
     - Design an email marketing sequence that educates and nurtures leads, incorporating customer reviews and key selling points.
     - Recommend strategies for search engine marketing (SEM) or search engine optimization (SEO) to improve online visibility.
   - Creative Elements: Advise on the campaign's visual and messaging elements, such as themes, colors, and a campaign slogan that aligns with the product's perceived strengths.
   - Measurement of Success: Specify key performance indicators (KPIs) to track the campaign's impact on awareness, customer engagement, and sales metrics.

The goal is to create a marketing campaign that is not only compelling and aligned with the product's positive attributes but also practical for a seller to implement effectively. The plan should leverage the identified strengths to differentiate our product in the marketplace and attract a broader customer base.'''

    bard_prompt_3_positive =f''' The product which is {class_name}, has received high ratings for quality, style, fit, delivery, and value for money. Customers have also commented positively on the product's style and customer service.
Incorporate these insights to craft a one or two-line description that vividly highlights these attributes, specifically mentioning the type of product along with enriching adjectives that enhance its appeal. This detailed and imaginative description will be used to create product highlight images that visually showcase the best features loved by our customers, making the product irresistible in our marketing campaign.
Ensure the description is specific, mentioning the product explicitly (e.g., "an elegant dress," "a rugged backpack") and using adjectives that elevate the imagery, reflecting the positive sentiments and qualities such as improved fit, amazing quality, and the joy of using or wearing the product.
The goal is for this description to directly inspire text-to-image generation, resulting in captivating visuals that accurately represent the product's praised features in a way that resonates with potential buyers.'''

    bard_prompt_2_negative =f'''
Following a recent analysis, we've identified areas of our product that received negative feedback from our customers. [Insert the summary provided by the model here, detailing the specific concerns and issues highlighted by customers.]

{var_summary}

In response, we have made several improvements and adjustments to address these concerns directly. Here are the changes we've implemented:
•⁠  [Detail the specific actions taken, improvements made, or examples of how customer feedback has been addressed. This could include product enhancements, changes in customer service practices, or updates to delivery processes.]

With these improvements, we are now looking to launch a marketing campaign that:
1. Communicates the Improvements: Clearly and transparently inform current and potential customers about the changes made in response to feedback. Highlight the specific improvements and the steps taken to enhance the product and customer experience.
2. Rebuilds Trust and Improves Product Image: Use the campaign to rebuild customer trust and improve the overall image of the product, emphasizing our commitment to quality and customer satisfaction.
3. Increases Awareness and Sales: Develop strategies to reintroduce the product to the market, aiming to attract new customers and regain those who may have had a negative perception, ultimately increasing sales.

Please create a detailed and actionable marketing campaign plan that includes:
•⁠  Target Audience: Identification of key segments to target, including former customers and potential new customers who may have been deterred by previous feedback.
•⁠  Promotional Strategies:
- Propose ideas for engaging social media content and campaigns that highlight the improvements and positive changes made, possibly including before-and-after comparisons or customer testimonials.
- Outline a strategy for an email marketing campaign that communicates the improvements to previous customers, offering them incentives to give the product another try.
- Recommend approaches for public relations efforts, such as press releases or media outreach, to share the story of how customer feedback has driven positive change.
•⁠  Creative Elements: Suggest themes, messages, and visual elements for the campaign that reinforce the message of renewal and improvement.
•⁠  Measurement of Success: Define clear KPIs to evaluate the campaign's effectiveness in changing perceptions, engaging customers, and driving sales.

The goal is to devise a campaign that not only addresses past criticisms but also positions our product as improved and superior thanks to customer input, making it practical for a seller to implement and achieve significant market impact.
'''

    bard_prompt_3_negative ='''Based on the detailed negative feedback summary and the subsequent improvements we've made to our product dress, please synthesize this information into one or two sentences. These sentences should succinctly highlight the key improvements and positive changes made in response to customer feedback. The focus should be on visual and impactful aspects that can be easily translated into engaging and informative Product Highlight Images for our marketing campaign.

The goal is to communicate the positive evolution of our product, emphasizing the specific issues that have been addressed and fixed. This concise summary will be used as input for a text-to-image generation model to create visuals that highlight these improvements, helping to visually convey our commitment to quality and customer satisfaction in our marketing materials.'''

    if sentiment == "positive":
        bard_prompt_2 = bard_prompt_2_positive
        bard_prompt_3 = bard_prompt_3_positive
    else:
        bard_prompt_2 = bard_prompt_2_negative
        bard_prompt_3 = bard_prompt_3_negative

    bard_prompt_2_output = generate_text(bard_prompt_2)
    bard_prompt_3_output = generate_text(bard_prompt_3)

    # Integrate the marketing poster generation here
    api_url = 'https://clipdrop-api.co/text-to-image/v1'
    if customizations is not None:
        prompt = f'Create a vibrant social media marketing poster for product {class_name}, emphasizing its top feature: style. Make it visually captivating, targeting modern consumers.' + "Make sure to take the following into consideration: " +customizations
    else:
        prompt = f'Create a vibrant social media marketing poster for product {class_name}, emphasizing its top feature: style. Make it visually captivating, targeting modern consumers.'
    headers = {'x-api-key': CLIPDROP_API_KEY}
    files = {'prompt': (None, prompt, 'text/plain')}
    
    try:
        response = requests.post(api_url, files=files, headers=headers)
        if response.ok:
            # Display the image directly in the notebook
            image = Image.open(io.BytesIO(response.content))
            display(image)
            image_link = "Marketing poster displayed successfully."
        else:
            image_link = "Failed to generate marketing poster due to API error."
    except requests.exceptions.RequestException as e:
        image_link = f"An error occurred while generating the marketing poster: {e}"
    
    return bard_prompt_2_output, image, summary

def generate_summary(campaign_output, summary):
    
    model_name = 'models/text-bison-001'
    
    palm.configure(api_key=PALM_API_KEY)
    
    initial_prompt =f'''Please summarise our detailed marketing campaign in concise bullet points under 400 words. This is our marketing campaign - {campaign_output}. This is the overall customer sentiment analysis - {summary[1]}'''

    def generate_text(prompt):
        try:
            completion = palm.generate_text(
                model=model_name,
                prompt=prompt,
                temperature=0.5,
                max_output_tokens=800,
            )
            return completion.result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    summary = generate_text(initial_prompt)
    summary = summary.split('\n', 1)
    return summary[1]











