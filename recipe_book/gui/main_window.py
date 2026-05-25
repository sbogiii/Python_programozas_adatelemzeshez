import tkinter as tk
from tkinter import ttk, messagebox
from data import recipe_manager
from gui.add_recipe_dialog import open_add_dialog


def create_main_window():
    """Főablak létrehozása és elindítása."""
    window = tk.Tk()
    window.title("Digitális Receptkönyv")
    window.geometry("900x600")


    #Bal panel
    left_frame = tk.Frame(window, width=300)
    left_frame.pack(side="left", fill="both", padx=10, pady=10)

    #Keresőmező
    tk.Label(left_frame, text="Keress egy recept nevére:", font=("Arial", 10, "bold")).pack(anchor="w")
    search_var = tk.StringVar()
    search_entry = tk.Entry(left_frame, textvariable=search_var)
    search_entry.pack(fill="x", pady=5)

    #Kategória szűrő
    tk.Label(left_frame, text="Kategória:", font=("Arial", 10, "bold")).pack(anchor="w")
    categories = ["mind", "leves", "főétel", "köret", "desszert", "ital", "egyéb"]
    category_var = tk.StringVar(value="mind")
    category_menu = ttk.Combobox(left_frame, textvariable=category_var,values=categories, state="readonly")
    category_menu.pack(fill="x", pady=5)

    #Összetevő szűrő
    tk.Label(left_frame, text="Összetevők:", font=("Arial", 10, "bold")).pack(anchor="w")
    ingredients_filter = tk.Listbox(left_frame, selectmode="multiple", height=5)
    ingredients_filter.pack(fill="x", pady=5)
    selected_label = tk.Label(left_frame, text="", wraplength=200, justify="left", font=("Arial", 9, "italic"))
    selected_label.pack(anchor="w")

    #Receptlista
    recipe_listbox = tk.Listbox(left_frame)
    recipe_listbox.pack(fill="both", expand=True, pady=5)

    #Gombok
    def on_add_recipe():
        """Megnyitja az új recept hozzáadásához szükséges dialog-ot."""
        open_add_dialog(window, lambda: refresh_list(recipe_manager.recipes))
    add_button = tk.Button(left_frame, text="Recept hozzáadása", command=on_add_recipe)
    add_button.pack(fill="x", pady=2)

    def on_delete_recipe():
        """Törli a kiválasztott receptet."""
        selection = recipe_listbox.curselection()
        if not selection:
            messagebox.showwarning("Figyelmeztetés", "Nincs kiválasztott recept!")
            return
        
        selected_index = selection[0]
        selected_name = recipe_listbox.get(selected_index)
        recipe_manager.delete_recipe(selected_name)
        refresh_list(recipe_manager.recipes)

        if recipe_manager.recipes:
            next_index = min(selected_index, len(recipe_manager.recipes)-1)
            recipe_listbox.selection_set(next_index)
            recipe_listbox.event_generate("<<ListboxSelect>>")
        else:
            name_label.config(text="")
            category_label.config(text="")
            ingredients_text.config(state="normal")
            ingredients_text.delete("1.0", tk.END)
            ingredients_text.config(state="disabled")
            instructions_text.config(state="normal")
            instructions_text.delete("1.0", tk.END)
            instructions_text.config(state="disabled")

    delete_button = tk.Button(left_frame, text="Recept törlése", command=on_delete_recipe)
    delete_button.pack(fill="x", pady=2)

    def clear_filters():
        """Törli az összes szűrőt."""
        nonlocal current_ingredient_filter
        current_ingredient_filter = []
        search_var.set("")
        category_var.set("mind")
        ingredients_filter.selection_clear(0, tk.END)
        refresh_list(recipe_manager.recipes)
        selected_label.config(text="")
    
    clear_button = tk.Button(left_frame, text="Szűrők törlése", command=clear_filters)
    clear_button.pack(fill="x", pady=2)

    #Jobb panel
    right_frame = tk.Frame(window)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    name_label = tk.Label(right_frame, text="", font=("Arial", 18, "bold"))
    name_label.pack(anchor="w", pady=5)

    category_label = tk.Label(right_frame, text="", font=("Arial", 10, "bold"))
    category_label.pack(anchor="w")

    tk.Label(right_frame, text="Hozzávalók:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10,0))
    ingredients_text = tk.Text(right_frame, height=8, state="disabled", font=("Arial", 10))
    ingredients_text.pack(fill="x", pady=5)

    tk.Label(right_frame, text="Elkészítés:", font=("Arial", 10, "bold")).pack(anchor="w")
    instructions_text = tk.Text(right_frame, height=12, state="disabled", font=("Arial", 10))
    instructions_text.pack(fill="both", expand=True, pady=5)

    current_ingredient_filter = []

    def refresh_list(recipe_list):
        """Frissíti a receptlistát."""
        recipe_listbox.delete(0, tk.END)
        for r in recipe_list:
            recipe_listbox.insert(tk.END, r.name)

    def refresh_ingredients_filter():
        """Frissíti az összetevő szűrőt az összes recept összetevőiből."""
        all_ingredients = set()
        for r in recipe_manager.recipes:
            for i in r.ingredients:
                all_ingredients.add(i.lower())
            ingredients_filter.delete(0, tk.END)
            for i in sorted(all_ingredients):
                ingredients_filter.insert(tk.END, i)

    def apply_filters(*args):
        """Minden szűrőt figyelembe véve frissíti a receptek listáját."""
        query = search_var.get()
        category = category_var.get()
        
        results = recipe_manager.recipes

        if category != "mind":
            results = [r for r in results if r.category.lower() == category.lower()]

        if query:
            results = [r for r in results if query.lower() in r.name.lower()]
        
        if current_ingredient_filter:
            results = [r for r in results if all(ing in [i.lower() for i in r.ingredients] for ing in current_ingredient_filter)]

        refresh_list(results)


    def show_recipe(event):
        """Megjeleníti a kiválasztott recept részleteit."""
        selection = recipe_listbox.curselection()
        if not selection:
            return
        selected_name = recipe_listbox.get(selection[0])
        recipe = next((r for r in recipe_manager.recipes if r.name == selected_name), None)
        if not recipe:
            return

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
    
    def on_ingredients_select(event):
        """Összetevő kijelöléskor frissíti a szűrőt."""
        nonlocal current_ingredient_filter
        new_selection = [ingredients_filter.get(i) for i in ingredients_filter.curselection()]
        if new_selection:
            current_ingredient_filter = new_selection
        apply_filters()
        if current_ingredient_filter:
            selected_label.config(text="Kiválasztva: "+", ".join(current_ingredient_filter))
        else:
            selected_label.config(text="")

    search_var.trace_add("write", apply_filters)
    category_var.trace_add("write", apply_filters)
    ingredients_filter.bind("<<ListboxSelect>>", on_ingredients_select)
    
    recipe_listbox.bind("<<ListboxSelect>>", show_recipe)

    recipe_manager.load_recipes()
    refresh_list(recipe_manager.recipes)
    refresh_ingredients_filter()
    window.mainloop()
