import BDD as bd
import datetime


class Bilan:

    def __init__(self, mail_utilisateur, date):
        self.mail_utilisateur = mail_utilisateur
        self.date = date

    def informations_complete(self):

        # recuperation de toute les information
        requet = "SELECT * FROM tache WHERE jour_actuel = %s AND " \
                 "numero IN (SELECT numero FROM utilisateur WHERE email = %s) ORDER BY numero_tache"
        bd.bdd_cursor.execute(requet, (self.date, self.mail_utilisateur))
        return bd.bdd_cursor.fetchall()

    def get_nbr_taches_totales(self):
        requet = "SELECT COUNT(*) FROM tache WHERE jour_actuel = %s AND " \
                 "numero IN (SELECT numero FROM utilisateur WHERE email = %s)"
        bd.bdd_cursor.execute(requet, (self.date, self.mail_utilisateur))
        return bd.bdd_cursor.fetchone()[0]

    def get_nbr_taches_effectuees(self):
        requet = "SELECT COUNT(*) FROM tache WHERE temps_effectue > 0 AND jour_actuel = %s AND " \
                 "numero IN (SELECT numero FROM utilisateur WHERE email = %s)"
        bd.bdd_cursor.execute(requet, (self.date, self.mail_utilisateur))
        return bd.bdd_cursor.fetchone()[0]

    def get_nbr_tache_avant_delai(self):
        requet = "SELECT COUNT(*) FROM tache WHERE temps_effectue > 0 AND temps_effectue < duree_tache AND " \
                 "jour_actuel = %s AND numero IN (SELECT numero FROM utilisateur WHERE email = %s)"
        bd.bdd_cursor.execute(requet, (self.date, self.mail_utilisateur))
        return bd.bdd_cursor.fetchone()[0]

    def get_nbr_tache_dans_delai(self):
        requet = "SELECT COUNT(*) FROM tache WHERE temps_effectue > 0 AND temps_effectue = duree_tache AND " \
                 "jour_actuel = %s AND numero IN (SELECT numero FROM utilisateur WHERE email = %s)"
        bd.bdd_cursor.execute(requet, (self.date, self.mail_utilisateur))
        return bd.bdd_cursor.fetchone()[0]

    def get_nbr_tache_apres_delai(self):
        requet = "SELECT COUNT(*) FROM tache WHERE temps_effectue > 0 AND temps_effectue > duree_tache AND " \
                 "jour_actuel = %s AND numero IN (SELECT numero FROM utilisateur WHERE email = %s)"
        bd.bdd_cursor.execute(requet, (self.date, self.mail_utilisateur))
        return bd.bdd_cursor.fetchone()[0]

    def get_temps_total_tache(self):
        requet = "SELECT SUM(duree_tache) FROM tache WHERE jour_actuel = %s AND " \
                 "numero IN (SELECT numero FROM utilisateur WHERE email = %s)"
        bd.bdd_cursor.execute(requet, (self.date, self.mail_utilisateur))
        return bd.bdd_cursor.fetchone()[0]

    def get_temps_total_tache_effectuees(self):
        requet = "SELECT SUM(temps_effectue) FROM tache WHERE jour_actuel = %s AND " \
                 "numero IN (SELECT numero FROM utilisateur WHERE email = %s)"
        bd.bdd_cursor.execute(requet, (self.date, self.mail_utilisateur))
        return bd.bdd_cursor.fetchone()[0]

    def get_temps_debordee(self):
        val = self.get_temps_total_tache_effectuees() - self.get_temps_total_tache()
        return val if val > 0 else 0
