import numpy as np
from flask import Flask, request, jsonify
import pickle
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

app = Flask(__name__)
model = pickle.load(open('/Users/RomainLejeune/Downloads/concevez_un_site_avec_flask-P1C1/Projet/model.pkl','rb'))
X = pickle.load(open('/Users/RomainLejeune/Downloads/concevez_un_site_avec_flask-P1C1/Projet/X_json.pkl','rb'))
df = pickle.load(open('/Users/RomainLejeune/Downloads/concevez_un_site_avec_flask-P1C1/Projet/df.pkl','rb'))


@app.route('/api',methods=['POST'])
def predict():
    # Get the data from the POST request.
    id_mov = request.get_json(force=True)['id']
    # Make prediction using model loaded from disk as per the data.
    Liste_voisins = model.kneighbors(X, return_distance=False)
    
    Liste_movies=[]
    for i in range(1,16):        
        Liste_movies.append(Liste_voisins[id_mov,i])

    Reco = []
    #Reco.append("Recommandation pour: " +df["movie_title"].iloc[[id_mov]].item())
    counter=0
    
    for i in range(0,15):
        
         if fuzz.partial_ratio(df["movie_title"].iloc[[id_mov]].item(),df["movie_title"].iloc[[Liste_movies[i]]].item())<=70:
            
           # Reco.append("Film "+str(counter+1)+": "+df["movie_title"].iloc[[Liste_movies[i]]].item())
            Reco.append(str([Liste_movies[i]])+': '+df["movie_title"].iloc[[Liste_movies[i]]].item()) 
            counter=counter+1
            
            if counter == 5:
                 break

    Reco=[s.replace('\xa0', '') for s in Reco]
   
    

    return jsonify(Reco)
    


if __name__ == '__main__':
    app.run(port=5000, debug=True)