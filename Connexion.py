import BDD as bd


class Connexion:
    def __init__(self, email_connect, mdp_connect):
        self.email_connect = email_connect
        self.mdp_connect = mdp_connect

    def verification(self):
        if not (self.email_connect and self.mdp_connect) == "":
            try:
                sql = "SELECT COUNT(*) FROM utilisateur WHERE email = %s and mdp = %s"
                bd.bdd_cursor.execute(sql, (self.email_connect, self.mdp_connect))

                req_user = bd.bdd_cursor.fetchone()[0]
                if req_user == 1:
                    return {"statut": True, "msg": "Connexion reussie!"}
                else:
                    return {"statut": False, "msg": "L'utilisateur n'existe pas!\nVerifiez les donnees puis reesayer!"}
            except:
                return {"statut": False, "msg": f"Nous avons rencontre une erreur lors de l'insertion!\n"
                                                "Merci de reessayer!"}
        else:
            return {"statut": False, "msg": "Completez tout les champs!"}
