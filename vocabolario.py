import tkinter as tk
import pandas as pd
import random
import os

# ===== CONFIG =====
CARTELLA_VOCABOLI = "data"
FILE_CSV = os.path.join(CARTELLA_VOCABOLI, "vocabolario.csv")

if not os.path.exists(FILE_CSV):
    raise Exception("File vocaboli.csv non trovato!")

# ===== APP =====
class VocabTrainer:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#f5e9c4")
        self.root.title("Allenatore di vocabolario")
        self.root.geometry("900x500")
        self.root.resizable(False, False)

        self.df = pd.read_csv(FILE_CSV, sep=":")

        # Score
        self.punteggio = 0
        self.totale = 0
        self.mostra_pulsanti = False

        # Left frame
        self.frame_left = tk.Frame(root, bg=self.root["bg"])
        self.frame_left.pack(side="left", expand=True, fill="both", padx=20)

        self.label_domanda = tk.Label(self.frame_left, text="", font=("Arial", 18),
                                      bg=self.root["bg"])
        self.label_domanda.pack(pady=20)

        self.entry = tk.Entry(self.frame_left, font=("Arial", 18), justify="center")
        self.entry.pack()

        self.label_risultato = tk.Label(self.frame_left, text="", font=("Arial", 14),
                                        bg=self.root["bg"])
        self.label_risultato.pack(pady=10)

        self.label_score = tk.Label(self.frame_left, text="", font=("Arial", 13),
                                    bg=self.root["bg"])
        self.label_score.pack(pady=5)

        # Buttons below
        self.frame_bottoni = tk.Frame(self.frame_left, bg=self.root["bg"])

        self.btn_riprova = tk.Button(self.frame_bottoni, text="Riprova",
                                     width=12, command=self.riprova)

        self.btn_ok = tk.Button(self.frame_bottoni, text="Avanti",
                                width=12, command=self.nuova_parola)

        self.btn_riprova.pack(side="left", padx=10)
        self.btn_ok.pack(side="right", padx=10)

        self.frame_bottoni.pack_forget()

        self.btn_esci = tk.Button(self.frame_left, text="Esci",
                                  width=10, command=root.quit)
        self.btn_esci.pack(side="bottom", pady=10)

        # Bind keys
        self.entry.bind("<Return>", self.controlla)
        self.entry.bind("<space>", self.space_press)

        # Right panel (settings)
        self.frame_right = tk.Frame(root, bg="#f5e9c4")
        self.frame_right.pack(side="right", fill="y", padx=10)

        tk.Label(self.frame_right, text="Direzione:", font=("Arial", 14, "bold"),
                 bg="#f5e9c4").pack(pady=10)

        self.mod_ita_fr = tk.BooleanVar(value=True)
        self.mod_fr_ita = tk.BooleanVar(value=False)

        tk.Checkbutton(self.frame_right, text="Italiano → Francese",
                       variable=self.mod_ita_fr, bg="#f5e9c4").pack(anchor="w")
        tk.Checkbutton(self.frame_right, text="Francese → Italiano",
                       variable=self.mod_fr_ita, bg="#f5e9c4").pack(anchor="w")

        self.nuova_parola()

    def nuova_parola(self):
        self.mostra_pulsanti = False
        self.frame_bottoni.pack_forget()

        # Pick random vocab line
        self.indice = random.randint(0, len(self.df) - 1)
        self.parola_ita = str(self.df.iloc[self.indice, 0]).strip()
        self.parola_fr = str(self.df.iloc[self.indice, 1]).strip()

        # Determine direction
        self.da_ita_a_fr = True
        if not self.mod_ita_fr.get() and self.mod_fr_ita.get():
            self.da_ita_a_fr = False
        elif self.mod_ita_fr.get() and self.mod_fr_ita.get():
            self.da_ita_a_fr = random.choice([True, False])

        # Update question
        if self.da_ita_a_fr:
            self.domanda = self.parola_ita
            self.risposta_corretta = self.parola_fr
            self.label_domanda.config(text=f"Traduci in francese:\n\n{self.parola_ita}")
        else:
            self.domanda = self.parola_fr
            self.risposta_corretta = self.parola_ita
            self.label_domanda.config(text=f"Traduci in italiano:\n\n{self.parola_fr}")

        self.label_risultato.config(text="")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.aggiorna_score()

    def controlla(self, event):
        if self.mostra_pulsanti:
            self.nuova_parola()
            return

        risposta = self.entry.get().strip()

        self.totale += 1

        if risposta.lower() == self.risposta_corretta.lower():
            self.punteggio += 1
            self.label_risultato.config(text="✅ Corretto!", fg="green")
        else:
            self.label_risultato.config(
                text=f"❌ Sbagliato!\nCorretto: {self.risposta_corretta}",
                fg="red"
            )

        self.aggiorna_score()
        self.mostra_bottoni()

    def aggiorna_score(self):
        percent = (self.punteggio / self.totale * 100) if self.totale > 0 else 0
        self.label_score.config(
            text=f"Punteggio: {self.punteggio} / {self.totale}  ({percent:.1f}%)"
        )

    def mostra_bottoni(self):
        self.mostra_pulsanti = True
        self.frame_bottoni.pack(pady=20)

    def riprova(self):
        self.mostra_pulsanti = False
        self.frame_bottoni.pack_forget()
        self.label_risultato.config(text="")
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def space_press(self, event):
        if self.mostra_pulsanti:
            self.riprova()


root = tk.Tk()
app = VocabTrainer(root)
root.mainloop()
