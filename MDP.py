import BDD as bd


class MDP:
    def __init__(self, email, mdp1, mdp2):
        self.email = email
        self.mdp1 = mdp1
        self.mdp2 = mdp2

    def verification(self):
        if not (self.email and self.mdp1 and self.mdp2) == "":
            if self.mdp2 == self.mdp1:
                try:
                    requet = "SELECT COUNT(email) FROM utilisateur WHERE email = %s"
                    bd.bdd_cursor.execute(requet, (self.email,))

                    req_user = bd.bdd_cursor.fetchone()[0]
                    if req_user == 1:

                        requet = "SELECT COUNT(*) FROM utilisateur WHERE email = %s AND mdp = %s"
                        bd.bdd_cursor.execute(requet, (self.email, self.mdp1))
                        req_user = bd.bdd_cursor.fetchone()[0]

                        if req_user == 0:
                            requet = "UPDATE utilisateur SET mdp = %s WHERE email %s"
                            bd.bdd_cursor.execute(requet, (self.mdp1, self.email))

                            bd.bdd.commit()
                            bd.bdd_cursor.close()
                            bd.bdd.close()
                            return {"statut": True, "msg": "Le mot de passe a bien ete modifie!"}
                        else:
                            return {"statut": False, "msg": "Le nouveau mot de passe est identique que l'ancien"}
                    else:
                        return {"statut": False, "msg": "L'adresse mail n'existe pas"}
                except:
                    return {"statut": False, "msg": "Nous avons rencontre un probleme!\n Merci de reesayer!"}
            else:
                return {"statut": False, "msg": "Les mots de passe ne correspondent pas!"}
        else:
            return {"statut": False, "msg": "Completez tout les champs!"}
