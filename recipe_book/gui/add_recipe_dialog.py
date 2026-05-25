import tkinter as tk
from tkinter import ttk, messagebox
from models.recipe import Recipe
from data import recipe_manager

def open_add_dialog(parent, on_save):
    """Megnyitja az új recept hozzáadása modalt."""
    dialog = tk.Toplevel(parent)
    dialog.title("Új recept hozzáadása")
    dialog.geometry("500x600")
    dialog.grab_set()

    #Név megadása
    tk.Label(dialog, text="Recept neve:").pack(anchor="w", padx=10, pady=(10,0))
    name_entry=tk.Entry(dialog)
    name_entry.pack(fill="x", padx=10)

    #Kategória kiválasztása
    tk.Label(dialog, text="Kategória").pack(anchor="w", padx=10, pady=(10,0))
    categories = ["leves", "főétel", "köret", "desszert", "ital", "egyéb"]
    category_var = tk.StringVar(value="leves")
    category_menu = ttk.Combobox(dialog, textvariable=category_var, values=categories, state="readonly")
    category_menu.pack(fill="x", padx=10)

    #Hozzávalók felsorolása
    tk.Label(dialog, text="Hozzávalók:").pack(anchor="w", padx=10, pady=(10,0))
    ingredients_text = tk.Text(dialog, height=6)
    ingredients_text.pack(fill="x", padx=10)

    #Elkészítési mód leírása
    tk.Label(dialog, text="Elkészítés:").pack(anchor="w", padx=10, pady=(10,0))
    instructions_text = tk.Text(dialog, height=8)
    instructions_text.pack(fill="x", padx=10)

    def save_recipe():
        """Elmenti az új receptet, ha a név ki van töltve, és a recept még nem létezik."""
        name = name_entry.get().strip()
        category = category_var.get()
        ingredients =  [line.strip() for line in ingredients_text.get("1.0", tk.END).splitlines() if line.strip()]
        instructions = [line.strip() for line in instructions_text.get("1.0", tk.END).splitlines() if line.strip()]

        if not name:
            messagebox.showerror("Hiba", "A recept neve kötelező!", parent=dialog)
            return
        
        recipe = Recipe(name, category, ingredients, instructions)
        if not recipe_manager.add_recipe(recipe):
            messagebox.showerror("Hiba", "Ilyen nevű recept már létezik!", parent=dialog)
            return
        
        on_save()
        dialog.destroy()

    tk.Button(dialog, text="Mentés", command=save_recipe).pack(fill="x", padx=10, pady=10)
    tk.Button(dialog, text="Mégse", command=dialog.destroy).pack(fill="x", padx=10)
