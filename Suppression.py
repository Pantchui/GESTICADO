import BDD as bd
import os


class Suppression:

    def __init__(self, numero):
        self.numero = numero

    def suppression_compte(self):
        os.remove(f"./profil/p{self.numero}.png")
        try:
            sql = "DELETE FROM utilisateur WHERE numero = %s"
            bd.bdd_cursor.execute(sql, (self.numero,))
            bd.bdd.commit()
            return {"etat": True, "message": "Le compte a bien ete supprime !"}
        except:
            return {"etat": False, "message": "Nous avons rencontre un probleme, Veuillez reessayer !"}
