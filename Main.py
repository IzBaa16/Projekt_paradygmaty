import requests # musisz to zainstalować "pip install requests"
import tkinter as tk
from tkinter import ttk

# liczba rekordów do wyświetlenia (początkowa ( i globalna))
display_limit = 20

# funkcja do pobierania danych z CoinCap API (to samo co w blazor)
def fetch_data():
    url = "https://api.coincap.io/v2/assets"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and 'data' in data:
        return data['data'] 
    else:
        return []

# funkcja do wyświetlania danych
def display_data():
    global display_limit 

    data = fetch_data()
    if not data:
        result_label.config(text="Błąd w pobieraniu danych.")
        return

    data_to_display = data[:display_limit]

    # za każdym razem jak zmienia się ilość wierszy to musimy wszystko usunąć i stworzyć od nowa
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    # nagłówki tabeli
    headers = ["Nazwa", "Symbol", "Cena"]
    for col, header in enumerate(headers):
        label = tk.Label(canvas_frame, text=header, font=('Arial', 18, 'bold'), bg="#4CAF50", fg="white", padx=10, pady=5, width=30)
        label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

    # Ustawiamy konfigurację kolumn, aby były równomiernie rozmieszczone
    for col in range(len(headers)):
        canvas_frame.grid_columnconfigure(col, weight=1, uniform="equal")

    # tabela danych
    for i, coin in enumerate(data_to_display):
        name_label = tk.Label(canvas_frame, text=coin['name'], font=('Arial', 15), bg="#f4f4f9", padx=10, pady=5, anchor="center")
        name_label.grid(row=i + 1, column=0, padx=5, pady=5)
        
        symbol_label = tk.Label(canvas_frame, text=coin['symbol'], font=('Arial', 15), bg="#f4f4f9", padx=10, pady=5, anchor="center")
        symbol_label.grid(row=i + 1, column=1, padx=5, pady=5)
        
        price_label = tk.Label(canvas_frame, text=f"${float(coin['priceUsd']):,.2f}", font=('Arial', 15), bg="#f4f4f9", padx=10, pady=5, anchor="center")
        price_label.grid(row=i + 1, column=2, padx=5, pady=5)

    # aktualizujemy region przewijania, aby działało poprawnie
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


# funkcja do zwiększania liczby rekordów o 5
def add_five():
    global display_limit
    display_limit += 5
    display_data()

# funkcja do zmniejszania liczby rekordów o 5
def remove_five():
    global display_limit
    if display_limit > 5:  # Zabezpieczenie by nie dało rady wyświetlić mniej niż 5 rekordów (czyli min 5)
        display_limit -= 5
    display_data()


# TU SIĘ ZACZYNA APLIKACJA SAMA W SOBIE

# główne okno aplikacji
root = tk.Tk()
root.title("Kryptowaluty - CoinCap")
root.geometry("1500x900") # NIE RUSZAJ TEGO (to jest do zmiany rozmiaru okna. Wtedy kolumny się rozsypią)

# ustawiamy tło okna
root.config(bg="#2E3B4E") # jak masz lepszy kolor to na html hexcolors sobie wybierz

# ramkę na elementy statyczne (przyciski, etykiety u góry)
top_frame = tk.Frame(root, bg="#2E3B4E")
top_frame.pack(fill="x", padx=10, pady=10)

# etykieta na wynik
result_label = tk.Label(top_frame, text="Dane o kryptowalutach", font=('Arial', 20, 'bold'), bg="#2E3B4E", fg="white")
result_label.pack(pady=5)

# przycisk do dodania 5 rekordów
add_button = tk.Button(top_frame, text="Dodaj 5 rekordów", command=add_five, bg="#4CAF50", fg="white", font=('Arial', 18, 'bold'))
add_button.pack(side="left", padx=5)

# przycisk do usunięcia 5 rekordów
remove_button = tk.Button(top_frame, text="Usuń 5 rekordów", command=remove_five, bg="#f44336", fg="white", font=('Arial', 18, 'bold'))
remove_button.pack(side="left", padx=5)

# ramka z przewijaniem (to ta po prawej mała)
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# ramka w canvasie, która ma naszą tabelę
canvas_frame = tk.Frame(canvas, bg="#f4f4f9")
canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

# pasek przewijania
scrollbar.pack(side="right", fill="y")
canvas.pack(padx=10, pady=10, fill="both", expand=True)


display_data()
root.mainloop()
