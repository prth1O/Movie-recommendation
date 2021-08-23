from flask import Flask,render_template,request
import pickle
import os
import numpy as np
import pandas as pd


app= Flask(__name__)

#loading model
sig=pickle.load(open("sig.pkl",'rb'))
df=pd.read_csv('movied_names.csv')
indices = pd.Series(df.index, index=df['original_title']).drop_duplicates()
mv_nm=df.original_title.to_list()
def give_rec(title, sig=sig):
    # Get the index corresponding to original_title
    idx = indices[title]

    # Get the pairwsie similarity scores
    sig_scores = list(enumerate(sig[idx]))

    # Sort the movies
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    # Scores of the 10 most similar movies
    sig_scores = sig_scores[1:11]

    # Movie indices
    movie_indices = [i[0] for i in sig_scores]

    # Top 10 most similar movies
    return df['original_title'].iloc[movie_indices]

@app.route('/',methods=['GET'])

def home():


    return render_template('Index.html',li=mv_nm)


@app.route('/Recomdation',methods=['GET',"POST"])

def  rec():
    f=request.form['Movie']
    recs=give_rec(str(f)).items()

    return render_template('rec.html',lm=f,rec=recs,li=mv_nm)



if __name__ == '__main__':
    app.run()
