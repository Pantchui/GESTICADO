import datetime

import BDD as bd


class Remplissage:
    def __init__(self, mail_utilisateur):
        self.mail_utilisateur = mail_utilisateur

    def affichage_tache(self):
        try:
            requet = "SELECT numero FROM utilisateur WHERE email = %s"
            bd.bdd_cursor.execute(requet, (self.mail_utilisateur,))
            numero = bd.bdd_cursor.fetchone()[0]

            # selection tache
            requet = "SELECT numero_tache, nom_tache, duree_tache FROM tache WHERE numero = %s AND jour_actuel = %s"
            bd.bdd_cursor.execute(requet, (numero, datetime.datetime.now().date()))
            results = bd.bdd_cursor.fetchall()
            return {"etat": True, "donnees": results}

        except:
            return {"etat": False, "msg": "Nous avons rencontre un probleme,\n"
                                          "Merci de reesayer!"}

    def heure_debut(self, num):
        try:
            requet = "SELECT numero FROM utilisateur WHERE email = %s"
            bd.bdd_cursor.execute(requet, (self.mail_utilisateur,))
            numero = bd.bdd_cursor.fetchone()[0]

            # selection tache
            requet = "UPDATE tache SET heure_debut = %s WHERE numero = %s AND jour_actuel = %s AND numero_tache = %s"
            bd.bdd_cursor.execute(requet, (datetime.datetime.now().time(), numero, datetime.datetime.now().date(), num))
            bd.bdd.commit()
            return {"etat": True}

        except:
            return {"etat": False, "msg": "Nous avons rencontre un probleme,\n"
                                          "Merci de reesayer!"}

    def fin_tache(self, temps_effectue, num):
        try:
            requet = "SELECT numero FROM utilisateur WHERE email = %s"
            bd.bdd_cursor.execute(requet, (self.mail_utilisateur,))
            numero = bd.bdd_cursor.fetchone()[0]

            # selection tache
            requet = "UPDATE tache SET temps_effectue = %s, heure_fin = %s  WHERE numero = %s " \
                     "AND jour_actuel = %s AND numero_tache = %s"
            bd.bdd_cursor.execute(requet, (temps_effectue, datetime.datetime.now().time(), numero,
                                           datetime.datetime.now().date(), num))
            bd.bdd.commit()
            return {"etat": True}

        except:
            return {"etat": False, "msg": "Nous avons rencontre un probleme,\n"
                                          "Merci de reesayer!"}
