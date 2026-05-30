import tkinter as tk
from tkinter import ttk, messagebox
import random

class SimulatoreInvestimenti:
    def __init__(self):
        self.saldo = 10000.0
        self.portafoglio = {}
        
        self.azioni = {
            "AAPL": {"nome": "Apple", "prezzo": 210.50, "settore": "Tech"},
            "TSLA": {"nome": "Tesla", "prezzo": 245.80, "settore": "Auto"},
            "ENI": {"nome": "Eni", "prezzo": 14.25, "settore": "Energia"},
            "RACE": {"nome": "Ferrari", "prezzo": 415.70, "settore": "Auto"},
            "ISP": {"nome": "Intesa Sanpaolo", "prezzo": 3.85, "settore": "Banche"},
            "TIT": {"nome": "Telecom Italia", "prezzo": 2.45, "settore": "Telecom"}
        }
        
    def aggiorna_prezzi(self):
        for ticker in self.azioni:
            variazione = random.uniform(-4, 4)
            self.azioni[ticker]["prezzo"] *= (1 + variazione / 100)
            self.azioni[ticker]["prezzo"] = round(self.azioni[ticker]["prezzo"], 2)

    def compra(self, ticker, quantita):
        if ticker not in self.azioni:
            return False
        costo = self.azioni[ticker]["prezzo"] * quantita
        if costo > self.saldo:
            return False
        self.saldo -= costo
        self.portafoglio[ticker] = self.portafoglio.get(ticker, 0) + quantita
        return True

    def vendi(self, ticker, quantita):
        if ticker not in self.portafoglio or self.portafoglio[ticker] < quantita:
            return False
        ricavo = self.azioni[ticker]["prezzo"] * quantita
        self.saldo += ricavo
        self.portafoglio[ticker] -= quantita
        if self.portafoglio[ticker] == 0:
            del self.portafoglio[ticker]
        return True


# ====================== FUNZIONI FINESTRE ======================

def apri_finestra_compra(sim, saldo_label, aggiorna_tabella):
    win = tk.Toplevel()
    win.title("Compra Azioni")
    win.geometry("400x280")
    
    tk.Label(win, text="Seleziona Azione:", font=("Arial", 11, "bold")).pack(pady=10)
    
    ticker_var = tk.StringVar()
    combo = ttk.Combobox(win, textvariable=ticker_var, values=list(sim.azioni.keys()), state="readonly", width=30)
    combo.pack(pady=5)
    combo.current(0)
    
    tk.Label(win, text="Quantità da acquistare:", font=("Arial", 11)).pack(pady=5)
    qty_var = tk.IntVar(value=1)
    tk.Entry(win, textvariable=qty_var, width=15).pack(pady=5)
    
    def conferma():
        try:
            ticker = ticker_var.get()
            qty = qty_var.get()
            if qty < 1:
                raise ValueError
            if sim.compra(ticker, qty):
                messagebox.showinfo("✅ Successo", f"Hai comprato {qty} azioni di {ticker}!")
                saldo_label.config(text=f"Saldo disponibile: € {sim.saldo:,.2f}")
                aggiorna_tabella()
            else:
                messagebox.showerror("❌ Errore", "Saldo insufficiente!")
        except:
            messagebox.showerror("❌ Errore", "Inserisci una quantità valida!")
        win.destroy()
    
    tk.Button(win, text="Conferma Acquisto", command=conferma, bg="#4CAF50", fg="white", height=2).pack(pady=15)


def apri_finestra_vendi(sim, saldo_label, aggiorna_tabella):
    if not sim.portafoglio:
        messagebox.showwarning("Attenzione", "Non possiedi ancora azioni!")
        return
    
    win = tk.Toplevel()
    win.title("Vendi Azioni")
    win.geometry("400x280")
    
    tk.Label(win, text="Seleziona Azione da Vendere:", font=("Arial", 11, "bold")).pack(pady=10)
    
    ticker_var = tk.StringVar()
    combo = ttk.Combobox(win, textvariable=ticker_var, values=list(sim.portafoglio.keys()), state="readonly", width=30)
    combo.pack(pady=5)
    combo.current(0)
    
    tk.Label(win, text="Quantità da vendere:", font=("Arial", 11)).pack(pady=5)
    qty_var = tk.IntVar(value=1)
    tk.Entry(win, textvariable=qty_var, width=15).pack(pady=5)
    
    def conferma():
        try:
            ticker = ticker_var.get()
            qty = qty_var.get()
            if qty < 1:
                raise ValueError
            if sim.vendi(ticker, qty):
                messagebox.showinfo("✅ Successo", f"Hai venduto {qty} azioni di {ticker}!")
                saldo_label.config(text=f"Saldo disponibile: € {sim.saldo:,.2f}")
                aggiorna_tabella()
            else:
                messagebox.showerror("❌ Errore", "Quantità non valida!")
        except:
            messagebox.showerror("❌ Errore", "Inserisci una quantità valida!")
        win.destroy()
    
    tk.Button(win, text="Conferma Vendita", command=conferma, bg="#f44336", fg="white", height=2).pack(pady=15)


def mostra_portafoglio(sim):
    if not sim.portafoglio:
        messagebox.showinfo("Portafoglio", "Non possiedi ancora nessuna azione.")
        return
    
    testo = "=== IL TUO PORTAFOGLIO ===\n\n"
    valore_totale = 0.0
    
    for ticker, qty in sim.portafoglio.items():
        prezzo = sim.azioni[ticker]["prezzo"]
        valore = prezzo * qty
        valore_totale += valore
        testo += f"• {ticker} - {sim.azioni[ticker]['nome']}\n"
        testo += f"   {qty} azioni × €{prezzo:.2f} = €{valore:.2f}\n\n"
    
    testo += f"Valore Portafoglio: €{valore_totale:.2f}\n"
    testo += f"Saldo Liquido: €{sim.saldo:.2f}\n"
    testo += f"Patrimonio Totale: €{sim.saldo + valore_totale:.2f}"
    
    messagebox.showinfo("Il tuo Portafoglio", testo)


# ====================== INTERFACCIA PRINCIPALE ======================

def crea_interfaccia():
    sim = SimulatoreInvestimenti()
    root = tk.Tk()
    root.title("Simulatore Investimenti - €")
    root.geometry("950x680")
    
    tk.Label(root, text="Simulatore di Investimenti", font=("Arial", 18, "bold")).pack(pady=10)
    
    saldo_label = tk.Label(root, text=f"Saldo disponibile: € {sim.saldo:,.2f}", 
                          font=("Arial", 14, "bold"), fg="green")
    saldo_label.pack(pady=8)
    
    tk.Label(root, text="Azioni disponibili", font=("Arial", 12, "bold")).pack(pady=(15,5))
    
    tree = ttk.Treeview(root, columns=("Ticker", "Nome", "Prezzo", "Settore"), show="headings", height=8)
    tree.heading("Ticker", text="Ticker")
    tree.heading("Nome", text="Nome")
    tree.heading("Prezzo", text="Prezzo €")
    tree.heading("Settore", text="Settore")
    tree.pack(pady=10, padx=30, fill="x")
    
    def aggiorna_tabella():
        for item in tree.get_children():
            tree.delete(item)
        for ticker, dati in sim.azioni.items():
            tree.insert("", "end", values=(ticker, dati["nome"], f"{dati['prezzo']:.2f}", dati["settore"]))
    
    aggiorna_tabella()
    
    # Pulsanti
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=20)
    
    tk.Button(btn_frame, text="Simula Nuova Giornata", command=lambda: [sim.aggiorna_prezzi(), aggiorna_tabella(), saldo_label.config(text=f"Saldo disponibile: € {sim.saldo:,.2f}")],
              bg="#4CAF50", fg="white", width=22, height=2).grid(row=0, column=0, padx=6)
    
    tk.Button(btn_frame, text="Compra", command=lambda: apri_finestra_compra(sim, saldo_label, aggiorna_tabella),
              bg="#2196F3", fg="white", width=15, height=2).grid(row=0, column=1, padx=6)
    
    tk.Button(btn_frame, text="Vendi", command=lambda: apri_finestra_vendi(sim, saldo_label, aggiorna_tabella),
              bg="#f44336", fg="white", width=15, height=2).grid(row=0, column=2, padx=6)
    
    tk.Button(btn_frame, text="Mostra Portafoglio", command=lambda: mostra_portafoglio(sim),
              bg="#9C27B0", fg="white", width=18, height=2).grid(row=0, column=3, padx=6)
    
    tk.Button(root, text="Esci", command=root.quit, width=15, height=1).pack(pady=20)
    
    root.mainloop()


if __name__ == "__main__":
    crea_interfaccia()