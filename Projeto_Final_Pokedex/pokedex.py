import io, requests, urllib3, mysql.connector, tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PokedexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokédex")
        self.root.geometry("850x500")
        self.id_sel = None
        self.imgs = []

        # --- PARTE ESQUERDA ---
        f_esq = tk.LabelFrame(root, text="Dados", padx=5, pady=5)
        f_esq.place(x=10, y=10, width=280, height=470)

        self.campos = {}
        for c in ["Nome", "Tipo", "Altura", "Peso", "Habilidade", "Ataque", "Defesa"]:
            tk.Label(f_esq, text=c).pack(anchor="w")
            e = tk.Entry(f_esq, width=35)
            e.pack(pady=2)
            self.campos[c] = e

        self.btn_salvar = tk.Button(f_esq, text="Salvar", command=self.salvar)
        self.btn_salvar.pack(fill="x", pady=(10, 4))
        tk.Button(f_esq, text="Limpar", command=self.limpar).pack(fill="x")

        # --- PARTE DIREITA (CARDS) ---
        f_dir = tk.LabelFrame(root, text="Meus Cards Pokémon", padx=5, pady=5)
        f_dir.place(x=300, y=10, width=535, height=470)

        self.cv = tk.Canvas(f_dir, bg="#e9ecef", highlightthickness=0)
        sb = tk.Scrollbar(f_dir, orient="vertical", command=self.cv.yview)
        self.f_cards = tk.Frame(self.cv, bg="#e9ecef")

        self.f_cards.bind("<Configure>", lambda e: self.cv.configure(scrollregion=self.cv.bbox("all")))
        self.cv.create_window((0, 0), window=self.f_cards, anchor="nw")
        self.cv.configure(yscrollcommand=sb.set)

        self.cv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.atualizar()

    def db(self):
        return mysql.connector.connect(user="root", host="localhost", password="", database="pokedex_bd")

    def pegar_foto(self, nome):
        try:
            nome_api = nome.lower().strip().replace(" ", "-")
            url = "/".join(["https://pokeapi.co", "api", "v2", "pokemon", nome_api])
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=8, verify=False)
            if r.status_code == 200:
                dados = r.json()
                return dados["sprites"]["front_default"] or ""
            else:
                messagebox.showwarning("API", f"Pokémon não encontrado (código: {r.status_code})")
        except Exception as e:
            messagebox.showerror("Erro de Rede/API", str(e))
        return ""

    def salvar(self):
        v = [self.campos[c].get().strip() for c in self.campos]
        nome_poke = self.campos["Nome"].get().strip()
        if not nome_poke:
            return messagebox.showwarning("Aviso", "Digite o Nome do Pokémon!")

        img = self.pegar_foto(nome_poke)
        con = self.db()
        cur = con.cursor()
        try:
            if self.id_sel:
                cur.execute("UPDATE pokemon SET nome=%s,tipo=%s,altura=%s,peso=%s,habilidade=%s,ataque=%s,defesa=%s,img=%s WHERE id=%s", (*v, img, self.id_sel))
            else:
                cur.execute("INSERT INTO pokemon (nome,tipo,altura,peso,habilidade,ataque,defesa,img) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (*v, img))
            con.commit()
        except Exception as e:
            messagebox.showerror("Erro no Banco", str(e))
        finally:
            con.close()

        self.limpar()
        self.atualizar()

    def atualizar(self):
        for w in self.f_cards.winfo_children():
            w.destroy()
        self.imgs.clear()

        con = self.db()
        cur = con.cursor()
        cur.execute("SELECT id, nome, tipo, altura, peso, habilidade, ataque, defesa, img FROM pokemon ORDER BY id DESC")

        for i, d in enumerate(cur.fetchall()):
            id_p, nome, tipo, alt, peso, hab, atq, defe, img_url = d

            card = tk.Frame(self.f_cards, bg="white", bd=2, relief="ridge", width=235, height=225)
            card.grid(row=i // 2, column=i % 2, padx=8, pady=8)
            card.pack_propagate(False)

            topo = tk.Frame(card, bg="#343a40")
            topo.pack(fill="x")
            tk.Label(topo, text=nome.upper(), bg="#343a40", fg="white", font=("Arial", 9, "bold")).pack(side="left", padx=6, pady=3)
            tk.Button(topo, text="X", bg="#dc3545", fg="white", font=("Arial", 8, "bold"), bd=0, width=3,
                      command=lambda x=id_p: self.excluir(x)).pack(side="right", padx=3, pady=2)

            box_foto = tk.Frame(card, bg="#f8f9fa", height=85)
            box_foto.pack(fill="x")
            box_foto.pack_propagate(False)

            if img_url:
                try:
                    raw = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=8, verify=False).content
                    pil_img = Image.open(io.BytesIO(raw)).convert("RGBA").resize((80, 80))
                    ft = ImageTk.PhotoImage(pil_img)
                    self.imgs.append(ft)
                    lbl = tk.Label(box_foto, image=ft, bg="#f8f9fa")
                    lbl.image = ft
                    lbl.pack(expand=True)
                except Exception as e:
                    messagebox.showerror("Erro ao baixar foto", str(e))
            else:
                tk.Label(box_foto, text="[Sem Foto na API]", bg="#f8f9fa", fg="gray").pack(expand=True)

            info = tk.Frame(card, bg="white", padx=8, pady=4)
            info.pack(fill="both", expand=True)

            tk.Label(info, text=f"Tipo: {tipo}", bg="white", fg="#0d6efd", font=("Arial", 8, "bold")).pack(anchor="w")
            tk.Label(info, text=f"Habilidade: {hab}", bg="white", font=("Arial", 8)).pack(anchor="w")
            tk.Label(info, text=f"Altura: {alt}  |  Peso: {peso}", bg="white", font=("Arial", 8)).pack(anchor="w")
            tk.Label(info, text=f"Ataque: {atq}  |  Defesa: {defe}", bg="white", fg="#198754", font=("Arial", 8, "bold")).pack(anchor="w")

            tk.Button(card, text="Editar Card", bg="#0d6efd", fg="white", font=("Arial", 8, "bold"), bd=0,
                      command=lambda x=d: self.editar(x)).pack(fill="x", side="bottom", ipady=2)

        con.close()

    def editar(self, d):
        self.limpar()
        id_p, nome, tipo, alt, peso, hab, atq, defe, _ = d
        self.id_sel = id_p
        for c, val in zip(self.campos, [nome, tipo, alt, peso, hab, atq, defe]):
            self.campos[c].insert(0, str(val))
        self.btn_salvar.config(text="Atualizar")

    def excluir(self, id_p):
        if messagebox.askyesno("Excluir", "Deseja apagar este card?"):
            con = self.db()
            cur = con.cursor()
            cur.execute("DELETE FROM pokemon WHERE id=%s", (id_p,))
            con.commit()
            con.close()
            if self.id_sel == id_p:
                self.limpar()
            self.atualizar()

    def limpar(self):
        self.id_sel = None
        for e in self.campos.values():
            e.delete(0, "end")
        self.btn_salvar.config(text="Salvar")

root = tk.Tk()
PokedexApp(root)
root.mainloop()