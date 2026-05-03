import tkinter as tk
from tkinter import ttk
from data import recipe_manager


def create_main_window():
    """Főablak létrehozása és elindítása."""
    window = tk.Tk()
    window.title("Digitális Receptkönyv")
    window.geometry("900x600")


    #Bal panel
    left_frame = tk.Frame(window, width=300)
    left_frame.pack(side="left", fill="both", padx=10, pady=10)

    #Keresőmező
    search_var = tk.StringVar()
    search_entry = tk.Entry(left_frame, textvariable=search_var)
    search_entry.pack(fill="x", pady=5)

    #Kategória szűrő
    categories = ["mind", "leves", "főétel", "köret", "desszert", "ital", "egyéb"]
    category_var = tk.StringVar(value="mind")
    category_menu = ttk.Combobox(left_frame, textvariable=category_var,values=categories, state="readonly")
    category_menu.pack(fill="x", pady=5)

    #Receptlista
    recipe_listbox = tk.Listbox(left_frame)
    recipe_listbox.pack(fill="both", expand=True, pady=5)

    #Gombok
    add_button = tk.Button(left_frame, text="Recept hozzáadása")
    add_button.pack(fill="x", pady=2)

    delete_button = tk.Button(left_frame, text="Recept törlése")
    delete_button.pack(fill="x", pady=2)

    #Jobb panel
    right_frame = tk.Frame(window)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    name_label = tk.Label(right_frame, text="")
    name_label.pack(anchor="w", pady=5)

    category_label = tk.Label(right_frame, text="")
    category_label.pack(anchor="w")

    tk.Label(right_frame, text="Hozzávalók:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10,0))
    ingredients_text = tk.Text(right_frame, height=8, state="disabled")
    ingredients_text.pack(fill="x", pady=5)

    tk.Label(right_frame, text="Elkészítés:", font=("Arial", 10, "bold")).pack(anchor="w")
    instructions_text = tk.Text(right_frame, height=12, state="disabled")
    instructions_text.pack(fill="both", expand=True, pady=5)


    def refresh_list(recipe_list):
        """Frissíti a receptlistát."""
        recipe_listbox.delete(0, tk.END)
        for r in recipe_list:
            recipe_listbox.insert(tk.END, r.name)

    def on_search(*args):
        """Lista frissítése a keresőmezőbe gépeléskor."""
        query = search_var.get()
        if query:
            refresh_list(recipe_manager.search_by_name(query))
        else:
            refresh_list(recipe_manager.recipes)
    search_var.trace_add("write", on_search)

    def on_category_change(*args):
        """Lista frissítése a kategória változtatáskor."""
        category = category_var.get()
        if category == "mind":
            refresh_list(recipe_manager.recipes)
        else:
            refresh_list(recipe_manager.filter_by_category(category))

        category_var.trace_add("write", on_category_change)

    def show_recipe(event):
        """Megjeleníti a kiválasztott recept részleteit."""
        selection = recipe_listbox.curselection()
        if not selection:
            return
        selected_name = recipe_listbox.get(selection[0])
        recipe = next(r for r in recipe_manager.recipes if r.name == selected_name)

        name_label.config(text=recipe.name)
        category_label.config(text=f"Kategória: {recipe.category}")

        ingredients_text.config(state="normal")
        ingredients_text.delete("1.0", tk.END)
        ingredients_text.insert(tk.END, "\n".join(recipe.ingredients))
        ingredients_text.config(state="disabled")

        instructions_text.config(state="normal")
        instructions_text.delete("1.0", tk.END)
        instructions_text.insert(tk.END, "\n".join(recipe.instructions))
        instructions_text.config(state="disabled")
    
    recipe_listbox.bind("<<ListboxSelect>>", show_recipe)

    recipe_manager.load_recipes()
    refresh_list(recipe_manager.recipes)
    window.mainloop()
