import BDD as bd


class Affichage:
    def __init__(self, email):
        self.email = email

    def information_utilisateur(self):
        sql = "SELECT * FROM utilisateur WHERE numero IN (SELECT numero FROM utilisateur WHERE email = %s)"
        bd.bdd_cursor.execute(sql, (self.email, ))
        infos = bd.bdd_cursor.fetchone()

        return infos
