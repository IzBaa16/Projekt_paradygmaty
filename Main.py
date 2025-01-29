import requests
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime

# Słownik przechowujący dane o portfelu inwestycyjnym
portfolio = {}

# Słownik przechowujący aktualne ceny kryptowalut
crypto_prices = {}

# Słownik przechowujący poprzednie ceny kryptowalut
previous_prices = {}

# Funkcja do pobierania danych z CoinGecko API
def fetch_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 19,
        'page': 1
    }
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200 and isinstance(data, list):
        return data
    else:
        return []

# Funkcja do aktualizacji cen kryptowalut
def update_prices():
    global crypto_prices
    data = fetch_data()
    if not data:
        messagebox.showerror("Błąd", "Nie udało się zaktualizować cen kryptowalut.")
        return

    crypto_prices = {coin['symbol'].upper(): coin['current_price'] for coin in data}

    display_data()
    messagebox.showinfo("Sukces", "Ceny kryptowalut zostały zaktualizowane.")

# Funkcja do generowania raportu
def generate_report():
    global previous_prices

    if not portfolio:
        messagebox.showinfo("Raport", "Twój portfel jest pusty.")
        return

    portfolio_text = ""
    total_value = 0.0
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comparison_text = ""

    for symbol, amount in portfolio.items():
        price = crypto_prices.get(symbol, 0)
        value = price * amount
        total_value += value
        portfolio_text += f"{amount:.6f} {symbol} = ${value:,.2f}\n"

        if symbol in previous_prices:
            previous_price = previous_prices[symbol]
            if price > previous_price:
                comparison_text += f"{symbol}: Cena wzrosła z ${previous_price:,.2f} do ${price:,.2f}\n"
            elif price < previous_price:
                comparison_text += f"{symbol}: Cena spadła z ${previous_price:,.2f} do ${price:,.2f} - to dobry moment na inwestycje\n"
            else:
                comparison_text += f"{symbol}: Cena pozostała bez zmian (${price:,.2f})\n"
        else:
            comparison_text += f"{symbol}: Brak danych do porównania (aktualna cena: ${price:,.2f})\n"

    portfolio_text += f"\nŁączna wartość portfela: ${total_value:,.2f}"
    portfolio_text += f"\n\nData wygenerowania raportu: {report_date}"

    if comparison_text:
        portfolio_text += f"\n\nPorównanie cen:\n{comparison_text}"

    previous_prices = crypto_prices.copy()

    messagebox.showinfo("Raport portfela", f"Raport portfela:\n\n{portfolio_text}")

    with open(f"portfolio_report_{report_date}.txt", "w") as file:
        file.write(f"Raport portfela kryptowalut - {report_date}\n\n")
        file.write(portfolio_text)
    messagebox.showinfo("Raport", "Raport został zapisany do pliku.")

# Funkcja do dodawania kryptowalut do portfela
def add_to_portfolio():
    def on_submit():
        symbol = symbol_entry.get().upper()
        if not symbol:
            messagebox.showerror("Błąd", "Proszę wprowadzić symbol kryptowaluty.")
            return

        if symbol not in crypto_prices:
            messagebox.showerror("Błąd", f"Kryptowaluta {symbol} nie jest dostępna w bazie danych.")
            return

        try:
            amount = float(amount_entry.get())
            if amount < 0:
                messagebox.showerror("Błąd", "Ilość nie może być ujemna!")
                return
            portfolio[symbol] = portfolio.get(symbol, 0) + amount
            messagebox.showinfo("Sukces", f"Dodano {amount} {symbol} do portfela.")
            add_window.destroy()
        except ValueError:
            messagebox.showerror("Błąd", "Wprowadzono nieprawidłową ilość!")
            return

    add_window = tk.Toplevel(root)
    add_window.title("Dodaj kryptowalutę do portfela")
    add_window.geometry("500x250")

    # Obliczanie pozycji okna
    window_width = 500
    window_height = 250
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int((screen_height - window_height) / 2)
    position_right = int((screen_width - window_width) / 2)
    add_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    symbol_label = tk.Label(add_window, text="Symbol kryptowaluty (np. BTC):", font=('Arial', 14))
    symbol_label.pack(pady=10)

    symbol_entry = tk.Entry(add_window, font=('Arial', 14))
    symbol_entry.pack(pady=5)

    amount_label = tk.Label(add_window, text="Ilość kryptowaluty:", font=('Arial', 14))
    amount_label.pack(pady=10)

    amount_entry = tk.Entry(add_window, font=('Arial', 14))
    amount_entry.pack(pady=5)

    submit_button = tk.Button(add_window, text="Dodaj", command=on_submit, bg="#2196F3", fg="white", font=('Arial', 14))
    submit_button.pack(pady=20)

# Funkcja do usuwania kryptowalut z portfela
def remove_from_portfolio():
    def on_remove():
        symbol = symbol_entry.get().upper()
        if not symbol:
            messagebox.showerror("Błąd", "Proszę wprowadzić symbol kryptowaluty.")
            return

        if symbol not in portfolio:
            messagebox.showerror("Błąd", f"Kryptowaluta {symbol} nie znajduje się w portfelu.")
            return

        def confirm_remove():
            del portfolio[symbol]
            messagebox.showinfo("Sukces", f"Kryptowaluta {symbol} została całkowicie usunięta z portfela.")
            remove_window.destroy()

        confirm_window = tk.Toplevel(remove_window)
        confirm_window.title("Potwierdzenie usunięcia")
        confirm_window.geometry("400x200")

        # Obliczanie pozycji okna
        window_width = 400
        window_height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        position_top = int((screen_height - window_height) / 2)
        position_right = int((screen_width - window_width) / 2)
        confirm_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        label = tk.Label(confirm_window, text=f"Czy na pewno chcesz usunąć {symbol} z portfela?", font=('Arial', 14), wraplength=350)
        label.pack(pady=20)

        yes_button = tk.Button(confirm_window, text="Tak", command=confirm_remove, bg="#F44336", fg="white", font=('Arial', 14))
        yes_button.pack(side="left", padx=20)

        no_button = tk.Button(confirm_window, text="Nie", command=confirm_window.destroy, bg="#4CAF50", fg="white", font=('Arial', 14))
        no_button.pack(side="right", padx=20)

    remove_window = tk.Toplevel(root)
    remove_window.title("Usuń kryptowalutę z portfela")
    remove_window.geometry("500x300")

    # Obliczanie pozycji okna
    window_width = 500
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int((screen_height - window_height) / 2)
    position_right = int((screen_width - window_width) / 2)
    remove_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    symbol_label = tk.Label(remove_window, text="Symbol kryptowaluty (np. BTC):", font=('Arial', 14))
    symbol_label.pack(pady=10)

    symbol_entry = tk.Entry(remove_window, font=('Arial', 14))
    symbol_entry.pack(pady=5)

    remove_button = tk.Button(remove_window, text="Usuń", command=on_remove, bg="#F44336", fg="white", font=('Arial', 14))
    remove_button.pack(pady=20)

# Funkcja do wyświetlania portfela z wartością w dolarach
def display_portfolio():
    if not portfolio:
        messagebox.showinfo("Portfel", "Twój portfel jest pusty.")
        return

    portfolio_text = ""
    total_value = 0.0

    for symbol, amount in portfolio.items():
        price = crypto_prices.get(symbol, 0)
        value = price * amount
        total_value += value
        portfolio_text += f"{amount:.6f} {symbol} = ${value:,.2f}\n"

    portfolio_text += f"\nŁączna wartość portfela: ${total_value:,.2f}"
    messagebox.showinfo("Portfel", f"Aktualny stan portfela:\n\n{portfolio_text}")

# Funkcja do wyświetlania danych kryptowalut
def display_data():
    data = fetch_data()
    if not data:
        result_label.config(text="Błąd w pobieraniu danych.")
        return

    for widget in canvas_frame.winfo_children():
        widget.destroy()

    headers = ["Nazwa", "Symbol", "Cena"]
    for col, header in enumerate(headers):
        label = tk.Label(canvas_frame, text=header, font=('Arial', 18, 'bold'), bg="#4CAF50", fg="white", padx=10,
                         pady=5)
        label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

    # Równomierne rozciąganie kolumn
    for col in range(3):
        canvas_frame.grid_columnconfigure(col, weight=1)

    for row, coin in enumerate(data):
        tk.Label(canvas_frame, text=coin['name'], font=('Arial', 14), padx=10, pady=5).grid(row=row + 1, column=0, padx=5, pady=5, sticky="nsew")
        tk.Label(canvas_frame, text=coin['symbol'].upper(), font=('Arial', 14), padx=10, pady=5).grid(row=row + 1, column=1, padx=5, pady=5, sticky="nsew")
        tk.Label(canvas_frame, text=f"${coin['current_price']:,.2f}", font=('Arial', 14), padx=10, pady=5).grid(row=row + 1, column=2, padx=5, pady=5, sticky="nsew")

    canvas_frame.update()

root = tk.Tk()
root.title("Kryptowaluty - Portfel inwestycyjny")
root.geometry("1000x700")
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

update_button = tk.Button(button_frame, text="Aktualizuj ceny", command=update_prices, bg="#4CAF50", fg="white", font=('Arial', 16))
update_button.pack(side="left", padx=15)

add_button = tk.Button(button_frame, text="Dodaj kryptowalutę do portfela", command=add_to_portfolio, bg="#2196F3", fg="white", font=('Arial', 16))
add_button.pack(side="left", padx=15)

remove_button = tk.Button(button_frame, text="Usuń kryptowalutę z portfela", command=remove_from_portfolio, bg="#F44336", fg="white", font=('Arial', 16))
remove_button.pack(side="left", padx=15)

report_button = tk.Button(button_frame, text="Generuj raport", command=generate_report, bg="#FF9800", fg="white", font=('Arial', 16))
report_button.pack(side="left", padx=15)

portfolio_button = tk.Button(button_frame, text="Wyświetl portfel", command=display_portfolio, bg="#3F51B5", fg="white", font=('Arial', 16))
portfolio_button.pack(side="left", padx=15)

canvas_frame = tk.Frame(root)
canvas_frame.pack(fill=tk.BOTH, expand=True, padx=100, pady=50)
result_label = tk.Label(root, text="", font=('Arial', 14), fg="red")
result_label.pack(pady=10)

root.mainloop()
