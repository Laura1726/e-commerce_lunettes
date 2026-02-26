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

    sql = ''' SELECT id_lunette AS id_article, nom_lunette AS nom, sexe, indice_protection, taille_monture AS taille,
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

    sql = """SELECT lp.*,
                    l.prix_lunette AS prix,
                    l.nom_lunette  AS nom,
                    l.stock,
                    lp.lunette_id  AS id_article
             FROM ligne_panier lp
                      JOIN lunette l ON lp.lunette_id = l.id_lunette
             WHERE lp.utilisateur_id = %s"""
    mycursor.execute(sql, (id_client,))
    articles_panier = mycursor.fetchall()
    prix_total = 123  # requete à faire



    # pour le filtre






    if len(articles_panier) >= 1:
        prix_total = sum(item['prix'] * item['quantite'] for item in articles_panier)
    else:
        prix_total = None

    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , items_filtre=types_article
                           )
