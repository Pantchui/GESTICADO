import BDD as bd
from PIL import Image, ImageDraw


class Personne:

    def __init__(self, firstname, lastname, mdp1, mdp2, email, age, chemin_photo, numero):
        self.numero = numero
        self.firstname = firstname
        self.lastname = lastname
        self.mdp1 = mdp1
        self.mdp2 = mdp2
        self.email = email
        self.age = age
        self.chemin_photo = chemin_photo

    # verification des informations
    def verification(self):
        if not (self.firstname or self.lastname or self.mdp1 or self.mdp2 or self.email or self.age) == "":
            if ('@' and '.') in self.email:
                if self.mdp1 == self.mdp2:
                    try:
                        age_entier = int(self.age)
                        self.age = age_entier

                        if self.chemin_photo == "":
                            self.chemin_photo = "./res/profil-default.png"

                        return {"etat": True}

                    except:
                        return {"etat": False, "message": "Age invalide"}
                else:
                    return {"etat": False, "message": "Les mots de passe ne correspondent pas"}
            else:
                return {"etat": False, "message": "L'adresse mail n'est pas valide"}
        else:
            return {"etat": False, "message": "Completez tout les champs!"}

    def traitement_profil(self):
        if self.chemin_photo == "":
            self.chemin_photo = "./res/profil-default.png"

        image = Image.open(self.chemin_photo)
        nouvelle_image = image.resize((100, 100))

        # Définir un rayon pour les coins arrondis
        rayon = 50

        # Créer un masque arrondi
        masque = Image.new("L", nouvelle_image.size, 0)
        draw = ImageDraw.Draw(masque)
        draw.rounded_rectangle((0, 0, nouvelle_image.width, nouvelle_image.height), rayon, fill=255)

        # Appliquer le masque à l'image
        image_arrondie = Image.new("RGBA", nouvelle_image.size)
        image_arrondie.paste(nouvelle_image, mask=masque)

        # Enregistrer l'image arrondie
        image_arrondie.save(f"./profil/p{self.numero}.png")

    def insertion_donnee(self):
        try:
            requet = "SELECT COUNT(email) FROM utilisateur WHERE email = %s"
            bd.bdd_cursor.execute(requet, (self.email, ))
            req_user = bd.bdd_cursor.fetchone()[0]

            if req_user == 0:
                sql = "INSERT INTO utilisateur VALUES(%s, %s, %s, %s, %s, %s)"
                values = (self.numero, self.firstname, self.lastname, self.mdp1, self.email, self.age)
                bd.bdd_cursor.execute(sql, values)

                bd.bdd.commit()
                bd.bdd_cursor.close()
                bd.bdd.close()

                return {"etat": True, "message": "Les donnees ont bien ete ajoutees!"}
            else:
                return {"etat": False, "message": "L'adresse mail existe deja!"}
        except:
            return {"etat": False, "message": "Nous avons rencontre une erreur lors de l'insertion!\n"
                                              "Merci de reessayer!"}

