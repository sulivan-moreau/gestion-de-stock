import tkinter as tk
from tkinter import ttk, simpledialog
import mysql.connector

# Connexion à la base de données
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pompom42650",
        database="store"
    )

# Récupération des produits
def fetch_products():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, name, price, quantity FROM product")
    products = cursor.fetchall()
    db.close()
    return products

# Ajout d'un produit
def add_product(name, price, quantity, id_category):
    db = connect_to_db()
    cursor = db.cursor()
    sql = "INSERT INTO product (name, price, quantity, id_category) VALUES (%s, %s, %s, %s)"
    values = (name, price, quantity, id_category)
    cursor.execute(sql, values)
    db.commit()
    db.close()
    refresh_products()

# Suppression d'un produit
def delete_product(product_id):
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
    db.commit()
    db.close()
    refresh_products()
    


# Mise à jour de l'affichage des produits
def refresh_products():
    for i in tree.get_children():
        tree.delete(i)
    for product in fetch_products():
        tree.insert('', tk.END, values=product)

# Interface graphique
def create_gui():
    global tree
    window = tk.Tk()
    window.title("Gestion de Stock")

    tree = ttk.Treeview(window, columns=('ID', 'Name', 'Price', 'Quantity'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Name', text='Name')
    tree.heading('Price', text='Price')
    tree.heading('Quantity', text='Quantity')

    refresh_products()

    # Boutons pour la gestion des produits
    tk.Button(window, text="Ajouter Produit", command=lambda: add_product_dialog()).pack(side=tk.TOP, fill=tk.X)
    tk.Button(window, text="Supprimer Produit", command=lambda: delete_product_dialog()).pack(side=tk.TOP, fill=tk.X)

    tree.pack(side='left', fill='both', expand=True)
    window.mainloop()

# Dialogues pour l'ajout et la suppression de produits
def add_product_dialog():
    # Exemple simple, à étendre selon les besoins
    name = simpledialog.askstring("Nom", "Entrez le nom du produit")
    price = simpledialog.askinteger("Prix", "Entrez le prix du produit")
    quantity = simpledialog.askinteger("Quantité", "Entrez la quantité du produit")
    id_category = simpledialog.askinteger("Catégorie", "Entrez l'ID de la catégorie du produit")
    add_product(name, price, quantity, id_category)

def delete_product_dialog():
    product_id = simpledialog.askstring("Supprimer", "Entrez l'ID du produit à supprimer")
    delete_product(product_id)

if __name__ == "__main__":
    create_gui()
