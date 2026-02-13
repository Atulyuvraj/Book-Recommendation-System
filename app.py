from flask import Flask,render_template,request
import joblib
import numpy as np
import pandas as pd

app=Flask(__name__)

book=joblib.load("books.joblib")
pt=joblib.load("data.joblib")
similarity=joblib.load("simi.pkl")
df=joblib.load("main_data.joblib")



@app.route("/")
def index():
    
    return render_template("index.html",book_name=list(book["Book-Title"].values),
    image=list(book["Image-URL-M"].values),
    author=list(book["Book-Author"].values),
    votes=list(book["Num-Rating"].values),
    rating=list(book["Avg-Rating"].values),)

@app.route("/recommend")
def rec():
    return render_template("rec.html")

@app.route("/find", methods=["POST", "GET"])
def find():
    if request.method == "POST":
        user_input = request.form.get("querry")
        
       
        if user_input not in pt.index:
          
            return render_template("rec.html", error="Book not found!")

       
        index = np.where(pt.index == user_input)[0][0]
        
        
        similar_items = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:6]
        
        data = []
        for i in similar_items:
            item = []
            # Use 'book' (the original dataframe) to fetch details
            temp_df = book[book['Book-Title'] == pt.index[i[0]]]
            
            # Extracting unique values for the response
            item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
            item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
            item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))
            
            data.append(item)
            
        # 4. Pass 'data' to your results page (fixed syntax)
        return render_template("rec.html", data=data)
    
     


if __name__=="__main__":
    app.run(debug=True)

