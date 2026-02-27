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

    sql = ''' SELECT id_lunette AS id_article,nom_lunette AS nom,sexe,indice_protection,taille_monture AS taille,prix_lunette AS prix,
                     image,stock,fournisseur,marque,categorie_id
              FROM lunette
              WHERE 1 = 1
          '''
    list_param = []
    condition_and = " AND "

    if 'filter_word' in session and session['filter_word']:
        sql = sql + condition_and + " nom_lunette LIKE %s "
        recherche = "%" + session['filter_word'] + "%"
        list_param.append(recherche)

    if 'filter_prix_min' in session and 'filter_prix_max' in session and session['filter_prix_min'] and session['filter_prix_max']:
        sql = sql + condition_and + ' prix_lunette BETWEEN %s AND %s'
        list_param.append(session['filter_prix_min'])
        list_param.append(session['filter_prix_max'])

    if 'filter_types' in session and session['filter_types']:
        placeholders = ', '.join(['%s'] * len(session['filter_types']))
        sql = sql + condition_and + f"categorie_id IN ({placeholders})"
        list_param.extend(session['filter_types'])

    sql += " ORDER BY nom ASC"
    tuple_sql = tuple(list_param)

    mycursor.execute(sql, tuple_sql)
    lunette = mycursor.fetchall()
    articles = lunette

    # utilisation du filtre
    sql3 = ''' prise en compte des commentaires et des notes dans le SQL    '''

    sql = '''
          SELECT id_categorie, libelle_categorie
          FROM categorie
          ORDER BY libelle_categorie;
          '''
    mycursor.execute(sql)
    categorie = mycursor.fetchall()
    types_article = categorie

    sql = """SELECT lp.*,l.prix_lunette AS prix,l.nom_lunette  AS nom,l.stock,lp.lunette_id  AS id_article
             FROM ligne_panier lp
            JOIN lunette l ON lp.lunette_id = l.id_lunette
             WHERE lp.utilisateur_id = %s"""
    mycursor.execute(sql, (id_client,))
    articles_panier = mycursor.fetchall()

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

