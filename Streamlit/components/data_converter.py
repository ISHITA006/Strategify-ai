import pandas as pd
import json

def create_sub_dataframe(df, col_name, value):
    sub_df = df[df[col_name] == value]
    return sub_df

def get_class_name(df, clothing_id):
    class_name = df[df['Clothing ID'] == clothing_id]['Class Name'].values[0]
    return class_name

def create_radar_chart_dict(df):
    df['age_group'] = pd.cut(df['Age'], bins=[16, 24, 34, 44, 54, 64, 100], labels=['16-24', '25-34', '35-44', '45-54', '55-64', '65>'])
    age_group_rating = df.groupby(['Rating', 'age_group']).size().unstack().fillna(0).astype(int).to_dict()
    age_group_rating = {'age_groups': age_group_rating}
    return age_group_rating

def to_json(df):
    df['Product Category'] = df['Department Name']+"/"+df['Division Name']+"/"+df['Class Name']
    df= df[['Clothing ID','Age', 'Rating', 'Recommended IND', 'Feedback', 'Positive Feedback Count', 'Product Category']]
    unique_prods = list(set(list(df['Clothing ID'])))
    reviews_dict = {}
    for prod in unique_prods:
        df_filtered = df[df['Clothing ID']==prod]
        reviews = list(df_filtered['Feedback'])
        ages = list(df_filtered['Age'])
        ratings = list(df_filtered['Rating'])
        recommends = list(df_filtered['Recommended IND'])
        pos_feedbacks = list(df_filtered['Positive Feedback Count'])
        product_category = list(df_filtered['Product Category'])[0]
        reviews_dict[prod] = {"product_category": product_category, "reviewer_age": ages, "ratings": ratings, \
                            "recommend": recommends, "upvotes": pos_feedbacks, "reviews": reviews}

    my_json = json.dumps(reviews_dict)
    return my_json

def from_json(json_str):
    clothing_id = []
    age = []
    rating = []
    recommend = []
    division_name = []
    department_name = []
    class_name = []
    reviews = []
    positive_feedback = []
    for i in json_str:
        for j in range(len(i['reviewerAge'])):
            clothing_id.append(i['productId'])
            age.append(i['reviewerAge'][j])
            rating.append(i['ratings'][j])
            reviews.append(i['rawReviews'][j])
            recommend.append(i['recommend'][j])
            positive_feedback.append(i['upvotes'][j])   
            names = i['productCategory'].split('/')
            department_name.append(names[0])
            division_name.append(names[1])
            class_name.append(names[2])
        
    df = pd.DataFrame({'Positive Feedback Count':positive_feedback, 'Clothing ID': clothing_id, 'Age': age, 'Rating': rating, 'Recommended IND': recommend, 'Department Name': department_name, 'Division Name': division_name, 'Class Name': class_name, 'Review Text': reviews})
    return df

def get_recurring_keywords(recurring_keywords):
    keywords = []
    for i in recurring_keywords['style']['recurring_keywords']:
        temp = i.split(',')
        for j in temp:
            keywords.append(j)
    return [x.strip() for x in keywords]
     
