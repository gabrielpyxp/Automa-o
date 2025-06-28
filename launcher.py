import os
import subprocess
import tkinter as tk
from tkinter import messagebox

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.txt")

def salvar_datas():
    d1 = entry_data_de.get().strip()
    d2 = entry_data_ate.get().strip()
    if not d1 or not d2:
        messagebox.showerror("Erro", "Preencha as duas datas antes de salvar.")
        return
    with open(CONFIG_FILE, "w") as f:
        f.write(f"{d1}\n{d2}")
    messagebox.showinfo("✅ Datas salvas", f"Data Início: {d1}\nData Fim: {d2}")

def executar_sequencia():
    # 1) Zap.py
    messagebox.showinfo("▶️", "Executando zap.py ...")
    ret = subprocess.run(["python", "zap.py"], shell=True)
    if ret.returncode != 0:
        messagebox.showerror("❌ zap.py", f"Erro ao rodar zap.py (code {ret.returncode})")
        return

    # 2) criar_db.py
    messagebox.showinfo("▶️", "Executando criar_db.py ...")
    ret = subprocess.run(["python", "criar_db.py"], shell=True)
    if ret.returncode != 0:
        messagebox.showerror("❌ criar_db.py", f"Erro ao rodar criar_db.py (code {ret.returncode})")
        return

    # 3) app.py
    messagebox.showinfo("▶️", "Iniciando app.py (Flask)...")
    # abrimos em processo separado para não bloquear a janela
    subprocess.Popen(["python", "app.py"], shell=True)
    messagebox.showinfo("✅ Pronto", "Flask rodando em http://127.0.0.1:5000")

# === GUI ===
root = tk.Tk()
root.title("Launcher Automação Onitel")
root.geometry("360x200")

tk.Label(root, text="Data Início (DD/MM/AAAA):").pack(pady=(10,0))
entry_data_de = tk.Entry(root, width=20)
entry_data_de.pack(pady=5)

tk.Label(root, text="Data Fim (DD/MM/AAAA):").pack()
entry_data_ate = tk.Entry(root, width=20)
entry_data_ate.pack(pady=5)

tk.Button(root, text="💾 Salvar Datas", command=salvar_datas, bg="#4CAF50", fg="white").pack(pady=(10,2))
tk.Button(root, text="▶️ Iniciar Automação", command=executar_sequencia, bg="#2196F3", fg="white").pack(pady=2)
tk.Button(root, text="❌ Fechar", command=root.destroy, bg="#f44336", fg="white").pack(pady=10)

root.mainloop()
