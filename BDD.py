from ttkbootstrap.dialogs import Messagebox
import pymysql

try:
    bdd = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="gesticado")

    bdd_cursor = bdd.cursor()
except:
    Messagebox.show_error(title="Erreur", message="Impossible de se connecter a la base de donnee!")
