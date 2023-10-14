# # import ttkbootstrap as ttkb
# # from timeit import default_timer
# #
# #
# # def update():
# #     now = default_timer() - start
# #     minutes, secondes = divmod(now, 60)
# #     heures, minutes = divmod(minutes, 60)
# #     str_time = "%d:%02d%ds:%02d" % (heures, minutes, secondes)
# #     time_label.config(text=str_time)
# #     time_label.after(1000, update())
# #
# #
# # main = ttkb.Window(themename="superhero")
# # time_label = ttkb.Label(main, font=("poppins", 30), bootstyle="danger")
# # time_label.pack(pady=30, padx=30)
# #
# # start = default_timer()
# # update()
# #
# # main.mainloop()
# # import time
# #
# #
# # def chronometre():
# #     temps_debut = time.time()  # Enregistre le temps de début
# #
# #     while True:
# #         temps_actuel = time.time()
# #         temps_ecoule = temps_actuel - temps_debut
# #
# #         heures = int(temps_ecoule / 3600)
# #         minutes = int((temps_ecoule % 3600) / 60)
# #         secondes = int(temps_ecoule % 60)
# #
# #         # Affiche le temps écoulé au format HH:MM:SS
# #         print(f"{heures:02d}:{minutes:02d}:{secondes:02d}", end="\r", flush=True)
# #
# #         time.sleep(1)  # Attend 1 seconde
# #
#
# # chronometre()
#
# import tkinter as tk
#
#
# class Chronometre:
#     def __init__(self, fenetre):
#         self.fenetre = fenetre
#         self.temps_ecoule = 0
#         self.en_cours = False
#
#         self.label_temps = tk.Label(fenetre, text="00:00:00", font=("Arial", 24))
#         self.label_temps.pack(pady=20)
#
#         self.bouton_demarrer = tk.Button(fenetre, text="Démarrer", command=self.demarrer)
#         self.bouton_demarrer.pack(pady=10)
#
#         self.bouton_arreter = tk.Button(fenetre, text="Arrêter", command=self.arreter)
#         self.bouton_arreter.pack(pady=10)
#
#         self.bouton_reinitialiser = tk.Button(fenetre, text="Réinitialiser", command=self.reinitialiser)
#         self.bouton_reinitialiser.pack(pady=10)
#
#         self.mise_a_jour_chronometre()
#
#     def mise_a_jour_chronometre(self):
#         heures = int(self.temps_ecoule / 3600)
#         minutes = int((self.temps_ecoule % 3600) / 60)
#         secondes = int(self.temps_ecoule % 60)
#
#         # Affiche le temps écoulé au format HH:MM:SS
#         temps_formatte = f"{heures:02d}:{minutes:02d}:{secondes:02d}"
#         self.label_temps.config(text=temps_formatte)
#
#         if self.en_cours:
#             self.temps_ecoule += 1
#
#         self.fenetre.after(1000, self.mise_a_jour_chronometre)
#
#     def demarrer(self):
#         self.en_cours = True
#
#     def arreter(self):
#         self.en_cours = False
#
#     def reinitialiser(self):
#         self.temps_ecoule = 0
#
#
# fenetre = tk.Tk()
# fenetre.title("Chronomètre")
# chronometre = Chronometre(fenetre)
# fenetre.mainloop()
import time

import ttkbootstrap as ttkb
from PIL import Image, ImageTk


def increment():
    progress.step(1)
    if int(progress.variable.get())+1 == 100:
        import main
    progress.after(100, increment)


def commencer():
    progress.grid(columnspan=3, column=0)
    increment()


acceuil = ttkb.Window(themename="superhero")
acceuil.geometry("500x500")
acceuil.grid_columnconfigure((0, 1, 2), weight=1)

image = Image.open("logo.png")
image_reduit = image.resize((int(image.size[0] * 0.2), int(image.size[1] * 0.2)))
i = ImageTk.PhotoImage(image=image_reduit)
ttkb.Label(acceuil, image=i).grid(row=0, column=0, columnspan=3, pady=(20, 0))
ttkb.Label(acceuil, text="GESTICADO", bootstyle="success", font=("poppins", 20, "bold")).grid(column=0, columnspan=3, row=1,
                                                                                              sticky="ns", pady=(0, 50))

# app.grid_rowconfigure(2, weight=1)
ttkb.Button(acceuil, text="Commencer", bootstyle="success outline", command=commencer).grid(columnspan=3, column=0, row=3,
                                                                                            pady=(5, 195))
var = ttkb.IntVar()
progress = ttkb.Floodgauge(acceuil, bootstyle="success", length=500, value=0, maximum=100, font=("poppins", 15),
                           mask="Loading... {}%", variable=var, mode="determinate")

acceuil.mainloop()
