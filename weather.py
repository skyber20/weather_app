# сделать программу, где ты вводишь данные, и если они совпадают, то можешь посмотреть погоду
# пароль и логин должны быть не менее 8 символов
# если они совпадают вывести ошибку


from tkinter import *
from tkinter import messagebox
import requests
from API_key import API_KEY



def transition():
    register_window.withdraw()
    weather_window.deiconify()


def login():
    with open('users_weather.csv', encoding='UTF8') as file:
        users = [user.strip().split(';') for user in file.readlines()[1:]]
    username = username_entry.get()
    password = password_entry.get()
    if not password or not username:
        messagebox.showerror('Ошибка!', 'Нужно заполнить все поля')
    else:
        for user in users:
            if user[0] == username and user[1] == password:
                a, b, c = username == password, len(username) < 8, len(password) < 8
                if a:
                    messagebox.showerror('Ошибка!', 'Имя пользователя и пароль не должны совпадать')
                if b:
                    messagebox.showerror('Ошибка!', 'Имя пользователя должно быть не мнее чем 8 символов')
                if c:
                    messagebox.showerror('Ошибка!', 'Пароль должно быть не мнее чем 8 символов')
                if not(any([a, b, c])):
                    transition()
                break
        else:
            messagebox.showerror("Ошибка!", "Неравильное имя пользователя или пароль")


register_window = Tk()
register_window.title = 'Авторизация'
register_window['bg'] = '#fafafa'
register_window.geometry('500x400')
register_window.resizable(width=False, height=False)

weather_window = Tk()
weather_window.resizable(height=False, width=False)
weather_window.geometry('500x400')
weather_window['bg'] = '#fafafa'
weather_window.title = 'Погода'

# canvas = Canvas(root, width=300, height=300)
# canvas.pack()

frame = Frame(register_window, bg='#fafafa')
frame.place(relheight=0.6, relwidth=0.5, relx=0.25, rely=0.2)

auth_text = Label(register_window, text='АВТОРИЗАЦИЯ', font='Arial 20', bg='#fafafa', fg='black')
auth_text.pack(pady=20)

Label(frame, text='Логин', bg='#fafafa').grid(row=0, column=0, padx=10, pady=10)
username_entry = Entry(frame)
username_entry.grid(row=0, column=1, padx=10, pady=10)

Label(frame, text='Пароль', bg='#fafafa').grid(row=1, column=0, padx=10, pady=10)
password_entry = Entry(frame, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

Button(frame, text='Войти', command=login).grid(row=2, columnspan=2)

Button(register_window, text='Выйти', command=register_window.quit).pack(side='left', anchor='sw', padx=20, pady=30)



def show_weather():
    city = city_entry.get()
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}') 
    if response.status_code == 200:
        data = response.json()
        name_city = data['name']
        main = data['weather'][0]['main']
        temperature = round(int(data['main']['temp'])) - 273
        wind = round(int(data['wind']['speed']))
        humidity = data['main']['humidity']
        
        Label(frame_weather, bg='#fafafa', text=f'Город: {name_city}').grid(row=2, columnspan=2, pady=10)
        Label(frame_weather, bg='#fafafa', text=f'Осадки: {main}').grid(row=3, column=0,padx=10, pady=5)
        Label(frame_weather, bg='#fafafa', text=f'Температура: {temperature}').grid(row=3, column=1,padx=10, pady=5)
        Label(frame_weather, bg='#fafafa', text=f'Скорость ветра: {wind}').grid(row=4, column=0,padx=10, pady=5)
        Label(frame_weather, bg='#fafafa', text=f'Влажность: {humidity}').grid(row=4, column=1,padx=10, pady=5)
    else:
        messagebox.showerror("Ошибка!", "Ничего не найдено")


Label(weather_window, text='ПОГОДА', bg='#fafafa', font='Arial 20', pady=20).pack()

frame_weather = Frame(weather_window, bg='#fafafa')
frame_weather.place(relheight=0.6, relwidth=0.6, rely=0.2, relx=0.2)

Label(frame_weather, text='Город', bg='#fafafa').grid(row=0, column=0, padx=10, pady=10)
city_entry = Entry(frame_weather)
city_entry.grid(row=0, column=1, pady=10, padx=10)

Button(frame_weather, text='Посмотреть', command=show_weather).grid(row=1, columnspan=2, pady=10)

Button(weather_window, text='Выйти', command=weather_window.quit).pack(side='left', anchor='sw', padx=20, pady=30)


weather_window.withdraw()

register_window.mainloop()
weather_window.mainloop()
