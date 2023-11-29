import customtkinter as ctk
import tkinter as tk
import sqlite3
 
ctk.set_appearance_mode("System") 


conn = sqlite3.connect('transactions.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value REAL,
        description TEXT,
        type TEXT
    )
''')
conn.commit()

class Transaction:
    def __init__(self, value, description, type, id=None):
        self.id = id
        self.value = value
        self.description = description
        self.type = type

def create_transaction(transaction):
    cursor.execute('''
        INSERT INTO transactions (value, description, type)
        VALUES (?, ?, ?)
    ''', (transaction.value, transaction.description, transaction.type))
    conn.commit()
    print("Transação adicionada")

def read_transaction(id):
    cursor.execute('SELECT * FROM transactions WHERE id = ?', (id))
    transaction = cursor.fetchone()
    if transaction:
        print("Transação:")
        print(transaction)
    else:
        print("Transação não encontrada")

def update_transaction(transaction):
    cursor.execute('''
        UPDATE transactions
        SET value = ?, description = ?, type = ?
        WHERE id = ?
    ''', (transaction.value, transaction.description, transaction.type ,transaction.id))
    conn.commit()
    print("Transacão atualizada com sucesso")

def delete_transaction(id):
    cursor.execute('DELETE FROM transactions WHERE id = ?', (id))
    conn.commit()
    print("Transação deletada com sucesso")

def get_all_transactions():
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    if transactions:
        print("\nLista de Transações:")
        for transaction in transactions:
            print(transaction)
        return transactions
        
    else:
        print("Nenhuma transação encontrada")

class App(ctk.CTk):
    
    def showAll(self):
        transactions = get_all_transactions()
        self.textbox.delete('1.0', 'end')
        for transaction in transactions:
            self.textbox.insert('end', f'{transaction}\n')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        self.title("Sistema de Finanças")
        self.geometry(f"1200x800")
 

        self.valueLabel = ctk.CTkLabel(self,
                                      text="Valor")
        self.valueLabel.grid(row=0, column=0,
                            padx=20, pady=20,
                            sticky="ew")
 

        self.valueEntry = ctk.CTkEntry(self, placeholder_text=0.00)
        self.valueEntry.grid(row=0, column=1,
                            columnspan=3, padx=20,
                            pady=20, sticky="ew")
 

        self.descriptionLabel = ctk.CTkLabel(self,
                                     text="Descrição")
        self.descriptionLabel.grid(row=1, column=0,
                           padx=20, pady=20,
                           sticky="ew")
 

        self.descriptionEntry = ctk.CTkEntry(self,
                            placeholder_text="Descrição")
        self.descriptionEntry.grid(row=1, column=1,
                           columnspan=3, padx=20,
                           pady=20, sticky="ew")
 


        self.typeVar = tk.StringVar(value="Entrada")
        self.typeTransaction = ctk.CTkLabel(self, 
                                    text="Tipo de Transação")
        self.typeTransaction.grid(row=2, column=0, 
                              padx=20, pady=20,
                              sticky="ew")

        

        self.outRadioButton = ctk.CTkRadioButton(self,
                                  text="Saída",
                                  variable=self.typeVar,
                                            value="Saida")
        self.outRadioButton.grid(row=2, column=1, padx=20,
                                  pady=20, sticky="ew")
 
        self.inRadioButton = ctk.CTkRadioButton(self,
                                      text="Entrada",
                                      variable=self.typeVar,
                                      value="Entrada")
        self.inRadioButton.grid(row=2, column=2,
                                    padx=20,
                                    pady=20, sticky="ew")

        self.registerButton = ctk.CTkButton(self,
                                         text="Cadastrar", command=lambda:create_transaction(Transaction(self.valueEntry.get(), self.descriptionEntry.get(), self.typeVar.get())))
        self.registerButton.grid(row=5, column=1,
                                        columnspan=2,
                                        padx=20, pady=20,
                                        sticky="ew")
        
        self.idDeleteLabel = ctk.CTkLabel(self,
                                      text="Id para Deletar")
        self.idDeleteLabel.grid(row=7, column=0,
                            padx=20, pady=20,
                            sticky="ew")
 

        self.idDeleteEntry = ctk.CTkEntry(self, placeholder_text=0)
        self.idDeleteEntry.grid(row=7, column=1,
                            columnspan=3, padx=10,
                            pady=20, sticky="ew")
        self.deleteButton = ctk.CTkButton(self,
                                         text="Deletar", command=lambda:delete_transaction(self.idDeleteEntry.get()))
        self.deleteButton.grid(row=7, column=3,
                                        columnspan=2,
                                        padx=20, pady=20,
                                        sticky="ew")
        
        self.idUpdateLabel = ctk.CTkLabel(self,
                                      text="Id para atualizar, preencha os dados de valor, descrição e tipo")
        self.idUpdateLabel.grid(row=8, column=0,
                            padx=20, pady=20,
                            sticky="ew")
 

        self.idUpdateEntry = ctk.CTkEntry(self, placeholder_text=0)
        self.idUpdateEntry.grid(row=8, column=1,
                            columnspan=3, padx=10,
                            pady=20, sticky="ew")
        self.updateButton = ctk.CTkButton(self,
                                         text="Atualizar",command=lambda:update_transaction(Transaction(self.valueEntry.get(), self.descriptionEntry.get(), self.typeVar.get(), self.idUpdateEntry.get())))
        self.updateButton.grid(row=8, column=3,
                                        columnspan=2,
                                        padx=20, pady=20,
                                        sticky="ew")
        self.textbox = ctk.CTkTextbox(master=self, width=400, corner_radius=0)
        self.textbox.grid(row=9, column=1, sticky="nsew")

        self.getListButton = ctk.CTkButton(self,
                                         text="Listar", command=lambda:self.showAll())
        self.getListButton.grid(row=9, column=2,
                                        columnspan=2,
                                        padx=20, pady=20,
                                        sticky="ew")
        

         
 
if __name__ == "__main__":
    app = App()
    app.mainloop()