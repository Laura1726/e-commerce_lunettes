#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = """SELECT lp.*, l.prix_lunette AS prix, l.nom_lunette AS nom
             FROM ligne_panier lp
                      JOIN lunette l ON lp.lunette_id = l.id_lunette
             WHERE lp.utilisateur_id = %s"""
    mycursor.execute(sql, (id_client,))
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:
        prix_total = sum(item['prix'] * item['quantite'] for item in articles_panier)
    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    id_client = session['id_user']
    sql = """SELECT lp.*, l.prix_lunette AS prix
             FROM ligne_panier lp
                      JOIN lunette l ON lp.lunette_id = l.id_lunette
             WHERE lp.utilisateur_id = %s"""
    mycursor.execute(sql, (id_client,))
    items_ligne_panier = mycursor.fetchall()

    # Création de la commande
    sql = "INSERT INTO commande(date_achat, etat_id, utilisateur_id) VALUES (CURRENT_DATE, 1, %s)"
    mycursor.execute(sql, (id_client,))

    # Récupération de l'id de la nouvelle commande
    mycursor.execute("SELECT last_insert_id() as last_insert_id")
    id_commande = mycursor.fetchone()['last_insert_id']

    for item in items_ligne_panier:
        # Ajout d'une ligne de commande
        sql = "INSERT INTO ligne_commande(prix, quantite, lunette_id, commande_id) VALUES (%s, %s, %s, %s)"
        mycursor.execute(sql, (item['prix'], item['quantite'], item['lunette_id'], id_commande))

        # Suppression de la ligne de panier
        sql = "DELETE FROM ligne_panier WHERE lunette_id = %s AND utilisateur_id = %s"
        mycursor.execute(sql, (item['lunette_id'], id_client))

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/article/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = """SELECT c.*,
                    SUM(lc.prix * lc.quantite) AS prix_total,
                    COUNT(lc.lunette_id)       AS nbr_articles,
                    e.libelle_etat             AS libelle
             FROM commande c
                      LEFT JOIN ligne_commande lc ON c.id_commande = lc.commande_id
                      LEFT JOIN etat e ON c.etat_id = e.id_etat
             WHERE c.utilisateur_id = %s
             GROUP BY c.id_commande
             ORDER BY c.etat_id ASC, c.date_achat DESC"""
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = """SELECT lc.*, l.nom_lunette AS nom
                 FROM ligne_commande lc
                          JOIN lunette l ON lc.lunette_id = l.id_lunette
                 WHERE lc.commande_id = %s"""
        mycursor.execute(sql, (id_commande,))
        articles_commande = mycursor.fetchall()

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )

