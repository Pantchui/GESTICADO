"""" #################################### importation de bibliotheque #################################### """
import random
import math
import time

import pyttsx3
import datetime

import ttkbootstrap as ttkb
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import Messagebox

import mysql.connector
from PIL import Image, ImageTk

"""" #################################### definitions de fonctions #################################### """


# fermer
def fermer():
    app.destroy()


# fin journee
def fermer_journee():
    # enregistrez les donnees
    try:
        bd = mysql.connector.connect(
            host="localhost",
            password="",
            user="root",
            database="gestion_temps_taches",
        )

        data = bd.cursor()

        # recuperation du numero
        requet = "SELECT numero FROM utilisateur WHERE mail = %s"
        data.execute(requet, (mail_connexion.get(),))
        numero = data.fetchall()[0][0]

        # update le temps effectue
        requet = "UPDATE taches SET fin_journee = %s WHERE numero = %s AND jour = %s"
        data.execute(requet, ("1", numero, jour_actuel()))

        bd.commit()

        fin_tache.config(state=ttkb.DISABLED)
        fin_journee.config(state=ttkb.DISABLED)
        debut_tache.config(state=ttkb.DISABLED)
        show_bilan()
        actions.select(2)

    except:
        erreur_bdd()


# gestion du bilan
def show_bilan():
    # traitement de dnnee
    bd = mysql.connector.connect(
        host="localhost",
        password="",
        user="root",
        database="gestion_temps_taches",
    )

    data = bd.cursor()

    # recuperation du numero
    requet = "SELECT numero FROM utilisateur WHERE mail = %s"
    data.execute(requet, (mail_connexion.get(),))
    numero = data.fetchall()[0][0]

    # nombre de tache
    requet = "SELECT * FROM taches WHERE numero = %s AND jour = %s"
    data.execute(requet, (numero, jour_actuel()))
    try:
        # recuperation des informations
        toutes_les_informations = data.fetchall()

        # nbr de taches final
        nbr_taches, nbr_taches_effectuees, taches_avt_delai, \
            taches_apr_delai, taches_pdt_delai = 0, 0, 0, 0, 0
        for i in range(len(toutes_les_informations)):
            nbr_taches += 1
            if toutes_les_informations[i][2] > 0:
                nbr_taches_effectuees += 1

                # verification par rapport au delai
                if toutes_les_informations[i][2] < toutes_les_informations[i][1]:
                    taches_avt_delai += 1
                if toutes_les_informations[i][2] > toutes_les_informations[i][1]:
                    taches_apr_delai += 1
                if toutes_les_informations[i][2] == toutes_les_informations[i][1]:
                    taches_pdt_delai += 1

        # temps total
        temps_total_tache, temps_total_tache_effectue = 0, 0
        for tt_information in toutes_les_informations:
            temps_total_tache += int(tt_information[1])
            temps_total_tache_effectue += int(tt_information[2])

        # temps deborde
        val = temps_total_tache_effectue - temps_total_tache
        temps_deborde = val if val > 0 else 0

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
        if round((nbr_taches_effectuees / nbr_taches) * 100) > 50:
            ttkb.Meter(bilan_frame, bootstyle="success", metertype="semi", subtextstyle="B.TLabel",
                       textright=f"/{nbr_taches} tâches", metersize=130, interactive=False,
                       textfont=("poppins", 12, "bold"),
                       subtext="complétées", subtextfont=("poppins", 7), amounttotal=nbr_taches, stripethickness=24,
                       amountused=nbr_taches_effectuees).grid(row=2, column=0, pady=20, padx=(0, 5))
        else:
            ttkb.Meter(bilan_frame, bootstyle="danger", metertype="semi", subtextstyle="B.TLabel",
                       textright=f"/{nbr_taches} tâches", metersize=130, interactive=False,
                       textfont=("poppins", 12, "bold"),
                       subtext="complétées", subtextfont=("poppins", 7), amounttotal=nbr_taches, stripethickness=24,
                       amountused=nbr_taches_effectuees).grid(row=2, column=0, pady=20, padx=(0, 5))

        # temps
        if temps_total_tache > temps_total_tache_effectue:
            ttkb.Meter(bilan_frame, bootstyle="success", metertype="semi", subtextstyle="B.TLabel",
                       textright=f"/{temps_total_tache}min", metersize=130, interactive=False,
                       textfont=("poppins", 12, "bold"), stripethickness=24,
                       subtext="consommées", subtextfont=("poppins", 7), amounttotal=temps_total_tache,
                       amountused=temps_total_tache_effectue).grid(row=2, column=1, pady=20, padx=5)
        else:
            ttkb.Meter(bilan_frame, bootstyle="danger", metertype="semi", subtextstyle="B.TLabel",
                       textright=f"/{temps_total_tache}min", metersize=130, interactive=False,
                       textfont=("poppins", 12, "bold"),
                       subtext="consommées", subtextfont=("poppins", 7), amounttotal=temps_total_tache,
                       stripethickness=24,
                       amountused=temps_total_tache_effectue).grid(row=2, column=1, pady=20, padx=5)

        # debordement
        if temps_deborde < 60:
            ttkb.Meter(bilan_frame, bootstyle="success", metertype="semi", subtextstyle="B.TLabel",
                       textright="min/160", metersize=130, interactive=False, textfont=("poppins", 12, "bold"),
                       subtext="ajoutés", amountused=temps_deborde, subtextfont=("poppins", 7), amounttotal=160,
                       stripethickness=24).grid(row=2, column=2, pady=20, padx=(5, 0))
        else:
            ttkb.Meter(bilan_frame, bootstyle="danger", metertype="semi", subtextstyle="B.TLabel",
                       textright="min/160", metersize=130, interactive=False, textfont=("poppins", 12, "bold"),
                       subtext="ajoutés", amountused=temps_deborde, subtextfont=("poppins", 7), amounttotal=160,
                       stripethickness=24).grid(row=2, column=2, pady=20, padx=(5, 0))

        # rapport par taches
        ttkb.Label(bilan_frame, text="Rapport par tâche", font=("poppins", 13)).grid(row=3, pady=20, column=0,
                                                                                     columnspan=3,
                                                                                     sticky="w")

        style = ttkb.Style()
        style.configure("B.TLabel", font=("poppins", 5))

        # meter
        r, c = 4, 0
        for toutes_les_information in toutes_les_informations:
            if toutes_les_information[2] > toutes_les_information[1]:
                ttkb.Meter(bilan_frame, bootstyle="danger", subtextstyle="B.TLabel",
                           textright=f"min/{toutes_les_information[1]}", metersize=130,
                           textfont=("poppins", 12, "bold"),
                           subtext=f"tâche {toutes_les_information[4]}", subtextfont=("poppins", 7),
                           amounttotal=toutes_les_information[1],
                           amountused=toutes_les_information[2]).grid(row=r, column=c, pady=20, padx=5)
            else:
                ttkb.Meter(bilan_frame, bootstyle="success", subtextstyle="B.TLabel",
                           textright=f"min/{toutes_les_information[1]}", metersize=130,
                           textfont=("poppins", 12, "bold"),
                           subtext=f"tâche {toutes_les_information[4]}", subtextfont=("poppins", 7),
                           amounttotal=toutes_les_information[1],
                           amountused=toutes_les_information[2]).grid(row=r, column=c, pady=20, padx=5)
            c += 1
            if c == 3:
                r += 1
                c = 0

        # rapport debordement de duree
        ttkb.Label(bilan_frame, text="Rapport débordement de durée", font=("poppins", 13)).grid(row=r + 1,
                                                                                                pady=(20, 10),
                                                                                                column=0,
                                                                                                columnspan=3,
                                                                                                sticky="w")
        r = r + 2
        exist = False
        for toutes_les_information in toutes_les_informations:
            if toutes_les_information[2] > toutes_les_information[1]:
                ttkb.Label(bilan_frame,
                           text=f"{toutes_les_information[4]}. {toutes_les_information[0]}: {toutes_les_information[2] - toutes_les_information[1]} minutes",
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
                   text=f"Accomplissement des tâches: {round((nbr_taches_effectuees / nbr_taches) * 100)}%",
                   font=("poppins", 12),
                   bootstyle="info").grid(row=r + 5, column=0, columnspan=3, sticky="w", padx=(15, 0))
        ttkb.Label(bilan_frame,
                   text=f"Utilisation du temps: {round((temps_total_tache_effectue / temps_total_tache) * 100)}%",
                   font=("poppins", 12),
                   bootstyle="info").grid(row=r + 6, column=0, columnspan=3, sticky="w", padx=(15, 0))
        ttkb.Label(bilan_frame,
                   text=f"Temps ajoutée: {round((temps_deborde / temps_total_tache) * 100)}% du temps initial",
                   font=("poppins", 12),
                   bootstyle="info").grid(row=r + 7, column=0, columnspan=3, sticky="w", padx=(15, 0))
        ttkb.Label(bilan_frame,
                   text=f"Tâches non terminées: {round(100 - ((nbr_taches_effectuees / nbr_taches) * 100))}%",
                   font=("poppins", 12),
                   bootstyle="info").grid(row=r + 8, column=0, columnspan=3, sticky="w", padx=(15, 0))

        ttkb.Separator(bilan_frame, bootstyle="info").grid(row=r + 9, column=0, columnspan=3, sticky="nsew",
                                                           padx=(15, 0), pady=20)

        ttkb.Label(bilan_frame,
                   text=f"Tâches terminées avant le delai: {round((taches_avt_delai / nbr_taches_effectuees) * 100)}% ({taches_avt_delai} tâche(s)/{nbr_taches_effectuees})",
                   font=("poppins", 12),
                   bootstyle="info").grid(row=r + 10, column=0, columnspan=3, sticky="w", padx=(15, 0))
        ttkb.Label(bilan_frame,
                   text=f"Tâches terminées dans le delai: {round((taches_pdt_delai / nbr_taches_effectuees) * 100)}% ({taches_pdt_delai} tâche(s)/{nbr_taches_effectuees})",
                   font=("poppins", 12),
                   bootstyle="info").grid(row=r + 11, column=0, columnspan=3, sticky="w", padx=(15, 0))
        ttkb.Label(bilan_frame,
                   text=f"Tâches terminées après le delai: {round((taches_apr_delai / nbr_taches_effectuees) * 100)}% ({taches_apr_delai} tâche(s)/{nbr_taches_effectuees})",
                   font=("poppins", 12),
                   bootstyle="info").grid(row=r + 12, column=0, columnspan=3, sticky="w", padx=(15, 0))

        ttkb.Button(bilan_frame, text="Fermer", bootstyle="outline danger",
                    command=fermer).grid(row=r + 13, column=2, pady=(30, 10))

    except:
        erreur_bdd()
        bilan_texte.config(text="Nous avons rencontrez une \nerreur. "
                                "Merci de reessayer!")


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
    try:
        bd = mysql.connector.connect(
            host="localhost",
            password="",
            user="root",
            database="gestion_temps_taches",
        )

        data = bd.cursor()

        # recuperation du numero
        requet = "SELECT numero FROM utilisateur WHERE mail = %s"
        data.execute(requet, (mail_connexion.get(),))
        numero = data.fetchall()[0][0]

        # update le temps effectue
        requet = "UPDATE taches SET temps_effectue = %s WHERE numero = %s AND jour = %s AND numero_tache = %s"
        data.execute(requet, (temps_ecoule_minute, numero, jour_actuel(), int(num_actuel)))

        bd.commit()

        label_tache = label_taches[int(num_actuel) - 1]
        label_tache[0].config(bootstyle="success")
        label_tache[1].config(bootstyle="success")
        fin_tache.config(state=ttkb.DISABLED)
        fin_journee.config(state=ttkb.ACTIVE, command=fermer_journee)
        show_bilan()

        if len(nums) != 0:
            debut_tache.config(state=ttkb.ACTIVE)

    except:
        erreur_bdd()


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

    # activation et descativation
    fin_journee.config(state=ttkb.DISABLED)
    debut_tache.config(state=ttkb.DISABLED)
    fin_tache.config(state=ttkb.ACTIVE, command=lambda: finission_tache(nums, num_actuel))

    # chronometre
    tache_encours = True
    chronometre()


# debut de journee
def debuter_journee():
    # desactivation  des champs
    tache.config(state=ttkb.DISABLED)
    ajouter_tache.config(state=ttkb.DISABLED)
    debut_journee.config(state=ttkb.DISABLED)

    # activations des champs
    debut_tache.config(state=ttkb.ACTIVE)
    fin_journee.config(state=ttkb.ACTIVE, command=fermer_journee)

    # connexion bdd
    bd = mysql.connector.connect(
        host="localhost",
        password="",
        user="root",
        database="gestion_temps_taches"
    )

    try:
        # recuperation du numero
        data = bd.cursor()
        requet = "SELECT numero FROM utilisateur WHERE mail = %s"
        data.execute(requet, (mail_connexion.get(),))
        numero = data.fetchall()[0][0]

        # recuperation des numero de taches
        requet = "SELECT numero_tache FROM taches WHERE numero = %s AND jour = %s"
        data.execute(requet, (numero, jour_actuel()))
        results = data.fetchall()

        nums = []
        for result in results:
            nums.append(result[0])
        nums = sorted(nums)
        selection_numero_tache.config(values=nums, state=ttkb.ACTIVE)
        selection_numero_tache.current(0)
        actions.hide(0)
        actions.select(1)

    except:
        erreur_bdd()


# remplissage
def remplissage():
    # verification si la taches exite

    debut_journee.config(state=ttkb.ACTIVE)

    visualisation_texte.grid_forget()

    # connexion base de donnee
    bd = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestion_temps_taches"
    )
    try:
        data = bd.cursor()
        requet = "SELECT numero FROM utilisateur WHERE mail = %s"
        data.execute(requet, (mail_connexion.get(),))
        numero = data.fetchall()[0][0]

        # selection tache
        requet = "SELECT numero_tache, nom_tache, duree FROM taches WHERE numero = %s AND jour = %s"
        data.execute(requet, (numero, jour_actuel()))
        results = data.fetchall()

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



    except:
        erreur_bdd()


# jour actuel
def jour_actuel():
    jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    mois = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin",
            "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]

    jour = jours[datetime.datetime.now().weekday()] + " " + str(datetime.datetime.now().day) + " " \
           + mois[datetime.datetime.now().month - 1] + " " + str(datetime.datetime.now().year)
    return jour


# erreur bdd
def erreur_bdd():
    global type_notification_audio
    if type_notification_audio:
        parler("Une erreur s'est produite merci de réessayer."
               "Si le problème persite bien vouloir nous contactez!")
    else:
        Messagebox.show_info(message="Une erreur s'est produite merci de réessayer. \n "
                                     "Si le problème persite bien vouloir nous contactez!",
                             title="Connexion", bootstyle="success")


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
    global image_label

    # inscription
    def inscription():
        global type_notification_audio, user_connect
        # verification des champs
        if not (pseudo.get() and mail.get() and mdp1.get() and mdp2.get()) == "":

            if type_notification_audio:
                parler("Inscription en cours")

            # validation du mail
            if '@' in mail.get() and mail.get().endswith(".com"):

                # verification des mots de passe
                if mdp1.get() == mdp2.get():

                    # numero
                    lettre = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                              'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

                    numero = str(random.randint(100, 999)) + lettre[random.randint(0, 25)] + \
                             lettre[random.randint(0, 25)].lower() + str(random.randint(10, 99))

                    # base de donnee
                    bd = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="gestion_temps_taches"
                    )
                    try:
                        datas = bd.cursor()

                        # requet
                        requet = "SELECT * FROM utilisateur WHERE numero = %s AND mail = %s"
                        datas.execute(requet, (numero, mail.get()))

                        results = datas.fetchall()
                        if not len(results) == 0:
                            if type_notification_audio:
                                parler("Le numéro et l'adresse mail existe déjà!")
                            else:
                                Messagebox.show_warning(message="Le numéro et l'adresse mail existe déjà!",
                                                        title="Attention",
                                                        bootstyle="success")
                        else:

                            # requet d'insertion'
                            requet = "INSERT INTO utilisateur(numero, pseudo, mail, mdp) VALUES(%s, %s, %s, %s)"
                            values = (numero, pseudo.get(), mail.get(), mdp2.get())

                            # execution de la requette
                            datas.execute(requet, values)
                            bd.commit()

                            user_connect = True

                            # configuration des champs
                            mail_connexion.insert(0, mail.get())
                            mdp_connexion.insert(0, mdp2.get())

                            btn_connexion.config(state=ttkb.DISABLED)
                            mail_connexion.config(state=ttkb.DISABLED)
                            mdp_connexion.config(state=ttkb.DISABLED)
                            inscription_btn.config(state=ttkb.DISABLED)

                            # message d'information
                            if type_notification_audio:
                                parler("Inscription réussie! Nous vous remercions pour votre confiance.")
                            else:
                                Messagebox.show_warning(message="Inscription réussie!\n"
                                                                " Nous vous remercions pour votre confiance.",
                                                        title="Attention",
                                                        bootstyle="success")
                            app_inscription.destroy()

                    except:
                        erreur_bdd()
                        app_inscription.destroy()
                else:
                    if type_notification_audio:
                        parler("Les mots de passe ne correspondent pas!")
                    else:
                        Messagebox.show_error(message="Les mots de passe ne correspondent pas!", title="Erreur",
                                              bootstyle="succcess")
            else:
                if type_notification_audio:
                    parler("Adresse mail incorrecte!")
                else:
                    Messagebox.show_error(message="Adresse mail incorrecte!", title="Erreur",
                                          bootstyle="succcess")
        else:
            if type_notification_audio:
                parler("Veuillez remplir tout les champs!")
            else:
                Messagebox.show_warning(message="Veuillez remplir tout les champs!", title="Attention",
                                        bootstyle="succcess")

    app_inscription = ttkb.Toplevel()
    app_inscription.title("GESTICADO - INSCRIPTION")
    app_inscription.geometry("700x500")
    app_inscription.grid_columnconfigure((0, 1, 2, 3), weight=1)
    # app_inscription.geometry("500x500")

    # texte principale
    ttkb.Label(app_inscription, text="Inscription", image=image_label, compound="left", font=("poppins", 30, "bold"),
               bootstyle="success").grid(row=0, columnspan=4, column=0, pady=20, padx=25)

    # pseudo
    ttkb.Label(app_inscription, text="Pseudo: ", font=("poppins", 13)).grid(row=1, column=0, pady=(10, 20),
                                                                            padx=(20, 0), sticky="ne")
    pseudo = ttkb.Entry(app_inscription, font=("poppins", 10))
    pseudo.grid(row=1, columnspan=3, column=1, pady=(10, 20), padx=(0, 20), sticky="nsew")

    # adresse mail
    ttkb.Label(app_inscription, text="Adresse mail: ", font=("poppins", 13)).grid(row=2, column=0, pady=(10, 20),
                                                                                  padx=(20, 0), sticky="e")
    mail = ttkb.Entry(app_inscription, font=("poppins", 10))
    mail.grid(row=2, columnspan=3, column=1, pady=(10, 20), padx=(0, 20), sticky="nsew")

    # mot de passe
    ttkb.Label(app_inscription, text="Mot de passe: ", font=("poppins", 13)).grid(row=3, column=0, pady=(10, 20),
                                                                                  padx=(20, 0), sticky="e")
    mdp1 = ttkb.Entry(app_inscription, font=("poppins", 10), show="*")
    mdp1.grid(row=3, columnspan=3, column=1, pady=(10, 20), padx=(0, 20), sticky="nsew")

    # confirmation mot de passe
    ttkb.Label(app_inscription, text="Confirmation: ", font=("poppins", 13)).grid(row=4, column=0, pady=(10, 20),
                                                                                  padx=(20, 0), sticky="e")
    mdp2 = ttkb.Entry(app_inscription, font=("poppins", 10), show="*")
    mdp2.grid(row=4, columnspan=3, column=1, pady=(10, 20), padx=(0, 20), sticky="nsew")

    # btn_valid
    btn_inscription = ttkb.Button(app_inscription, text="Inscription", bootstyle="success outline",
                                  command=inscription)
    btn_inscription.grid(row=6, column=3, pady=20, padx=20, sticky="e")


# connexion
def connexion():
    global user_connect, type_notification_audio
    # verification champ vide!
    if not (mail_connexion.get() and mdp_connexion.get()) == "":

        if type_notification_audio:
            parler("Identification en cours")

        # verification mail
        if '@' in mail_connexion.get() and mail_connexion.get().endswith(".com"):

            # connexion bd
            bd = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="gestion_temps_taches"
            )
            try:
                data = bd.cursor()

                # recuperation information
                requet = "SELECT * FROM utilisateur WHERE mail=%s AND mdp=%s"
                data.execute(requet, (mail_connexion.get(), mdp_connexion.get()))

                # fetch information
                results = data.fetchall()

                if len(results) != 0:
                    # desactivation des champs
                    btn_connexion.configure(state=ttkb.DISABLED)
                    mail_connexion.configure(state=ttkb.DISABLED)
                    mdp_connexion.configure(state=ttkb.DISABLED)
                    inscription_btn.configure(state=ttkb.DISABLED)

                    # variable de connexion
                    user_connect = True
                    existance()

                    global tache_exits

                    if tache_exits:
                        remplissage()

                    # message
                    if type_notification_audio:
                        parler("Connexion réuissie! Vous pouvez maintenant ajouter vos tâches!")
                    else:
                        Messagebox.show_info(message="Connexion réuissie!\n Vous pouvez maintenant ajouter vos tâches!",
                                             title="Connexion", bootstyle="success")

                        # recuperation du numero
                        requet = "SELECT numero FROM utilisateur WHERE mail = %s"
                        data.execute(requet, (mail_connexion.get(),))
                        numero = data.fetchall()[0][0]

                        # recherche fin de journee
                        # recuperation du numero
                        requet = "SELECT fin_journee FROM taches WHERE numero = %s AND jour = %s"
                        data.execute(requet, (numero, jour_actuel()))
                        fins = data.fetchall()
                        # print(fins, len(fins), fins[0], len(fins[0]))

                        if len(fins) > 0:
                            if fins[0][0] == 1:
                                ajouter_tache.config(state=ttkb.DISABLED)
                                if type_notification_audio:
                                    parler("Vous avez déjâ fermé cette journée, vous pouvez seulement, visualiser le "
                                           "rapport de la journée!")
                                else:
                                    Messagebox.show_info(
                                        message="Vous avez déjâ fermé cette journée, vous pouvez seulement, "
                                                "visualiser le rapport de la journée!",
                                        title="Connexion", bootstyle="success")
                                show_bilan()
                                actions.hide(0)
                                actions.select(2)
                else:
                    if type_notification_audio:
                        parler("Echec de connexion! Verifiez vos données!")
                    else:
                        Messagebox.show_warning(message="Echec de connexion! Verifiez vos données!", title="Erreur",
                                                bootstyle="success")
            except:
                erreur_bdd()
        else:
            if type_notification_audio:
                parler("L'adresse mail n'est pas correct!")
            else:
                Messagebox.show_warning(message="L'adresse mail n'est pas correct!", title="Erreur",
                                        bootstyle="success")
    else:
        if type_notification_audio:
            parler("Complétez tous les champs!")
        else:
            Messagebox.show_warning(message="Complétez tous les champs!", title="Attention", bootstyle="success")


# choix duree
def change_duree(e):
    if unite.get() == "Heures":
        duree.config(values=[1, 2, 3, 4, 5, 6])
    else:
        duree.config(values=[2, 5, 10, 15, 30, 45])
    duree.current(0)


# ajout de taches
def add_task():
    global type_notification_audio, user_connect

    # verification de la connexion
    if user_connect:

        # verification du champ
        if not tache.get() == "":

            # verification de la taille
            if len(tache.get()) < 100:

                # connexion bdd
                bd = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="gestion_temps_taches"
                )
                try:
                    datas = bd.cursor()

                    # selection de numero
                    requet = "SELECT numero FROM utilisateur WHERE mail = %s AND mdp = %s"
                    datas.execute(requet, (mail_connexion.get(), mdp_connexion.get()))
                    numero = datas.fetchall()[0][0]

                    # verification du nom de la tache
                    requet = "SELECT * FROM taches WHERE nom_tache = %s AND jour = %s AND numero = %s"
                    jour = jour_actuel()
                    datas.execute(requet, (tache.get(), jour, numero))

                    if len(datas.fetchall()) == 0:

                        # traitement duree
                        if unite.get() == "Heures":
                            duree_minute = int(duree.get()) * 60
                        else:
                            duree_minute = int(duree.get())

                        # insertion des donnees
                        requet = "INSERT INTO taches(nom_tache, duree, numero, numero_tache, jour)" \
                                 "VALUES(%s, %s, %s, %s, %s)"
                        datas.execute(requet,
                                      (tache.get(), duree_minute, numero, int(numero_tache.get()), jour_actuel()))
                        bd.commit()

                        # detection position
                        plein_tache = False
                        global tableau_numero_tache
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

                        # activation debut de journee
                        debut_journee.config(state=ttkb.ACTIVE)
                        remplissage()

                        # notification
                        if type_notification_audio:
                            parler("La tâche, a bien été ajoutée")
                        else:
                            Messagebox.show_info(title="Ajout de tache", message="La tâche, a bien été ajoutée",
                                                 bootstyle="success")
                        # si on a atteint la limite
                        if plein_tache:
                            # notification
                            if type_notification_audio:
                                parler("Vous avez déjà atteint la limite de neuf tâches, vous ne pouvez ajouter de "
                                       "tâche!")
                            else:
                                Messagebox.show_info(title="Ajout de tache", bootstyle="success",
                                                     message="Vous avez déjà atteint la limite de neuf tâches\n "
                                                             "Vous ne pouvez ajouter de tâche!")
                        return 0
                    else:
                        if type_notification_audio:
                            parler("Le nom de la tâche existe déjà")
                        else:
                            Messagebox.show_info(title="Ajout tâches",
                                                 message="Le nom de la tâche existe déjà!",
                                                 bootstyle="success")
                except:
                    erreur_bdd()
            else:
                if type_notification_audio:
                    parler("Le nom de la tâche est trop long")
                else:
                    Messagebox.show_info(title="Ajout tâches",
                                         message="Le nom de la tâche est trop long!",
                                         bootstyle="success")
        else:
            if type_notification_audio:
                parler("Le nom de la tâche n'a pas été defini")
            else:
                Messagebox.show_info(title="Ajout tâches",
                                     message="Le nom de la tâche n'a pas été defini!",
                                     bootstyle="success")
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
    global tache_exits, tableau_numero_tache
    bdd = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestion_temps_taches"
    )
    datas = bdd.cursor()

    # selection de numero
    requet = "SELECT numero FROM utilisateur WHERE mail = %s AND mdp = %s"
    datas.execute(requet, (mail_connexion.get(), mdp_connexion.get()))
    numero = datas.fetchall()[0][0]

    datas.execute("SELECT numero_tache FROM taches WHERE jour = %s AND fin_journee = %s AND numero = %s",
                  (jour_actuel(), "0", numero))
    resultats = datas.fetchall()

    if len(resultats) > 0:
        tache_exits = True

        for resultat in resultats:
            tableau_numero_tache.remove(resultat[0])

        numero_tache.config(values=tableau_numero_tache)
        numero_tache.current(0)


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
ttkb.Label(bilan, text="Rapport journalier", bootstyle="success inverse",
           font=("poppins", 15)).pack(fill="x", pady=5, padx=5)

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

# adresse mail
ttkb.Label(identification, text="Adresse mail: ", font=("poppins", 13)).grid(row=1, column=0, pady=(10, 20),
                                                                             padx=(20, 0), sticky="e")
mail_connexion = ttkb.Entry(identification, font=("poppins", 10))
mail_connexion.grid(row=1, columnspan=3, column=1, pady=(10, 20), padx=(0, 20), sticky="nsew")

# mot de passe
ttkb.Label(identification, text="Mot de passe: ", font=("poppins", 13)).grid(row=2, column=0, pady=(10, 20),
                                                                             padx=(20, 0), sticky="e")
mdp_connexion = ttkb.Entry(identification, font=("poppins", 10), show="*")
mdp_connexion.grid(row=2, columnspan=3, column=1, pady=(10, 20), padx=(0, 20), sticky="nsew")

# message
ttkb.Label(identification, text="Pas de compte?", font=("poppins", 8)).grid(row=3, column=0, sticky="e")
inscription_btn = ttkb.Button(identification, text="inscrivez-vous!", bootstyle="info-link", width=0,
                              command=show_inscription)
inscription_btn.grid(row=3, column=1, sticky="w")

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
