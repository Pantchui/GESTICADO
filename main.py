"""" #################################### importation de bibliotheque #################################### """
import random
import math
import time
from tkinter.filedialog import askopenfilename

import pyttsx3
import datetime

import ttkbootstrap as ttkb
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import Messagebox, Querybox

from PIL import Image, ImageTk

import Personne
import MDP
import Connexion
import Affichage
import Modification
import Suppression
import Ajout_tache
import Remplissage
import Bilan

"""" #################################### definitions de fonctions #################################### """


# ancien bilan
def ancien_bilan():
    global user_connect, type_notification_audio
    if user_connect:
        date = Querybox().get_date()
        import BDD as bd
        sql = "SELECT COUNT(*) FROM tache WHERE jour_actuel = %s AND " \
              "numero IN (SELECT numero FROM utilisateur WHERE email = %s)"

        bd.bdd_cursor.execute(sql, (date, mail_connexion.get()))
        if bd.bdd_cursor.fetchone()[0] > 0:
            show_bilan(date)
            app.update()
        else:
            if type_notification_audio:
                parler("Le jour entre n'existe pas!")
            else:
                Messagebox.show_warning(title="Attention",
                                        message="Le jour entre n'existe pas!")
    else:
        if type_notification_audio:
            parler("Connectez vous, avant d'afficher un ancien bilan!")
        else:
            Messagebox.show_warning(title="Attention",
                                    message="Connectez vous, avant d'afficher un ancien bilan!")
        actions.select(3)


# profil
def show_profil():
    global user_connect, type_notification_audio

    # suppression du compte
    def supprimer_compte():
        msg = Messagebox.okcancel(title="Confirmation suppression",
                                  message="Voulez vous supprimer votre compte?\nCette action est irreversible")
        if msg == "OK":
            suppression = Suppression.Suppression(numero_profil.get())
            erreur = suppression.suppression_compte()

            if type_notification_audio:
                parler(erreur["etat"])
            else:
                Messagebox.show_info(title="Information", message=erreur["message"])

            if erreur["etat"]:
                time.sleep(0.5)
                app.destroy()

        else:
            Messagebox.show_info(title="Information", message="Nous avons pris votre reponse en compte")

    def selection_profil():
        global profil_path_modifie
        profil_image = askopenfilename(title="Ajouter une photo de profil",
                                       filetypes=(("JPG", "*.jpg"),
                                                  ("JPEG", "*.jpeg"),
                                                  ("PNG", "*.png")), defaultextension=".jpg")
        profil_path_modifie.set(profil_image)
        if not profil_path_modifie.get() == "":
            btn_profil_modif.config(text=chemin_coupe(profil_path_modifie.get()))

    def modification():
        utilisateur_modif = Modification.Modification(prenom_profil.get(), nom_profil.get(), mdp_profil.get(),
                                                      mdp_profil.get(), mail_profil.get(), age_profil.get(),
                                                      profil_path_modifie.get(), numero_profil.get())
        erreur = utilisateur_modif.verification()
        if erreur["etat"]:
            erreur = utilisateur_modif.modification()
            if type_notification_audio:
                parler(erreur["message"])
            else:
                Messagebox.show_warning(title="Attention", message=erreur["message"])

            if erreur["etat"]:
                # modification profil
                utilisateur_modif.modification_profil()

                infos_modifiees = Affichage.Affichage(mail_connexion.get())

                # recuperation des informations
                infos_modifiee = infos_modifiees.information_utilisateur()

                # retrait anciens donnes
                prenom_profil.delete(0, ttkb.END)
                nom_profil.delete(0, ttkb.END)
                mdp_profil.delete(0, ttkb.END)
                mail_profil.delete(0, ttkb.END)
                age_profil.delete(0, ttkb.END)

                # ajout nouveau elt
                prenom_profil.insert(0, infos_modifiee[1])
                nom_profil.insert(0, infos_modifiee[2])
                mdp_profil.insert(0, infos_modifiee[3])
                mail_profil.insert(0, infos_modifiee[4])
                age_profil.insert(0, infos_modifiee[5])

        else:
            if type_notification_audio:
                parler(erreur["message"])
            else:
                Messagebox.show_warning(title="Attention", message=erreur["message"])

    if user_connect:
        user_infos = Affichage.Affichage(mail_connexion.get())

        # recuperation des informations
        user_info = user_infos.information_utilisateur()

        # creation tab
        profil = ttkb.Frame(actions)
        actions.add(profil, text="Mon compte")

        ttkb.Label(profil, text="Mon compte", bootstyle="success inverse",
                   font=("poppins", 15)).pack(fill=ttkb.X, pady=(5, 5), padx=5)

        profil_frame = ScrolledFrame(profil, height=400, autohide=True)
        profil_frame.pack(fill=ttkb.BOTH, padx=5, pady=(5, 10), ipadx=5, ipady=5)
        profil_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        img = Image.open(f"./profil/p{user_info[0]}.png")
        img_profil = ImageTk.PhotoImage(image=img, size=(300, 300))
        ttkb.Label(profil_frame, image=img_profil).grid(columnspan=4, column=0, row=0, padx=(30, 0))

        # modifier le information
        btn_modifier_compte = ttkb.Button(profil_frame, text="Modifier", bootstyle="info outline", command=modification)
        btn_modifier_compte.grid(row=0, column=4, pady=(70, 0))

        # diviser
        ttkb.Separator(profil_frame, ).grid(row=2, column=4, sticky="ew", pady=20)
        ttkb.Separator(profil_frame, ).grid(row=2, column=3, sticky="ew", pady=20)
        ttkb.Separator(profil_frame, ).grid(row=2, column=2, sticky="ew", pady=20)
        ttkb.Separator(profil_frame, ).grid(row=2, column=1, sticky="ew", pady=20)
        ttkb.Separator(profil_frame, ).grid(row=2, column=0, sticky="ew", pady=20)

        # numero
        ttkb.Label(profil_frame, text="Numero: ", font=("poppins", 13)).grid(row=3, column=0, pady=(10, 20),
                                                                             padx=(20, 0), sticky="ne")
        numero_profil = ttkb.Entry(profil_frame, font=("poppins", 10))
        numero_profil.grid(row=3, columnspan=3, column=1, pady=(10, 20), padx=(0, 20), sticky="nsew")
        numero_profil.insert(0, user_info[0])
        numero_profil.config(state=ttkb.DISABLED)

        # prenom
        ttkb.Label(profil_frame, text="Prenom: ", font=("poppins", 13)).grid(row=4, column=0, pady=(10, 20),
                                                                             padx=(20, 0), sticky="ne")
        prenom_profil = ttkb.Entry(profil_frame, font=("poppins", 10))
        prenom_profil.grid(row=4, columnspan=3, column=1, pady=(10, 20), padx=(0, 20), sticky="nsew")
        prenom_profil.insert(0, user_info[1])

        # nom
        ttkb.Label(profil_frame, text="Nom: ", font=("poppins", 13)).grid(row=5, column=0, pady=(10, 20),
                                                                          padx=(20, 0), sticky="ne")
        nom_profil = ttkb.Entry(profil_frame, font=("poppins", 10))
        nom_profil.grid(row=5, columnspan=3, column=1, pady=(10, 20), padx=(0, 20), sticky="nsew")
        nom_profil.insert(0, user_info[2])

        # adresse mail
        ttkb.Label(profil_frame, text="Adresse mail: ", font=("poppins", 13)).grid(row=6, column=0, pady=(10, 20),
                                                                                   padx=(20, 0), sticky="e")
        mail_profil = ttkb.Entry(profil_frame, font=("poppins", 10))
        mail_profil.grid(row=6, columnspan=3, column=1, pady=(10, 20), padx=(0, 20), sticky="nsew")
        mail_profil.insert(0, user_info[4])

        # age
        ttkb.Label(profil_frame, text="Age: ", font=("poppins", 13)).grid(row=7, column=0, pady=(10, 20),
                                                                          padx=(20, 0), sticky="e")
        age_profil = ttkb.Entry(profil_frame, font=("poppins", 10))
        age_profil.grid(row=7, columnspan=3, column=1, pady=(10, 20), padx=(0, 20), sticky="nsew")
        age_profil.insert(0, user_info[5])

        # mot de passe
        ttkb.Label(profil_frame, text="Mot de passe: ", font=("poppins", 13)).grid(row=8, column=0, pady=(10, 20),
                                                                                   padx=(20, 0), sticky="e")
        mdp_profil = ttkb.Entry(profil_frame, font=("poppins", 10), show="*")
        mdp_profil.grid(row=8, columnspan=3, column=1, pady=(10, 20), padx=(0, 20), sticky="nsew")
        mdp_profil.insert(0, user_info[3])

        # profil
        ttkb.Label(profil_frame, text="Ajouter un profil: ", font=("poppins", 13)).grid(row=9, column=0, pady=(10, 20),
                                                                                        padx=(20, 0), sticky="e")
        btn_profil_modif = ttkb.Button(profil_frame, text="Ajouter", bootstyle="success", command=selection_profil)
        btn_profil_modif.grid(row=9, column=1, pady=(10, 20), sticky="w")

        # supprimer le compte
        btn_supprimer_compte = ttkb.Button(profil_frame, text="Supprimer", bootstyle="danger outline",
                                           command=supprimer_compte)
        btn_supprimer_compte.grid(row=10, column=4, pady=20)


# mot de passe
def mdp_oublie():
    # modification mdp
    def modification_mdp():
        mdp_modifie = MDP.MDP(email_oublie.get(), mdp1_oublie.get(), mdp2_oublie.get())
        erreur = mdp_modifie.verification()

        if erreur["statut"]:
            Messagebox.show_info(title="Information", message=erreur["msg"])
            app_mdp.destroy()
        else:
            Messagebox.show_warning(title="Attention", message=erreur["msg"])

    app_mdp = ttkb.Toplevel(title="Mot de passe")
    app_mdp.iconbitmap("res/logo.ico")

    ttkb.Label(app_mdp, text=f"Mot de passe oublie".upper(), font=("poppins", 17, "bold"), bootstyle="success").grid(
        row=0, column=0, columnspan=2, padx=20, pady=20)

    # email
    ttkb.Label(app_mdp, text="Adresse Mail: ", font=("poppins", 13)).grid(sticky="se", padx=20, pady=10, row=1,
                                                                          column=0)
    email_oublie = ttkb.Entry(app_mdp, font=("poppins", 10), width=35, style="TEntry")
    email_oublie.grid(row=1, column=1, pady=10, padx=20, sticky="w")

    # mdp1
    ttkb.Label(app_mdp, font=("poppins", 13), text="Nouveau Mot de passe: ").grid(sticky="se", padx=20, pady=10, row=2,
                                                                                  column=0)
    mdp1_oublie = ttkb.Entry(app_mdp, show="*", font=("poppins", 10), width=35, style="TEntry")
    mdp1_oublie.grid(row=2, column=1, pady=10, padx=20, sticky="w")

    # mdp2
    ttkb.Label(app_mdp, font=("poppins", 13), text="Confirmez: ").grid(sticky="se", padx=20, pady=10, row=3, column=0)
    mdp2_oublie = ttkb.Entry(app_mdp, show="*", font=("poppins", 10), width=35, style="TEntry")
    mdp2_oublie.grid(row=3, column=1, pady=10, padx=20, sticky="w")

    btn_oublie = ttkb.Button(app_mdp, text="Modifier", bootstyle="success", command=modification_mdp)
    btn_oublie.grid(row=4, column=1, pady=20, padx=20, sticky="se")

    app_mdp.mainloop()


# couper chemin
def chemin_coupe(chemin_complet):
    nouveau_chemin = chemin_complet[len(chemin_complet) - 18:]
    nouveau_chemin = "..." + nouveau_chemin

    return nouveau_chemin


# fermer
def fermer():
    app.destroy()


# fin journee
def fermer_journee():
    global type_notification_audio
    import BDD
    # enregistrez les donnees
    try:
        # recuperation du numero
        sql = "UPDATE tache SET fin_journee = %s WHERE jour_actuel = %s AND " \
              "numero IN (SELECT numero FROM utilisateur WHERE email = %s)"
        BDD.bdd_cursor.execute(sql, (1, datetime.datetime.now().date(),  mail_connexion.get()))
        BDD.bdd.commit()

        fin_tache.config(state=ttkb.DISABLED)
        fin_journee.config(state=ttkb.DISABLED)
        debut_tache.config(state=ttkb.DISABLED)
        selection_numero_tache.config(state=ttkb.DISABLED)
        show_bilan()
        actions.select(2)

    except:
        if type_notification_audio:
            parler("Nous avons rencontre un probleme, Merci de reesayer!")
        else:
            Messagebox.show_warning(title="Attention", message="Nous avons rencontre un probleme,\n"
                                                               "Merci de reesayer!")


# gestion du bilan
def show_bilan(date=datetime.datetime.now().date()):
    # gestion des bilan
    bilan_utilisateur = Bilan.Bilan(mail_connexion.get(), date)
    titre_bilan.config(text=f"Rapport journalier: {date}")

    """" #################################### bilan #################################### """

    # supression de l'element
    bilan_texte.grid_forget()

    # rapport general graphique
    ttkb.Label(bilan_frame, text="Rapport général", font=("poppins", 13)).grid(row=1, pady=20, column=0,
                                                                               columnspan=3,
                                                                               sticky="w")
    style = ttkb.Style()
    style.configure("B.TLabel", font=("poppins", 5))

    # meter
    if round((bilan_utilisateur.get_nbr_taches_effectuees() / bilan_utilisateur.get_nbr_taches_totales()) * 100) > 50:
        ttkb.Meter(bilan_frame, bootstyle="success", metertype="semi", subtextstyle="B.TLabel",
                   textright=f"/{bilan_utilisateur.get_nbr_taches_totales()} tâches", metersize=130, interactive=False,
                   textfont=("poppins", 12, "bold"),
                   subtext="complétées", subtextfont=("poppins", 7),
                   amounttotal=bilan_utilisateur.get_nbr_taches_totales(), stripethickness=24,
                   amountused=bilan_utilisateur.get_nbr_taches_effectuees()).grid(row=2, column=0, pady=20, padx=(0, 5))
    else:
        ttkb.Meter(bilan_frame, bootstyle="danger", metertype="semi", subtextstyle="B.TLabel",
                   textright=f"/{bilan_utilisateur.get_nbr_taches_totales()} tâches", metersize=130, interactive=False,
                   textfont=("poppins", 12, "bold"),
                   subtext="complétées", subtextfont=("poppins", 7),
                   amounttotal=bilan_utilisateur.get_nbr_taches_totales(), stripethickness=24,
                   amountused=bilan_utilisateur.get_nbr_taches_effectuees()).grid(row=2, column=0, pady=20, padx=(0, 5))

    # temps
    if bilan_utilisateur.get_temps_total_tache() > bilan_utilisateur.get_temps_total_tache_effectuees():
        ttkb.Meter(bilan_frame, bootstyle="success", metertype="semi", subtextstyle="B.TLabel",
                   textright=f"/{bilan_utilisateur.get_temps_total_tache()}min", metersize=130, interactive=False,
                   textfont=("poppins", 12, "bold"), stripethickness=24, subtext="consommées",
                   subtextfont=("poppins", 7), amounttotal=bilan_utilisateur.get_temps_total_tache(),
                   amountused=bilan_utilisateur.get_temps_total_tache_effectuees()).grid(row=2, column=1, pady=20,
                                                                                         padx=5)
    else:
        ttkb.Meter(bilan_frame, bootstyle="danger", metertype="semi", subtextstyle="B.TLabel",
                   textright=f"/{bilan_utilisateur.get_temps_total_tache()}min", metersize=130, interactive=False,
                   textfont=("poppins", 12, "bold"), subtext="consommées", subtextfont=("poppins", 7),
                   amounttotal=bilan_utilisateur.get_temps_total_tache(),
                   stripethickness=24,
                   amountused=bilan_utilisateur.get_temps_total_tache_effectuees()).grid(row=2, column=1, pady=20,
                                                                                         padx=5)

    # debordement
    if bilan_utilisateur.get_temps_debordee() < 60:
        ttkb.Meter(bilan_frame, bootstyle="success", metertype="semi", subtextstyle="B.TLabel",
                   textright="min/160", metersize=130, interactive=False, textfont=("poppins", 12, "bold"),
                   subtext="ajoutés", amountused=bilan_utilisateur.get_temps_debordee(), subtextfont=("poppins", 7),
                   amounttotal=160,
                   stripethickness=24).grid(row=2, column=2, pady=20, padx=(5, 0))
    else:
        ttkb.Meter(bilan_frame, bootstyle="danger", metertype="semi", subtextstyle="B.TLabel",
                   textright="min/160", metersize=130, interactive=False, textfont=("poppins", 12, "bold"),
                   subtext="ajoutés", amountused=bilan_utilisateur.get_temps_debordee(), subtextfont=("poppins", 7),
                   amounttotal=160,
                   stripethickness=24).grid(row=2, column=2, pady=20, padx=(5, 0))

    # rapport par taches
    ttkb.Label(bilan_frame, text="Rapport par tâche", font=("poppins", 13)).grid(row=3, pady=20, column=0,
                                                                                 columnspan=3,
                                                                                 sticky="w")

    style = ttkb.Style()
    style.configure("B.TLabel", font=("poppins", 5))

    # meter
    r, c = 4, 0
    for toutes_les_information in bilan_utilisateur.informations_complete():
        if toutes_les_information[2] > toutes_les_information[1]:
            ttkb.Meter(bilan_frame, bootstyle="danger", subtextstyle="B.TLabel",
                       textright=f"min/{toutes_les_information[1]}", metersize=130,
                       textfont=("poppins", 12, "bold"),
                       subtext=f"tâche {toutes_les_information[3]}", subtextfont=("poppins", 7),
                       amounttotal=toutes_les_information[1],
                       amountused=toutes_les_information[2]).grid(row=r, column=c, pady=20, padx=5)
        else:
            ttkb.Meter(bilan_frame, bootstyle="success", subtextstyle="B.TLabel",
                       textright=f"min/{toutes_les_information[1]}", metersize=130,
                       textfont=("poppins", 12, "bold"),
                       subtext=f"tâche {toutes_les_information[3]}", subtextfont=("poppins", 7),
                       amounttotal=toutes_les_information[1],
                       amountused=toutes_les_information[2]).grid(row=r, column=c, pady=20, padx=5)
        c += 1
        if c == 3:
            r += 1
            c = 0

    # rapport detaille par tache
    r = r + 1
    ttkb.Label(bilan_frame, text="Rapport détaillé par tâche", font=("poppins", 13)).grid(row=r,
                                                                                          pady=(20, 10),
                                                                                          column=0,
                                                                                          columnspan=3,
                                                                                          sticky="w")
    frame_detail = ttkb.Frame(bilan_frame)
    frame_detail.grid(row=r + 1, column=0, columnspan=3)
    frame_detail.grid_columnconfigure((0, 1, 2, 3), weight=1)
    nbr_tour = 0
    c = 0
    l = 0
    for toutes_les_information in bilan_utilisateur.informations_complete():
        if toutes_les_information[2] > 0:
            ttkb.Label(frame_detail, font=("poppins", 10), bootstyle="info",
                       text=f"{toutes_les_information[3]} - {toutes_les_information[0]}\n"
                            f"  Numero: {toutes_les_information[6]}\n"
                            f"  Jour: {toutes_les_information[4]}.\n"
                            f"  Duree: {toutes_les_information[1]}min\n"
                            f"  Temps effectué: {toutes_les_information[2]}min.\n"
                            f"  (de {toutes_les_information[7]} a {toutes_les_information[8]})"
                       ).grid(row=l, pady=20, padx=20, column=c, columnspan=2, sticky="w")
            nbr_tour += 1
            if nbr_tour == 1:
                c = 2
            elif nbr_tour == 2:
                c = 0
                nbr_tour = 0
                l += 1

    # rapport debordement de duree
    r = r + 2
    ttkb.Label(bilan_frame, text="Rapport débordement de durée", font=("poppins", 13)).grid(row=r, pady=(20, 10),
                                                                                            column=0, columnspan=3,
                                                                                            sticky="w")
    r = r + 2
    exist = False
    for toutes_les_information in bilan_utilisateur.informations_complete():
        if toutes_les_information[2] > toutes_les_information[1]:
            ttkb.Label(bilan_frame,
                       text=f"{toutes_les_information[3]}. {toutes_les_information[0]}: {toutes_les_information[2] - toutes_les_information[1]} minutes",
                       font=("poppins", 12),
                       bootstyle="danger").grid(row=r, column=0, columnspan=3, sticky="w", padx=(15, 0))
            r += 1
            exist = True

    if not exist:
        ttkb.Label(bilan_frame,
                   text=f"Pas de tâches",
                   font=("poppins", 12),
                   bootstyle="info").grid(row=r, column=0, columnspan=3, sticky="w", padx=(15, 0))

    # rapport general theorique
    ttkb.Label(bilan_frame, text="Rapport géneral théorique", font=("poppins", 13)).grid(row=r + 4, pady=(20, 10),
                                                                                         column=0,
                                                                                         columnspan=3, sticky="w")

    ttkb.Label(bilan_frame,
               text=f"Accomplissement des tâches: "
                    f"{round((bilan_utilisateur.get_nbr_taches_effectuees() / bilan_utilisateur.get_nbr_taches_totales()) * 100)}%",
               font=("poppins", 12),
               bootstyle="info").grid(row=r + 5, column=0, columnspan=3, sticky="w", padx=(15, 0))
    ttkb.Label(bilan_frame,
               text=f"Utilisation du temps: "
                    f"{round((bilan_utilisateur.get_temps_total_tache_effectuees() / bilan_utilisateur.get_temps_total_tache()) * 100)}%",
               font=("poppins", 12),
               bootstyle="info").grid(row=r + 6, column=0, columnspan=3, sticky="w", padx=(15, 0))
    ttkb.Label(bilan_frame,
               text=f"Temps ajoutée: "
                    f"{round((bilan_utilisateur.get_temps_debordee() / bilan_utilisateur.get_temps_total_tache()) * 100)}% du temps initial",
               font=("poppins", 12),
               bootstyle="info").grid(row=r + 7, column=0, columnspan=3, sticky="w", padx=(15, 0))
    ttkb.Label(bilan_frame,
               text=f"Tâches non terminées: "
                    f"{round(100 - ((bilan_utilisateur.get_nbr_taches_effectuees() / bilan_utilisateur.get_nbr_taches_totales()) * 100))}%",
               font=("poppins", 12),
               bootstyle="info").grid(row=r + 8, column=0, columnspan=3, sticky="w", padx=(15, 0))

    ttkb.Separator(bilan_frame, bootstyle="info").grid(row=r + 9, column=0, columnspan=3, sticky="nsew",
                                                       padx=(15, 0), pady=20)

    ttkb.Label(bilan_frame,
               text=f"Tâches terminées avant le delai: {round((bilan_utilisateur.get_nbr_tache_avant_delai() / bilan_utilisateur.get_nbr_taches_effectuees()) * 100)}% ({bilan_utilisateur.get_nbr_tache_avant_delai()} tâche(s)/{bilan_utilisateur.get_nbr_taches_effectuees()})",
               font=("poppins", 12),
               bootstyle="info").grid(row=r + 10, column=0, columnspan=3, sticky="w", padx=(15, 0))
    ttkb.Label(bilan_frame,
               text=f"Tâches terminées dans le delai: {round((bilan_utilisateur.get_nbr_tache_dans_delai() / bilan_utilisateur.get_nbr_taches_effectuees()) * 100)}% ({bilan_utilisateur.get_nbr_tache_dans_delai()} tâche(s)/{bilan_utilisateur.get_nbr_taches_effectuees()})",
               font=("poppins", 12),
               bootstyle="info").grid(row=r + 11, column=0, columnspan=3, sticky="w", padx=(15, 0))
    ttkb.Label(bilan_frame,
               text=f"Tâches terminées après le delai: {round((bilan_utilisateur.get_nbr_tache_apres_delai() / bilan_utilisateur.get_nbr_taches_effectuees()) * 100)}% ({bilan_utilisateur.get_nbr_tache_apres_delai()} tâche(s)/{bilan_utilisateur.get_nbr_taches_effectuees()})",
               font=("poppins", 12),
               bootstyle="info").grid(row=r + 12, column=0, columnspan=3, sticky="w", padx=(15, 0))

    ttkb.Button(bilan_frame, text="Fermer", bootstyle="outline danger",
                command=fermer).grid(row=r + 13, column=2, pady=(30, 10))


# fin de tache
def finission_tache(nums, num_actuel):
    global tache_encours, label_taches, temps_ecoule_tache

    # arret
    tache_encours = False
    chronometre()

    # gestion temps ecoule
    temps_ecoule_minute = math.ceil(temps_ecoule_tache / 60)

    if temps_ecoule_minute == 0:
        temps_ecoule_minute = 1

    # enregistrez les donnees
    fintache = Remplissage.Remplissage(mail_connexion.get())
    erreur = fintache.fin_tache(temps_ecoule_minute, num_actuel)

    if erreur["etat"]:
        label_tache = label_taches[int(num_actuel) - 1]
        label_tache[0].config(bootstyle="success")
        label_tache[1].config(bootstyle="success")
        fin_tache.config(state=ttkb.DISABLED)
        fin_journee.config(state=ttkb.ACTIVE, command=fermer_journee)
        show_bilan()

        if len(nums) != 0:
            debut_tache.config(state=ttkb.ACTIVE)
    else:
        global type_notification_audio
        if type_notification_audio:
            parler(erreur["msg"])
        else:
            Messagebox.show_warning(title="Attention", message=erreur["msg"])


# chronomrtre
def chronometre():
    global tache_encours, temps_ecoule_tache
    # demarrage du compte a rebour
    h = int(temps_ecoule_tache / 3600)
    m = int((temps_ecoule_tache % 3600) / 60)
    s = int(temps_ecoule_tache % 60)

    temps_formatte = f"{h:02d}h {m:02d}m {s:02d}s"
    temps_tache.config(text=temps_formatte)

    if tache_encours:
        temps_ecoule_tache += 1
        temps_tache.after(1000, chronometre)


# debut tache
def debuter_tache():
    global label_taches, tache_encours, temps_ecoule_tache

    # remise du temps a 0
    temps_ecoule_tache = 0

    # gestion de numero
    num_actuel = selection_numero_tache.get()
    nums = selection_numero_tache.cget('values')
    label_tache = label_taches[int(num_actuel) - 1]

    label_tache[0].config(bootstyle="warning", font=('poppins', 12, 'bold'))
    label_tache[1].config(bootstyle="warning", font=('poppins', 12, 'bold'))
    nums = list(nums)
    nums.remove(num_actuel)
    if len(nums) == 0:
        selection_numero_tache.config(state=ttkb.DISABLED)
    else:
        selection_numero_tache.config(values=nums)
        selection_numero_tache.current(0)

    # update heure de debut
    heuredebut = Remplissage.Remplissage(mail_connexion.get())
    erreur = heuredebut.heure_debut(num_actuel)
    if erreur["etat"]:

        # activation et descativation
        fin_journee.config(state=ttkb.DISABLED)
        debut_tache.config(state=ttkb.DISABLED)
        fin_tache.config(state=ttkb.ACTIVE, command=lambda: finission_tache(nums, num_actuel))

        # chronometre
        tache_encours = True
        chronometre()
    else:
        global type_notification_audio
        if type_notification_audio:
            parler(erreur["msg"])
        else:
            Messagebox.show_warning(title="Attention", message=erreur["msg"])


# debut de journee
def debuter_journee():
    debutjournee = Remplissage.Remplissage(mail_connexion.get())
    erreur = debutjournee.affichage_tache()

    if erreur["etat"]:
        nums = []
        resultats = erreur["donnees"]
        for i in range(len(resultats)):
            nums.append(resultats[i][0])
        nums = sorted(nums)
        selection_numero_tache.config(values=nums, state=ttkb.ACTIVE)
        selection_numero_tache.current(0)
        actions.hide(0)
        actions.select(1)

        # desactivation  des champs
        tache.config(state=ttkb.DISABLED)
        ajouter_tache.config(state=ttkb.DISABLED)
        debut_journee.config(state=ttkb.DISABLED)

        # activations des champs
        debut_tache.config(state=ttkb.ACTIVE)
        fin_journee.config(state=ttkb.ACTIVE, command=fermer_journee)

    else:
        global type_notification_audio
        if type_notification_audio:
            parler(erreur["msg"])
        else:
            Messagebox.show_warning(title="Attention", message=erreur["msg"])


# remplissage
def remplissage():
    # verification si la taches exite
    debut_journee.config(state=ttkb.ACTIVE)
    visualisation_texte.grid_forget()

    remplissage_tache = Remplissage.Remplissage(mail_connexion.get())
    erreur = remplissage_tache.affichage_tache()

    if erreur["etat"]:
        results = erreur["donnees"]

        global label_taches, label_taches_warm
        i = 2
        result_tries = sorted(results, key=lambda x: x[0])
        for result_trie in result_tries:
            numero_duree = ttkb.Label(visualisation, text=f"{result_trie[0]}. {result_trie[2]}min",
                                      font=("poppins", 11))
            numero_duree.grid(row=i, column=0, padx=20, pady=15, sticky="w")

            nom = ttkb.Label(visualisation, text=result_trie[1], font=("poppins", 11))
            nom.grid(row=i, column=1, columnspan=2, padx=20, pady=15, sticky="w")
            i += 1

            label_taches.append((numero_duree, nom))
    else:
        global type_notification_audio
        if type_notification_audio:
            parler(erreur["msg"])
        else:
            Messagebox.show_warning(title="Attention", message=erreur["msg"])


# text to speech
def parler(texte):
    # initialisation
    engime = pyttsx3.init()

    # augmentation de la vitesse
    engime.setProperty('rate', 150)

    # defintion des voix
    voices = engime.getProperty('voices')
    engime.setProperty('voice', voices[0].id)

    # parler
    engime.say(texte)
    engime.runAndWait()


# changement parametre
def change_parametre():
    global type_notification_audio
    theme_style = ttkb.Style(theme=theme.get().lower())
    if notification.get() == "Audio":
        type_notification_audio = True
        parler("Maintenant, vous allez être notifié de manière audio.")
    else:
        type_notification_audio = False
        Messagebox.show_info(message="Maintenant, vous allez être notifié par texte.",
                             title="Information notification")


def show_inscription():
    # blocquer le button
    inscription_btn.config(state=ttkb.DISABLED)

    # confirmation d'annulation
    def confirmation_fermeture():
        msg = Messagebox.okcancel(title="Confirmation", message="Etes vous sur de vouloir annuler l'inscription?")
        if msg == "OK":
            app_inscription.destroy()
            inscription_btn.config(state=ttkb.ACTIVE)
        else:
            Messagebox.show_warning(title="Information", message="Nous avons pris en compte votre choix!")

    # choix profil
    def selection_profil():
        global profil_path
        profil_image = askopenfilename(title="Ajouter une photo de profil",
                                       filetypes=(("JPG", "*.jpg"),
                                                  ("JPEG", "*.jpeg"),
                                                  ("PNG", "*.png")), defaultextension=".jpg")
        profil_path.set(profil_image)
        if not profil_path.get() == "":
            btn_profil.config(text=chemin_coupe(profil_path.get()))

    # inscription
    def inscription():

        global type_notification_audio, profil_path, user_connect

        # numero
        numero = str(datetime.datetime.now().year) + str(random.randint(1000, 9999))

        # verification des champs
        person = Personne.Personne(prenom.get(), nom.get(), mdp1.get(), mdp2.get(), mail.get(),
                                   age.get(), profil_path.get(), numero)

        erreur = person.verification()
        if erreur["etat"]:
            erreur = person.insertion_donnee()
            if erreur["etat"]:
                if type_notification_audio:
                    parler(erreur["message"])
                else:
                    Messagebox.show_info(title="Informatipn", message=erreur["message"], bootstyle="success")
                person.traitement_profil()

                mail_connexion.insert(0, f"{mail.get()}")
                mdp_connexion.insert(0, f"{mdp1.get()}")

                app_inscription.destroy()
                user_connect = True

                actions.hide(3)
                show_profil()
                actions.select(5)

                # existence
                existance()

            else:
                if type_notification_audio:
                    parler(erreur["message"])
                else:
                    Messagebox.show_warning(title="Attention", message=erreur["message"], bootstyle="success")
        else:
            if type_notification_audio:
                parler(erreur["message"])
            else:
                Messagebox.show_warning(title="Attention", message=erreur["message"], bootstyle="success")

    # confirmation fermeture
    global image_label

    app_inscription = ttkb.Toplevel()
    app_inscription.title("GESTICADO - INSCRIPTION")
    app_inscription.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
    # app_inscription.geometry("500x500")

    # texte principale
    ttkb.Label(app_inscription, text="Inscription", image=image_label, compound="left", font=("poppins", 30, "bold"),
               bootstyle="success").grid(row=0, columnspan=8, column=0, pady=20, padx=25)

    # prenom
    ttkb.Label(app_inscription, text="Prenom: ", font=("poppins", 13)).grid(row=1, column=0, pady=(10, 20),
                                                                            padx=(20, 0), sticky="ne")
    prenom = ttkb.Entry(app_inscription, font=("poppins", 10))
    prenom.grid(row=1, columnspan=3, column=1, pady=(10, 20), padx=(0, 20), sticky="nsew")

    # nom
    ttkb.Label(app_inscription, text="Nom: ", font=("poppins", 13)).grid(row=1, column=4, pady=(10, 20),
                                                                         padx=(20, 0), sticky="ne")
    nom = ttkb.Entry(app_inscription, font=("poppins", 10))
    nom.grid(row=1, columnspan=3, column=5, pady=(10, 20), padx=(0, 20), sticky="nsew")

    # adresse mail
    ttkb.Label(app_inscription, text="Adresse mail: ", font=("poppins", 13)).grid(row=2, column=0, pady=(10, 20),
                                                                                  padx=(20, 0), sticky="e")
    mail = ttkb.Entry(app_inscription, font=("poppins", 10))
    mail.grid(row=2, columnspan=3, column=1, pady=(10, 20), padx=(0, 20), sticky="nsew")

    # age
    ttkb.Label(app_inscription, text="Age: ", font=("poppins", 13)).grid(row=2, column=4, pady=(10, 20),
                                                                         padx=(20, 0), sticky="e")
    age = ttkb.Entry(app_inscription, font=("poppins", 10))
    age.grid(row=2, columnspan=3, column=5, pady=(10, 20), padx=(0, 20), sticky="nsew")

    # mot de passe
    ttkb.Label(app_inscription, text="Mot de passe: ", font=("poppins", 13)).grid(row=3, column=0, pady=(10, 20),
                                                                                  padx=(20, 0), sticky="e")
    mdp1 = ttkb.Entry(app_inscription, font=("poppins", 10), show="*")
    mdp1.grid(row=3, columnspan=3, column=1, pady=(10, 20), padx=(0, 20), sticky="nsew")

    # confirmation mot de passe
    ttkb.Label(app_inscription, text="Confirmation: ", font=("poppins", 13)).grid(row=3, column=4, pady=(10, 20),
                                                                                  padx=(20, 0), sticky="e")
    mdp2 = ttkb.Entry(app_inscription, font=("poppins", 10), show="*")
    mdp2.grid(row=3, columnspan=3, column=5, pady=(10, 20), padx=(0, 20), sticky="nsew")

    # profil
    ttkb.Label(app_inscription, text="Ajouter un profil: ", font=("poppins", 13)).grid(row=4, column=0, pady=(10, 20),
                                                                                       padx=(20, 0), sticky="e")
    btn_profil = ttkb.Button(app_inscription, text="Ajouter", bootstyle="success",
                             command=selection_profil)
    btn_profil.grid(row=4, column=1, pady=(10, 20), sticky="w")

    # btn_valid
    btn_inscription = ttkb.Button(app_inscription, text="Inscription", bootstyle="success outline",
                                  command=inscription)
    btn_inscription.grid(row=4, column=7, pady=20, padx=20, sticky="e")

    app_inscription.protocol("WM_DELETE_WINDOW", confirmation_fermeture)


# connexion
def connexion():
    global user_connect, type_notification_audio
    connect = Connexion.Connexion(mail_connexion.get(), mdp_connexion.get())

    # verification
    erreur = connect.verification()
    if erreur["statut"]:
        # configuration des champs
        btn_connexion.config(state=ttkb.DISABLED)
        inscription_btn.config(state=ttkb.DISABLED)
        oublie_mdp.config(state=ttkb.DISABLED)

        mail_connexion.config(state=ttkb.DISABLED)
        mdp_connexion.config(state=ttkb.DISABLED)

        user_connect = True
        actions.hide(3)
        show_profil()
        actions.select(5)

        # existence
        existance()

        if type_notification_audio:
            parler(erreur["msg"])
        else:
            Messagebox.show_info(title="Information", message=erreur["msg"])

    else:
        if type_notification_audio:
            parler(erreur["msg"])
        else:
            Messagebox.show_warning(title="Attention", message=erreur["msg"])


# choix duree
def change_duree(e):
    if unite.get() == "Heures":
        duree.config(values=[1, 2, 3, 4, 5, 6])
    else:
        duree.config(values=[2, 5, 10, 15, 30, 45])
    duree.current(0)


# ajout de taches
def add_task():
    global type_notification_audio, user_connect, tableau_numero_tache

    # verification de la connexion
    if user_connect:

        # verification unite
        if unite.get() == "Heures":
            duree_minute = int(duree.get()) * 60
        else:
            duree_minute = int(duree.get())

        ajouttache = Ajout_tache.AjoutTache(tache.get(), duree_minute, mail_connexion.get(), numero_tache.get())
        erreur = ajouttache.verification()

        if erreur["etat"]:
            erreur = ajouttache.ajout_de_la_tache()
            if type_notification_audio:
                parler(erreur["msg"])
            else:
                Messagebox.show_warning(title="Attention", message=erreur["msg"])

            if erreur["etat"]:
                # detection position
                plein_tache = False
                for j in range(len(tableau_numero_tache)):
                    if int(numero_tache.get()) == tableau_numero_tache[j]:
                        del tableau_numero_tache[j]
                        if not len(tableau_numero_tache) == 0:
                            numero_tache.config(values=tableau_numero_tache)
                            numero_tache.current(0)
                            tache.delete(0, ttkb.END)
                        else:
                            numero_tache.config(state=ttkb.DISABLED)
                            ajouter_tache.config(state=ttkb.DISABLED)
                            plein_tache = True
                        break

                # si on a atteint la limite
                if plein_tache:
                    # notification
                    if type_notification_audio:
                        parler("Vous avez déjà atteint la limite de neuf tâches, vous ne pouvez plus ajouter de "
                               "tâche!")
                    else:
                        Messagebox.show_info(title="Ajout de tache", bootstyle="success",
                                             message="Vous avez déjà atteint la limite de neuf tâches\n "
                                                     "Vous ne pouvez plus ajouter de tâche!")
                remplissage()
        else:
            if type_notification_audio:
                parler(erreur["msg"])
            else:
                Messagebox.show_warning(title="Attention", message=erreur["msg"])
    else:
        if type_notification_audio:
            parler("Désolé vous n'êtes pas connecté! "
                   "Connectez vous ou inscrivez vous, pour ajouter des tâches")
        else:
            Messagebox.show_info(title="Ajout tâches",
                                 message="Désolé vous n'êtes pas connecté! \n"
                                         "Connectez vous ou inscrivez vous, pour ajouter des tâches",
                                 bootstyle="success")


def increment():
    progress.step(1)
    if int(progress.variable.get()) + 1 == 100:
        app.withdraw()
        time.sleep(1)
        frame.pack(ipadx=10, ipady=10, padx=10, pady=10, fill=ttkb.BOTH, expand=True)
        acceuil.pack_forget()
        app.deiconify()
        return
    progress.after(100, increment)


def commencer():
    progress.grid(columnspan=3, column=0)
    increment()


# verification existence
def existance():
    import BDD
    global tache_exits, tableau_numero_tache, type_notification_audio

    BDD.bdd_cursor.execute("SELECT COUNT(*) FROM tache WHERE fin_journee = %s AND jour_actuel = %s AND "
                           "numero IN (SELECT numero FROM utilisateur WHERE email = %s)",
                           (1, datetime.datetime.now().date(), mail_connexion.get()))

    if BDD.bdd_cursor.fetchone()[0] > 0:
        if type_notification_audio:
            parler("Vous avez, ferme votre journee")
        else:
            Messagebox.show_info(title="Info", message="Vous avez deja ferme votre journee")
        actions.hide(0)
        actions.select(2)
        show_bilan()

    else:
        if not len(tableau_numero_tache) == 0:
            # selection de numero
            BDD.bdd_cursor.execute("SELECT numero_tache FROM tache WHERE jour_actuel = %s AND fin_journee = %s AND "
                                   "numero  IN (SELECT numero FROM utilisateur WHERE email = %s AND mdp = %s)",
                                   (datetime.datetime.now().date(), 0, mail_connexion.get(), mdp_connexion.get()))
            resultats = BDD.bdd_cursor.fetchall()
            if len(resultats) > 0:
                tache_exits = True

                for resultat in resultats:
                    tableau_numero_tache.remove(resultat[0])

                numero_tache.config(values=tableau_numero_tache)
                numero_tache.current(0)
                remplissage()

        else:
            ajouter_tache.config(state=ttkb.DISABLED)
            debut_journee.config(state=ttkb.ACTIVE)
            tache.config(state=ttkb.DISABLED)
            numero_tache.config(state=ttkb.DISABLED)
            remplissage()


# creation app
app = ttkb.Window(themename="superhero")
app.geometry("500x500")
app.iconbitmap("res/logo.ico")
app.iconbitmap(default="res/logo.ico")
app.title("GESTICADO")

# variable globale
choix_unite = ""
user_connect = False
type_notification_audio = False
label_taches = []
label_taches_warm = []
tache_exits = False
tache_encours = False
temps_ecoule_tache = 0
profil_path = ttkb.StringVar(value="")
profil_path_modifie = ttkb.StringVar(value="")

# retrait tableau numero de tache
tableau_numero_tache = [1, 2, 3, 4, 5, 6, 7, 8, 9]

"""####################################### Acceuil #############################"""

acceuil = ttkb.Frame(app)
acceuil.pack(fill=ttkb.BOTH, expand=True)
acceuil.grid_columnconfigure((0, 1, 2), weight=1)

image = Image.open("res/logo.png")
image_reduit = image.resize((int(image.size[0] * 0.2), int(image.size[1] * 0.2)))
image_label = ImageTk.PhotoImage(image=image_reduit)

ttkb.Label(acceuil, image=image_label).grid(row=0, column=0, columnspan=3, pady=(20, 0))
ttkb.Label(acceuil, text="GESTICADO", bootstyle="success", font=("poppins", 20, "bold")).grid(column=0, columnspan=3,
                                                                                              row=1,
                                                                                              sticky="ns", pady=(0, 50))

# app.grid_rowconfigure(2, weight=1)
ttkb.Button(acceuil, text="Commencer", bootstyle="success outline", command=commencer).grid(columnspan=3, column=0,
                                                                                            row=3,
                                                                                            pady=(5, 195))
var = ttkb.IntVar()
progress = ttkb.Floodgauge(acceuil, bootstyle="success", length=500, value=0, maximum=100, font=("poppins", 15),
                           mask="Chargement... {}%", variable=var, mode="determinate")

# creation frame
frame = ttkb.Frame(app, bootstyle="dark")

# creation notebook
actions = ttkb.Notebook(frame, bootstyle="dark", height=410)
actions.pack(pady=10, padx=10, ipady=10, ipadx=5, fill=ttkb.BOTH)

# creation tab notebook
ajout_tache = ttkb.Frame(actions)
visualisation_tache = ttkb.Frame(actions)
bilan = ttkb.Frame(actions)
identification = ttkb.Frame(actions)
parametre = ttkb.Frame(actions)

# ajout dans le notebook
actions.add(ajout_tache, text="Ajout tâches")
actions.add(visualisation_tache, text="Visualisation tâches")
actions.add(bilan, text="Rapport")
actions.add(identification, text="Identification")
actions.add(parametre, text="Paramétre")
actions.select(3)

"""" #################################### traitement ajout taches #################################### """
ajout_frame = ttkb.Frame(ajout_tache)
ajout_frame.pack(fill=ttkb.BOTH, expand=True)
ajout_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

# titre principale
ttkb.Label(ajout_frame, text="Ajout de tâches", font=("poppins", 15),
           bootstyle="success inverse").grid(row=0, columnspan=4, column=0, pady=(5, 40),
                                             padx=5, sticky="nsew")

# les actions
ttkb.Label(ajout_frame, text="Tâches: ", font=("poppins", 13)).grid(row=2, columnspan=2, column=0, pady=(0, 20),
                                                                    sticky="e", padx=(25, 0))
tache = ttkb.Entry(ajout_frame, font=("poppins", 10), width=35, style="TEntry")
tache.grid(row=2, columnspan=2, column=2, pady=(0, 20), padx=(0, 25))

# numero de tache
ttkb.Label(ajout_frame, text="N. tâche: ", font=("poppins", 13)).grid(row=3, columnspan=2, column=0, pady=(0, 20),
                                                                      sticky="e", padx=(25, 0))
numero_tache = ttkb.Combobox(ajout_frame, font=("poppins", 13), values=tableau_numero_tache, width=25)
numero_tache.grid(row=3, columnspan=2, column=2, pady=(0, 20), padx=(0, 25))
numero_tache.current(0)

ttkb.Label(ajout_frame, text="Unité: ", font=("poppins", 13)).grid(row=4, columnspan=2, column=0, pady=(0, 20),
                                                                   sticky="e", padx=(25, 0))
unite = ttkb.Combobox(ajout_frame, font=("poppins", 13), values=["Heures", "Minutes"], width=25)
unite.bind("<<ComboboxSelected>>", change_duree)
unite.grid(row=4, columnspan=2, column=2, pady=(0, 20), padx=(0, 25))
unite.current(0)

ttkb.Label(ajout_frame, text="Durée: ", font=("poppins", 13)).grid(row=5, columnspan=2, column=0, pady=(0, 20),
                                                                   sticky="e", padx=(25, 0))

duree = ttkb.Combobox(ajout_frame, font=("poppins", 13), width=25, values=[1, 2, 3, 4, 5, 6])
duree.grid(row=5, columnspan=2, column=2, pady=(0, 20), padx=(0, 25))
duree.current(0)

debut_journee = ttkb.Button(ajout_frame, text="Débuter la journée", bootstyle="info", state=ttkb.DISABLED,
                            command=debuter_journee)
debut_journee.grid(row=7, column=0, padx=(5, 0), pady=(60, 30), sticky="s")

ajouter_tache = ttkb.Button(ajout_frame, text="Ajouter", bootstyle="success", command=add_task)
ajouter_tache.grid(row=7, column=3, padx=(0, 5), pady=(60, 30), sticky="e")

"""" #################################### visualisation de taches #################################### """
# tire
ttkb.Label(visualisation_tache, text="Visualisation de tâches", bootstyle="success inverse",
           font=("poppins", 15)).pack(fill="x", padx=5, pady=(5, 10))
# creation frame visualisation
visualisation = ScrolledFrame(visualisation_tache, height=240, autohide=True)
visualisation.pack(fill="x", padx=5, pady=(5, 10), ipadx=5, ipady=5)

ttkb.Separator(visualisation_tache, bootstyle="success").pack(fill="x", pady=10, padx=5)

visualisation_time = ttkb.Frame(visualisation_tache, height=110)
visualisation_time.pack(fill="x", padx=5, pady=(5, 10))

# configuration visualisation_time
visualisation_time.grid_columnconfigure((0, 1, 2), weight=1)

# debut de taches
debut_tache = ttkb.Button(visualisation_time, text="Debut", bootstyle="success", state=ttkb.DISABLED,
                          command=debuter_tache)
debut_tache.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

# comptage de temps
temps_tache = ttkb.Label(visualisation_time, text="00h 00m 00s", bootstyle="light inverse", justify="center",
                         font=("poppins", 12, "bold"))
temps_tache.grid(row=0, column=1, sticky="nswe", )

# fin de taches
fin_tache = ttkb.Button(visualisation_time, text="Fin", bootstyle="success", state=ttkb.DISABLED)
fin_tache.grid(row=0, column=2, sticky="nsew", padx=(10, 0))

# arret journee
fin_journee = ttkb.Button(visualisation_time, text="Fermer", bootstyle="danger", state=ttkb.DISABLED)
fin_journee.grid(row=1, column=2, sticky="nsew", pady=10, padx=(10, 0))

# traitement visualisation tache
visualisation.grid_columnconfigure((0, 1, 2), weight=1)

# selection id
ttkb.Label(visualisation, text="Numero: ", font=("poppins", 13)).grid(row=0, column=0, sticky="nsew", pady=(0, 10))
selection_numero_tache = ttkb.Combobox(visualisation, font=("poppins", 12), width=30, state=ttkb.DISABLED)
selection_numero_tache.grid(row=0, column=1, columnspan=2, sticky="nsew", pady=(0, 10))

# titre
ttkb.Label(visualisation, text="Durée", font=("poppins", 12, "bold")).grid(row=1, column=0, sticky="nsew")
ttkb.Label(visualisation, text="Tâches", font=("poppins", 12, "bold")).grid(row=1, column=1, columnspan=2,
                                                                            sticky="nsew")

# message avant l'ajout des taches
visualisation_texte = ttkb.Label(visualisation, text="Pas de tache...", font=("poppins", 20),
                                 bootstyle="danger")
visualisation_texte.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")

"""" #################################### bilan #################################### """
# tire
titre_bilan = ttkb.Label(bilan, text="Rapport journalier", bootstyle="success inverse",
           font=("poppins", 15))
titre_bilan.pack(fill="x", pady=5, padx=5)

ttkb.Button(bilan, text="Afficher le bilan d'un ancien jour",
            bootstyle="info outline", command=ancien_bilan).pack(fill="x", pady=(20, 5), padx=5)

bilan_frame = ScrolledFrame(bilan, height=410, autohide=True)
bilan_frame.pack(fill=ttkb.BOTH, pady=10, ipady=5, ipadx=10)

# configuration
bilan_frame.grid_columnconfigure((0, 1, 2), weight=1)

# message avant l'ajout des taches
bilan_texte = ttkb.Label(bilan_frame, text="Finissez au moins une tache!"
                                           "\npuis vous aurez vos rapports", font=("poppins", 20),
                         bootstyle="danger")
bilan_texte.grid(row=1, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
"""" #################################### indentification #################################### """

# configuration
identification.grid_columnconfigure((0, 1, 2, 3), weight=1)

# titre
ttkb.Label(identification, text="Identification", bootstyle="success inverse",
           font=("poppins", 15)).grid(row=0, columnspan=4, column=0, padx=5,
                                      pady=(5, 35), sticky="nsew")

# message
ttkb.Label(identification, text="Pas de compte?", font=("poppins", 8)).grid(row=1, column=0, sticky="e")
inscription_btn = ttkb.Button(identification, text="inscrivez-vous!", bootstyle="info-link", width=0,
                              command=show_inscription)
inscription_btn.grid(row=1, column=1, sticky="w")

# adresse mail
ttkb.Label(identification, text="Adresse mail: ", font=("poppins", 13)).grid(row=2, column=0, pady=(10, 20),
                                                                             padx=(20, 0), sticky="e")
mail_connexion = ttkb.Entry(identification, font=("poppins", 10))
mail_connexion.grid(row=2, columnspan=3, column=1, pady=(10, 20), padx=(0, 20), sticky="nsew")

# mot de passe
ttkb.Label(identification, text="Mot de passe: ", font=("poppins", 13)).grid(row=3, column=0, pady=(10, 20),
                                                                             padx=(20, 0), sticky="e")
mdp_connexion = ttkb.Entry(identification, font=("poppins", 10), show="*")
mdp_connexion.grid(row=3, columnspan=3, column=1, pady=(10, 20), padx=(0, 20), sticky="nsew")

# message
ttkb.Label(identification, text="Mot de passe", font=("poppins", 8)).grid(row=4, column=0, sticky="e")
oublie_mdp = ttkb.Button(identification, text="oublie?", bootstyle="info-link", width=0,
                         command=mdp_oublie)
oublie_mdp.grid(row=4, column=1, sticky="w")

# btn_valid
btn_connexion = ttkb.Button(identification, text="Identification", bootstyle="success outline",
                            command=connexion)
btn_connexion.grid(row=4, column=3, pady=(10, 0), padx=20, sticky="e")

"""" #################################### parametre #################################### """

parametre.grid_columnconfigure((0, 1, 2, 3), weight=1)

# titre
ttkb.Label(parametre, text="Paramétre", bootstyle="success inverse",
           font=("poppins", 15)).grid(row=0, columnspan=4, column=0, padx=5,
                                      pady=(5, 35), sticky="nsew")
# changement theme
ttkb.Label(parametre, text="Thème: ", font=('poppins', 13)).grid(row=1, column=0, sticky="e", pady=20, padx=(20, 0))
theme = ttkb.Combobox(parametre, values=['Superhero', 'Vapor', 'Morph', 'Darkly', 'Solar', 'Cyborg',
                                         'Pulse', 'Yeti', 'Journal', 'Simplex', 'Cosmo', 'Litera', 'Lumen'],
                      font=('poppins', 10))
theme.grid(row=1, column=1, columnspan=3, sticky="nsew", pady=20, padx=(5, 20))
theme.current(0)

# changement notification
ttkb.Label(parametre, text="Type notification: ", font=('poppins', 13)).grid(row=2, column=0, sticky="e", pady=20,
                                                                             padx=(20, 0))
notification = ttkb.Combobox(parametre, values=['Texte', 'Audio'], font=('poppins', 10))
notification.grid(row=2, column=1, columnspan=3, sticky="nsew", pady=20, padx=(5, 20))
notification.current(0)

# btn_valid
ttkb.Button(parametre, text="Appliquer", bootstyle="success outline",
            command=change_parametre).grid(row=3, column=3, pady=(10, 0), padx=20, sticky="e")

ttkb.Label(parametre, image=image_label, text="GESTICADO", bootstyle="success", font=("poppins", 12, "bold"),
           compound="bottom").grid(columnspan=4, column=0)

app.mainloop()
