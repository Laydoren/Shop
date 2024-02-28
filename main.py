import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import json

class OnlineStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Store")
        self.users = self.load_users()
        self.current_user = None

        self.login_frame = self.create_login_frame()

    def load_users(self):
        try:
            with open('users.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_users(self):
        with open('users.json', 'w') as file:
            json.dump(self.users, file)

    def create_login_frame(self):
        frame = tk.Frame(self.root)
        frame.pack()

        self.login_label = tk.Label(frame, text="Введите имя пользователя:")
        self.login_label.pack(pady=10)

        self.login_entry = tk.Entry(frame)
        self.login_entry.pack(pady=10)

        self.login_button = tk.Button(frame, text="Войти", command=self.login)
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(frame, text="Зарегистрироваться", command=self.register)
        self.register_button.pack(pady=10)

        return frame

    def add_item_to_cart(self, event):
        selected_item = self.catalogue_listbox.get(self.catalogue_listbox.curselection())
        item_name, item_price = selected_item.split(" - ")[0], float(selected_item.split(" - ")[1][:-3])

        new_product = {"name": item_name, "price": item_price}
        self.current_user["cart"].append(new_product)
        self.update_cart_listbox()
        self.save_users()

    def create_catalogue_frame(self):
        self.catalogue_frame = tk.Frame(self.root)

        self.catalogue_items = [
            {"name": "Вода", "price": 12.0},
            {"name": "Молоко", "price": 20.0},
            {"name": "Кирпич", "price": 100.0},
            {"name": "Карта сокровищ", "price": 250000.0},
            {"name": "Пакет в пакете", "price": 2.0},
            {"name": "Карандаш", "price": 10.0},
            {"name": "Тетрадь", "price": 15.0},
            {"name": "Ничего", "price": 0.0},
            {"name": "Шоколадка", "price": 50.0},
            {"name": "Орех", "price": 5.0},
        ]

        self.scrollbar = tk.Scrollbar(self.catalogue_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.catalogue_listbox = tk.Listbox(self.catalogue_frame, yscrollcommand=self.scrollbar.set)
        self.catalogue_listbox.pack(pady=10)

        self.scrollbar.config(command=self.catalogue_listbox.yview)

        for item in self.catalogue_items:
            self.catalogue_listbox.insert(tk.END, f"{item['name']} - {item['price']} ₽")

        self.catalogue_listbox.bind("<Double-Button-1>", self.add_item_to_cart)

        exit_button = tk.Button(self.catalogue_frame, text="Скрыть каталог", command=self.catalogue_frame.destroy)
        exit_button.pack(pady=10)

        return self.catalogue_frame

    def login(self):
        username = self.login_entry.get()
        for user in self.users:
            if user['name'] == username:
                self.current_user = user
                self.create_main_frame()
                self.login_frame.destroy()  # Destroy the existing login frame

                return
        messagebox.showerror("Ошибка", "Пользователь не найден")

    def logout(self):
        self.current_user = None
        self.main_frame.destroy()
        self.login_frame.destroy()  # Destroy the existing login frame
        self.login_frame = self.create_login_frame()  # Create a new login frame
        self.login_frame.pack()
        self.catalogue_frame.destroy()
        self.profile_window.destroy()

    def register(self):
        username = simpledialog.askstring("Регистрация", "Введите ваше имя:")
        if username:
            new_user = {'name': username, 'cart': [], 'profile_picture': None}
            self.users.append(new_user)
            self.save_users()
            self.login_entry.delete(0, tk.END)
            self.login_entry.insert(tk.END, username)
            self.login()
            self.login_frame.destroy()

    def create_main_frame(self):

        self.login_frame.destroy()

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        self.cart_listbox = tk.Listbox(self.main_frame, width=50)
        self.cart_listbox.pack(pady=10)

        def remove_item_from_cart(event):
            selected_index = self.cart_listbox.curselection()
            if selected_index:
                selected_index = selected_index[0]
                if selected_index >= 0 and selected_index < len(self.current_user['cart']):
                    del self.current_user['cart'][selected_index]
                    self.update_cart_listbox()
                    self.save_users()

        self.cart_listbox.bind("<Double-Button-1>", remove_item_from_cart)

        self.add_to_cart_button = tk.Button(self.main_frame, text="Добавить в корзину", command=self.add_to_cart)
        self.add_to_cart_button.pack(pady=10)

        self.remove_from_cart_button = tk.Button(self.main_frame, text="Удалить из корзины", command=self.remove_from_cart)
        self.remove_from_cart_button.pack(pady=10)

        self.calculate_total_button = tk.Button(self.main_frame, text="Общая цена", command=self.calculate_total)
        self.calculate_total_button.pack(pady=10)

        self.catalogue_button = tk.Button(self.main_frame, text="Каталог", command=self.show_catalogue)
        self.catalogue_button.pack(pady=10)

        self.profile_button = tk.Button(self.main_frame, text="Профиль", command=self.open_or_update_profile)
        self.profile_button.pack(pady=10)

        self.logout_button = tk.Button(self.main_frame, text="Выйти", command=self.logout)
        self.logout_button.pack(pady=10)

        self.update_cart_listbox()

    def show_catalogue(self):
        self.catalogue_frame = self.create_catalogue_frame()
        self.catalogue_frame.pack()

    def add_to_cart(self):
        product_name = simpledialog.askstring("Добавить в корзину", "Введите название продукта:")
        product_price = simpledialog.askfloat("Добавить в корзину", "Введите цену продукта:")
        if product_name and product_price:
            new_product = {'name': product_name, 'price': product_price}
            self.current_user['cart'].append(new_product)
            self.update_cart_listbox()
            self.save_users()

    def remove_from_cart(self):
        if not self.current_user['cart']:
            messagebox.showinfo("Корзина пуста", "Ваша корзина пуста")
            return
        product_name = simpledialog.askstring("Удалить из корзины", "Введите название продукта для удаления:")
        if product_name:
            removed_product = None
            for product in self.current_user['cart']:
                if product['name'] == product_name:
                    removed_product = product
                    break
            if removed_product:
                self.current_user['cart'].remove(removed_product)
                self.update_cart_listbox()
                messagebox.showinfo("Удалено", f"{removed_product['name']} был удален из вашей корзины!")

    def calculate_total(self):
        total_price = sum(product['price'] for product in self.current_user['cart'])
        messagebox.showinfo("Общая цена", f"Общая стоимость вашей корзины: {total_price:.2f} ₽")

    def update_cart_listbox(self):
        self.cart_listbox.delete(0, tk.END)
        for item in self.current_user['cart']:
            self.cart_listbox.insert(tk.END, f"{item['name']} - {item['price']} ₽")

    def open_or_update_profile(self):
        if self.current_user:
            self.open_profile()
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, войдите в свой профиль")

    def open_profile(self):
        self.profile_window = tk.Toplevel(self.root)
        self.profile_window.title(f"Ваш профиль, {self.current_user['name']}")

        self.name_label = tk.Label(self.profile_window, text="Имя: " + self.current_user['name'], font=('Helvetica', 14))
        self.name_label.pack(pady=10)

        self.profile_picture_label = tk.Label(self.profile_window, text="Изображение профиля:")
        self.profile_picture_label.pack()

        self.update_profile_picture_label()

        change_name_button = tk.Button(self.profile_window, text="Изменить имя профиля", command=self.change_name)
        change_name_button.pack()

        upload_picture_button = tk.Button(self.profile_window, text="Загрузить фото", command=self.upload_picture)
        upload_picture_button.pack()

        delete_button = tk.Button(self.profile_window, text="Удалить профиль", command=self.delete_profile)
        delete_button.pack()

        close_button = tk.Button(self.profile_window, text="Закрыть", command=self.profile_window.destroy)
        close_button.pack()

    def delete_profile(self):
        if messagebox.askyesno("Удаление профиля", "Вы уверены, что хотите удалить свой профиль? Это действие необратимо."):
            self.users.remove(self.current_user)
            self.current_user = None
            self.save_users()
            self.profile_window.destroy()
            self.logout()

    def update_profile_window(self):
        self.name_label.config(text="Имя: " + self.current_user['name'])
        self.update_profile_picture_label()

    def update_profile_picture_label(self):
        if self.current_user['profile_picture']:
            image = Image.open(self.current_user['profile_picture'])
            image = image.resize((100, 100))
            photo = ImageTk.PhotoImage(image)
            self.profile_picture_label.image = photo
            self.profile_picture_label.config(image=photo)
            self.profile_picture_label.pack()

    def change_name(self):
        new_name = simpledialog.askstring("Изменить имя профиля", "Введите ваше имя:")
        if new_name:
            if any(user['name'] == new_name for user in self.users if user != self.current_user):
                messagebox.showerror("Ошибка", "Имя занято. Пожалуйста, введите другое имя.")
            else:
                self.current_user['name'] = new_name
                self.update_profile_window()

    def upload_picture(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.current_user['profile_picture'] = file_path
            self.update_profile_window()


if __name__ == "__main__":
    root = tk.Tk()
    app = OnlineStoreApp(root)
    root.mainloop()