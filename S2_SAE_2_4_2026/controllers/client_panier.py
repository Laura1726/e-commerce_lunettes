#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_lunette = request.form.get('id_article')
    quantite = request.form.get('quantite')
    # ---------
    #id_declinaison_article=request.form.get('id_declinaison_article',None)
    id_declinaison_article = 1

# ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_article))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_article = declinaisons[0]['id_declinaison_article']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_article))
    #     article = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_article.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , article=article)

# ajout dans le panier d'un article
    sql = "SELECT * FROM ligne_panier WHERE lunette_id = %s AND utilisateur_id=%s"
    mycursor.execute(sql, (id_lunette, id_client))
    lunette_panier = mycursor.fetchone()

    mycursor.execute("SELECT * FROM lunette WHERE id_lunette = %s", (id_lunette,))
    lunette_stock = mycursor.fetchone()

    if lunette_stock['stock'] >= int(quantite):

        if not (lunette_panier is None) and lunette_panier['quantite'] >= 1:
            sql = "UPDATE ligne_panier SET quantite = quantite+%s WHERE utilisateur_id = %s AND lunette_id=%s"
            mycursor.execute(sql, (quantite, id_client, id_lunette))
        else:
            sql = "INSERT INTO ligne_panier(utilisateur_id,lunette_id,quantite, date_ajout) VALUES (%s,%s,%s, current_timestamp)"
            mycursor.execute(sql, (id_client, id_lunette, quantite))

        # Décrémenter le stock
        sql = "UPDATE lunette SET stock = stock - %s WHERE id_lunette = %s"
        mycursor.execute(sql, (quantite, id_lunette))

    else:
        flash(u'Stock insuffisant')

    get_db().commit()

    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'article
    # id_declinaison_article = request.form.get('id_declinaison_article', None)

    sql = "SELECT * FROM ligne_panier WHERE lunette_id = %s AND utilisateur_id = %s"
    mycursor.execute(sql, (id_article, id_client))
    article_panier = mycursor.fetchone()

    if not (article_panier is None) and article_panier['quantite'] > 1:
        sql = "UPDATE ligne_panier SET quantite = quantite - 1 WHERE lunette_id = %s AND utilisateur_id = %s"
        mycursor.execute(sql, (id_article, id_client))
    else:
        sql = "DELETE FROM ligne_panier WHERE lunette_id = %s AND utilisateur_id = %s"
        mycursor.execute(sql, (id_article, id_client))

    # mise à jour du stock de l'article disponible
    sql = "UPDATE lunette SET stock = stock + 1 WHERE id_lunette = %s"
    mycursor.execute(sql, (id_article,))
    get_db().commit()
    return redirect('/client/article/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = "SELECT * FROM ligne_panier WHERE utilisateur_id = %s"
    mycursor.execute(sql, (client_id,))
    items_panier = mycursor.fetchall()

    for item in items_panier:
        sql = "UPDATE lunette SET stock = stock + %s WHERE id_lunette = %s"
        mycursor.execute(sql, (item['quantite'], item['lunette_id']))

    sql = "DELETE FROM ligne_panier WHERE utilisateur_id = %s"
    mycursor.execute(sql, (client_id,))
    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', '')
    #id_declinaison_article = request.form.get('id_declinaison_article')

    sql = "SELECT * FROM ligne_panier WHERE lunette_id = %s AND utilisateur_id = %s"
    mycursor.execute(sql, (id_article, id_client))
    ligne = mycursor.fetchone()

    sql2 = "UPDATE lunette SET stock = stock + %s WHERE id_lunette = %s"
    mycursor.execute(sql2, (ligne['quantite'], id_article))

    sql = "DELETE FROM ligne_panier WHERE lunette_id = %s AND utilisateur_id = %s"
    mycursor.execute(sql, (id_article, id_client))

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    # test des variables puis
    # mise en session des variables

    if filter_word or filter_word == '':
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash('Le mot doit être composé de lettres uniquement')
        else:
            if len(filter_word) == 1:
                flash('Le mot doit contenir au moins 2 lettres')
            else:
                session.pop('filter_word', None)

    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                session['filter_prix_min'] = filter_prix_min
                session['filter_prix_max'] = filter_prix_max
            else:
                flash('Le prix minimum doit être inférieur au prix maximum')
        else:
            flash('Les prix doivent être des nombres entiers')
    if filter_types and filter_types != []:
        session['filter_types'] = filter_types

    print(session)

    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/article/show')
