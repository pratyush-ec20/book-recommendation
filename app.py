from flask import Flask, render_template,request
import pickle
import pandas as pd
import numpy as np

pickle_off1=open('popular.pkl','rb')
popular_df = pd.read_pickle(pickle_off1)

pickle_off2=open('pt.pkl','rb')
pt=pd.read_pickle(pickle_off2)

pickle_off3=open('books.pkl','rb')
books=pd.read_pickle(pickle_off3)

pickle_off4=open('similarity_score.pkl','rb')
similarity_score=pd.read_pickle(pickle_off4)





app = Flask(__name__)

@app.route('/')
def index():
    
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           #popular_df['Image-URL-L']=popular_df['Image-URL-L'].str.replace('http://','https://')
                           image=list(popular_df['Image-URL-L'].str.replace('http://','https://').values),
                           votes=list(popular_df['num_ratings'].values),
                           ratings=list(popular_df['avg_ratings'].values))

                          

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    
    user_input = request.form.get("user_input")
    index=np.where(pt.index==user_input)[0][0]
    similar_items=sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:9]
    data=[]
    for i in similar_items:
        item=[]
        temp_df= books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))
        
        data.append(item)
    print(data)    
    return render_template('recommend.html',data=data)
    


if __name__=='__main__':
    app.run(debug=True)
