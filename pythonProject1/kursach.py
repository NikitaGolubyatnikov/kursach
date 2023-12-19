import tkinter as tk
import json
from tkinter import messagebox


class BusRouteApp:
    def __init__(self, root):
        # Инициализация основного окна
        self.root = root
        self.root.title("Автобусные маршруты")
        self.bus_routes = []  # Список для хранения маршрутов

        # Загрузка маршрутов из файла при запуске
        self.load_bus_routes()

        # Создание виджетов интерфейса
        self.create_widgets()

    def load_bus_routes(self):
        # Загрузка маршрутов из файла JSON
        try:
            with open('bus_routes.json', 'r', encoding='utf-8') as file:
                self.bus_routes = json.load(file)
        except FileNotFoundError:
            pass

    def save_bus_routes(self):
        # Сохранение маршрутов в файл JSON
        with open('bus_routes.json', 'w', encoding='utf-8') as file:
            json.dump(self.bus_routes, file, indent=4, ensure_ascii=False)

    def create_widgets(self):
        # Загрузка изображения для фона главного окна
        self.background_image = tk.PhotoImage(file="background_image.png")

        # Создание метки для отображения изображения на главном окне
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Растягиваем изображение на всё окно

        # Настройка шрифта для кнопок и меток
        button_font = ('Arial', 12)
        entry_font = ('Arial', 10)

        # Создание кнопок для управления маршрутами
        self.new_route_button = tk.Button(self.root, text="Создать новый маршрут", command=self.create_new_route,
                                          font=button_font)
        self.new_route_button.pack(padx=10, pady=10)

        self.edit_route_button = tk.Button(self.root, text="Редактировать маршрут",
                                           command=self.show_edit_route_options, font=button_font)
        self.edit_route_button.pack(padx=10, pady=10)

        self.delete_route_button = tk.Button(self.root, text="Удалить маршрут", command=self.show_delete_route_options,
                                             font=button_font)
        self.delete_route_button.pack(padx=10, pady=10)

        self.exit_button = tk.Button(self.root, text="Выход", command=self.save_and_exit, font=button_font)
        self.exit_button.pack(padx=10, pady=10)

        # Создание полей ввода для данных маршрута
        tk.Label(self.root, text="Номер автобуса:", font=entry_font).pack()
        self.bus_number_entry = tk.Entry(self.root, font=entry_font)
        self.bus_number_entry.pack()

        tk.Label(self.root, text="Остановки (через запятую):", font=entry_font).pack()
        self.stops_entry = tk.Entry(self.root, font=entry_font)
        self.stops_entry.pack()

        tk.Label(self.root, text="Время (через запятую):", font=entry_font).pack()
        self.time_entry = tk.Entry(self.root, font=entry_font)
        self.time_entry.pack()

        self.routes_frame = tk.Frame(self.root)
        self.routes_frame.pack(padx=10, pady=10)

        # Обновление списка маршрутов
        self.update_routes_buttons()

    def create_new_route(self):
        # Создание нового маршрута на основе данных из полей ввода
        bus_number = self.bus_number_entry.get().strip()
        stops = self.stops_entry.get().strip()
        time = self.time_entry.get().strip()

        if not bus_number or not stops or not time:
            print("Заполните все поля")
            return

        stops = stops.split(',')
        time = time.split(',')

        for route in self.bus_routes:
            if route['bus_number'] == bus_number:
                print("Маршрут с таким номером уже существует")
                return

        new_route = {
            'bus_number': bus_number,
            'stops': stops,
            'time': time
        }

        self.bus_routes.append(new_route)
        self.save_bus_routes()
        self.update_routes_buttons()

        # Очистка полей ввода после создания нового маршрута
        self.bus_number_entry.delete(0, tk.END)
        self.stops_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)

    def show_edit_route_options(self):
        # Создание окна для редактирования маршрутов
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактировать маршрут")

        # Создание списка для отображения доступных маршрутов
        routes_listbox = tk.Listbox(edit_window)
        routes_listbox.pack()

        # Добавление доступных маршрутов в список
        for route in self.bus_routes:
            routes_listbox.insert(tk.END, route['bus_number'])

        # Кнопка для выбора маршрута для редактирования
        edit_button = tk.Button(edit_window, text="Выбрать",
                                command=lambda: self.edit_route(routes_listbox.get(tk.ACTIVE), edit_window))
        edit_button.pack()

    def edit_route(self, selected_route, edit_window):
        # Поиск данных выбранного маршрута
        selected_route_data = None
        for route in self.bus_routes:
            if route['bus_number'] == selected_route:
                selected_route_data = route
                break

        if selected_route_data:
            edit_window.destroy()  # Закрытие окна выбора маршрута для редактирования

            # Создание нового окна для редактирования выбранного маршрута
            edit_window = tk.Toplevel(self.root)
            edit_window.title(f"Редактировать маршрут {selected_route}")

            # Создание полей ввода для редактирования данных маршрута
            tk.Label(edit_window, text="Номер автобуса:").pack()
            bus_number_entry = tk.Entry(edit_window)
            bus_number_entry.insert(tk.END, selected_route_data['bus_number'])
            bus_number_entry.pack()

            tk.Label(edit_window, text="Остановки (через запятую):").pack()
            stops_entry = tk.Entry(edit_window)
            stops_entry.insert(tk.END, ', '.join(selected_route_data['stops']))
            stops_entry.pack()

            tk.Label(edit_window, text="Время (через запятую):").pack()
            time_entry = tk.Entry(edit_window)
            time_entry.insert(tk.END, ', '.join(selected_route_data['time']))
            time_entry.pack()

            # Кнопка для сохранения изменений в маршруте
            update_button = tk.Button(edit_window, text="Сохранить изменения",
                                      command=lambda: self.update_route(selected_route_data, bus_number_entry.get(),
                                                                        stops_entry.get(), time_entry.get(),
                                                                        edit_window))
            update_button.pack()

    def show_delete_route_options(self):
        # Создание окна для удаления маршрутов
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Удалить маршрут")

        # Создание списка для отображения доступных маршрутов
        routes_listbox = tk.Listbox(delete_window)
        routes_listbox.pack()

        # Добавление доступных маршрутов в список
        for route in self.bus_routes:
            routes_listbox.insert(tk.END, route['bus_number'])

        # Кнопка для выбора маршрута для удаления
        delete_button = tk.Button(delete_window, text="Выбрать",
                                  command=lambda: self.delete_route(routes_listbox.get(tk.ACTIVE)))
        delete_button.pack()

    def delete_route(self, selected_route):
        # Запрос подтверждения удаления маршрута
        confirm_delete = tk.messagebox.askokcancel("Подтверждение удаления",
                                                   f"Вы точно хотите удалить маршрут {selected_route}?")

        # Если подтверждено удаление
        if confirm_delete:
            # Поиск маршрута для удаления и удаление его
            for route in self.bus_routes:
                if route['bus_number'] == selected_route:
                    self.bus_routes.remove(route)
                    print(f"Маршрут {selected_route} удален")
                    break
            else:
                print("Маршрут не найден")

            # Сохранение изменений, обновление интерфейса и списка маршрутов для удаления
            self.save_bus_routes()
            self.update_routes_buttons()  # Обновляем интерфейс после удаления маршрута

            # Обновление списка маршрутов для удаления и закрытие старого окна удаления
            self.update_delete_route_options()

    def update_delete_route_options(self):
        # Закрытие старого окна удаления, если оно открыто
        if hasattr(self, 'delete_window') and getattr(self, 'delete_window', None):
            self.delete_window.destroy()

        # Создание нового окна для удаления маршрутов
        self.delete_window = tk.Toplevel(self.root)
        self.delete_window.title("Удалить маршрут")

        routes_listbox = tk.Listbox(self.delete_window)
        routes_listbox.pack()

        for route in self.bus_routes:
            routes_listbox.insert(tk.END, route['bus_number'])

        # Кнопка для выбора маршрута для удаления
        delete_button = tk.Button(self.delete_window, text="Выбрать",
                                  command=lambda: self.delete_route(routes_listbox.get(tk.ACTIVE)))
        delete_button.pack()

    def save_and_exit(self):
        # Сохранение маршрутов и закрытие приложения
        self.save_bus_routes()
        self.root.destroy()

    def update_routes_buttons(self):
        # Очистка фрейма перед обновлением
        for widget in self.routes_frame.winfo_children():
            widget.destroy()

        # Добавление кнопок для каждого маршрута
        for route in self.bus_routes:
            route_button = tk.Button(self.routes_frame, text=f"Маршрут {route['bus_number']}",
                                     command=lambda r=route: self.display_route_info(r))
            route_button.pack()

    def display_route_info(self, route):
        # Отображение информации о выбранном маршруте в отдельном окне
        info_window = tk.Toplevel(self.root)
        info_window.title(f"Информация о маршруте {route['bus_number']}")

        stops = ', '.join(route['stops'])
        times = ', '.join(route['time'])

        route_info_label = tk.Label(info_window,
                                    text=f"Номер автобуса: {route['bus_number']}\nОстановки: {stops}\nВремя: {times}")
        route_info_label.pack()

    def update_route(self, selected_route_data, new_bus_number, new_stops, new_time, edit_window):
        # Обновление информации о маршруте после редактирования
        new_stops = new_stops.split(',')
        new_time = new_time.split(',')

        selected_route_data['bus_number'] = new_bus_number
        selected_route_data['stops'] = new_stops
        selected_route_data['time'] = new_time

        # Сохранение изменений, обновление интерфейса и закрытие окна редактирования
        self.save_bus_routes()
        self.update_routes_buttons()
        edit_window.destroy()  # Закрытие окна редактирования

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1280x720")  # Установка размеров окна
    app = BusRouteApp(root)
    root.mainloop()