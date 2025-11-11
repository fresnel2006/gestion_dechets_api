from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

app=FastAPI()
class Utilisateur(BaseModel):
    nom: str
    numero: str
    mot_de_passe: str
class telephone(BaseModel):
    numero:str
class numeroetmotdepasse(BaseModel):
    numero:str
    mot_de_passe:str
connecter=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="utilisateurs_donnees"
)
@app.post("/verifier_utilisateur")
def verifier_utilisateur(Numero:telephone):
    conn=connecter.cursor()
    sql="SELECT * FROM utilisateur where numero=%s;"
    conn.execute(sql,(Numero.numero,))
    resultat=conn.fetchall()
    connecter.commit()
    if resultat==[]:
        return {"existe":"false"}
    else:
        return {"existe":"true"}
@app.post("/ajouter_utilisateur")
def ajouter_utilisateur(utilisateur:Utilisateur):
    conn=connecter.cursor()
    sql="INSERT INTO utilisateur (nom,numero,mot_de_passe) VALUES (%s,%s,%s)"
    conn.execute(sql,(utilisateur.nom,utilisateur.numero,utilisateur.mot_de_passe))
    connecter.commit()
    conn.close()
    return {"utilisateur":"utilisateur ajouté"}

@app.post("/verifier_donnee")
def verifierdonnee(verificateur:numeroetmotdepasse):
    conn=connecter.cursor()
    sql="SELECT * FROM utilisateur WHERE numero=%s AND mot_de_passe=%s;"
    conn.execute(sql,(verificateur.numero,verificateur.mot_de_passe))
    resultat=conn.fetchall()
    connecter.commit()
    if resultat==[]:
        return {"existe":"false","utilisateur":"rien"}
    else:
        return {"existe": "true", "utilisateur":resultat}

