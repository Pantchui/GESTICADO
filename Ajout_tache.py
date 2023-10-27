import BDD as bd
import datetime


class AjoutTache:
    def __init__(self, nom_tache, duree_tahe_minute, mail_utilisateur, numero_tache):
        self.nom_tache = nom_tache
        self.duree_tahe_minute = duree_tahe_minute
        self.mail_utilisateur = mail_utilisateur
        self.numero_tache = numero_tache

    def verification(self):
        # nom tache vide
        if not self.nom_tache == "":

            # verification de la longeur
            if len(self.nom_tache) <= 100:

                return {"etat": True}
            else:
                return {"etat": False, "msg": "Le nom de la tache, est trop long!"}
        else:
            return {"etat": False, "msg": "Le nom de la tache, est vide!"}

    def ajout_de_la_tache(self):
        try:
            bd.bdd_cursor.execute("SELECT numero FROM utilisateur WHERE email = %s", self.mail_utilisateur)
            numero = bd.bdd_cursor.fetchone()[0]

            # verification de l'existence de la tache
            sql = "SELECT COUNT(nom_tache) FROM tache WHERE nom_tache = %s " \
                  "AND jour_actuel = %s AND numero = %s"
            bd.bdd_cursor.execute(sql, (self.nom_tache, datetime.datetime.now().date(), numero))

            if bd.bdd_cursor.fetchone()[0] == 0:
                sql = "INSERT INTO tache(nom_tache, duree_tache, numero_tache, jour_actuel, numero) " \
                      "VALUES(%s, %s, %s, %s, %s)"
                bd.bdd_cursor.execute(sql, (self.nom_tache, self.duree_tahe_minute,
                                            self.numero_tache, datetime.datetime.now().date(), numero))

                bd.bdd.commit()
                return {"etat": True, "msg": "La tache a bien ete ajoute!"}
            else:
                return {"etat": False, "msg": "Le vous avez deja enregistre la tache,\n"
                                              "pour la journee d'aujourd'hui!"}
        except:
            return {"etat": False, "msg": "Nous avons rencontre un probleme,\n"
                                          "Merci de reesayer!"}
