#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''   selection des articles   '''

    sql = ''' SELECT id_lunette, nom_lunette AS nom, sexe, indice_protection, taille_monture AS taille,
    prix_lunette AS prix, image, stock, fournisseur, marque, categorie_id
    FROM lunette
    ORDER BY nom ASC;
    '''
    mycursor.execute(sql)
    lunette = mycursor.fetchall()
    articles = lunette
    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3=''' prise en compte des commentaires et des notes dans le SQL    '''

    sql = '''
          SELECT id_categorie, libelle_categorie
          FROM categorie
          ORDER BY libelle_categorie;
          '''
    mycursor.execute(sql)
    categorie = mycursor.fetchall()
    types_article = categorie

    sql = "SELECT * , 10 as prix , concat('lunette',lunette_id) as nom FROM ligne_panier"
    mycursor.execute(sql)
    articles_panier = mycursor.fetchall()
    prix_total = 123  # requete à faire



    # pour le filtre






    if len(articles_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           #, prix_total=prix_total
                           , items_filtre=types_article
                           )
