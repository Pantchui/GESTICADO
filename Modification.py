import Personne
import os


class Modification(Personne.Personne):
    def __init__(self, firstname, lastname, mdp1, mdp2, email, age, chemin_photo, numero):
        super().__init__(firstname, lastname, mdp1, mdp2, email, age, chemin_photo, numero)

    def modification(self):
        try:
            # verification de l'email
            sql = "SELECT COUNT(email) FROM utilisateur WHERE email = %s"
            Personne.bd.bdd_cursor.execute(sql, (self.email, ))

            if Personne.bd.bdd_cursor.fetchone()[0] == 0:
                # selection des elements
                sql = "SELECT COUNT(*) FROM utilisateur WHERE firstName = %s AND " \
                      "lastName = %s AND mdp = %s AND email = %s AND age = %s"
                Personne.bd.bdd_cursor.execute(sql, (self.firstname, self.lastname, self.mdp1, self.email, self.age))

                if Personne.bd.bdd_cursor.fetchone()[0] == 0:
                    sql = "UPDATE utilisateur SET firstName = %s, lastName = %s, mdp = %s, email = %s, " \
                          "age = %s WHERE numero = %s"
                    Personne.bd.bdd_cursor.execute(sql, (self.firstname, self.lastname, self.mdp1, self.email,
                                                         self.age, self.numero))
                    Personne.bd.bdd.commit()

                    return {"etat": True, "message": "Les donness ont bien ete enregistre!"}
                else:
                    return {"etat": False, "message": "Les donnees sont identiques!"}
            else:
                return {"etat": False, "message": "L'adresse mail existe deja!"}
        except:
            return {"etat": False, "message": "Nous avons rencontre un probleme, Veuillez reessayer !"}

    def modification_profil(self):
        if not self.chemin_photo == "":
            photo_profil = f"./profil/p{self.numero}.png"
            os.remove(photo_profil)
            Personne.Personne.traitement_profil(self.chemin_photo)
