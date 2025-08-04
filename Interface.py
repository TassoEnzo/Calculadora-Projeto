import customtkinter as ctk
from Calculavel import Calculavel

valor_atual = ""
expressao = ""
historico = []

expressao_var = None
resultado_var = None
frame_historico = None
historico_box = None
botao_historico = None
historico_visivel = False

def formatar_resultado(valor):
    try:
        texto = str(valor).replace(".", ",")
        if texto.endswith(",0"):
            texto = texto[:-2]
        return texto
    except Exception:
        return "Erro"

def atualizar_display():
    expressao_var.set(expressao + valor_atual)
    resultado_var.set("")

def usar_expressao(expr):
    global expressao, valor_atual, historico_visivel
    expressao = expr.replace(",", ".")
    valor_atual = ""
    atualizar_display()
    frame_historico.place_forget()
    historico_visivel = False

def abrir_historico():
    global historico_visivel
    if historico_visivel:
        frame_historico.place_forget()
        historico_visivel = False
        return
    historico_visivel = True
    historico_box.configure(state="normal")
    historico_box.delete("0.0", "end")
    for expr, res in historico:
        if expr.strip():
            historico_box.insert("end", f"{expr} = {res}\n")
    historico_box.configure(state="disabled")

    frame_historico.place(relx=0.03, rely=0.11, relwidth=0.94, relheight=0.2)
    frame_historico.lift()

def limpar_historico():
    historico.clear()
    historico_box.configure(state="normal")
    historico_box.delete("0.0", "end")
    historico_box.configure(state="disabled")

def clique_geral(event):
    global historico_visivel
    if historico_visivel:
        widget = event.widget
        while widget:
            if widget in (frame_historico, botao_historico):
                return
            widget = widget.master
        frame_historico.place_forget()
        historico_visivel = False

def adicionar_digito(digito):
    global valor_atual
    valor_atual += str(digito)
    atualizar_display()

def tecla_pressionada(event):
    if historico_visivel:
        return
    if event.char.isdigit():
        adicionar_digito(event.char)
    elif event.char in [",", "."]:
        adicionar_virgula()

def adicionar_virgula():
    global valor_atual
    if "," not in valor_atual and "." not in valor_atual:
        valor_atual += ","
        atualizar_display()

def adicionar_operador(operador):
    global valor_atual, expressao
    if valor_atual:
        expressao += valor_atual.replace(",", ".") + operador
        valor_atual = ""
    elif expressao:
        expressao += operador
    atualizar_display()

def salvar_historico():
    historico.append((expressao_var.get(), resultado_var.get()))

def calcular_raiz():
    global valor_atual
    if valor_atual:
        numero = float(valor_atual.replace(",", "."))
        resultado = Calculavel.raiz_quadrada(numero)
        expressao_var.set(f"√({valor_atual})")
        resultado_var.set(formatar_resultado(resultado))
        valor_atual = ""
        salvar_historico()

def calcular_reciproco():
    global valor_atual
    if valor_atual:
        try:
            numero = float(valor_atual.replace(",", "."))
            resultado = Calculavel.reciproco(numero)
            expressao_var.set(f"1/({valor_atual})")
            resultado_var.set(formatar_resultado(resultado))
        except ZeroDivisionError:
            expressao_var.set("")
            resultado_var.set("Erro: divisão por zero")
        valor_atual = ""
        salvar_historico()

def calcular_porcentagem():
    global expressao, valor_atual
    if not valor_atual:
        return
    try:
        numero = float(valor_atual.replace(",", "."))
        if expressao:
            base = Calculavel.calcular(expressao.rstrip("+-*/"))
            resultado = Calculavel.porcentagem(base, numero)
            expressao_var.set(f"{formatar_resultado(numero)}% de {formatar_resultado(base)}")
        else:
            resultado = round(numero / 100, 6)
            expressao_var.set(f"{formatar_resultado(numero)}%")
        resultado_var.set(formatar_resultado(resultado))
    except Exception as e:
        expressao_var.set("")
        resultado_var.set(f"Erro: {str(e)}")
    finally:
        valor_atual = ""
        expressao = ""
        salvar_historico()

def calcular_exponenciacao():
    global expressao, valor_atual
    if not valor_atual:
        return
    try:
        expoente = float(valor_atual.replace(",", "."))
        if expressao:
            base = Calculavel.calcular(expressao.rstrip("+-*/"))
        else:
            base = float(valor_atual.replace(",", "."))
        resultado = Calculavel.exponenciar(base, expoente)
        expressao_var.set(f"{formatar_resultado(base)}^{formatar_resultado(expoente)}")
        resultado_var.set(formatar_resultado(resultado))
    except Exception as e:
        expressao_var.set("")
        resultado_var.set(f"Erro: {str(e)}")
    finally:
        valor_atual = ""
        expressao = ""
        salvar_historico()

def calcular_total():
    global valor_atual, expressao
    if valor_atual:
        expressao += valor_atual.replace(",", ".")
    resultado = Calculavel.calcular(expressao)
    expressao_var.set(expressao.replace(".", ","))
    resultado_var.set(formatar_resultado(resultado))
    valor_atual = ""
    expressao = ""
    salvar_historico()

def alternar_sinal():
    global valor_atual
    if not valor_atual:
        return
    if valor_atual.startswith("-"):
        valor_atual = valor_atual[1:]
    else:
        valor_atual = "-" + valor_atual
    atualizar_display()

def tecla_pressionada(event):
    if historico_visivel:
        return
    if event.char.isdigit():
        adicionar_digito(event.char)
    elif event.char in [",", "."]:
        adicionar_virgula()
    elif event.char in "+-*/":
        adicionar_operador(event.char)
    elif event.char in "()":
        adicionar_parenteses(event.char)
    elif event.keysym in ("Return", "KP_Enter", "equal"):
        calcular_total()
    elif event.keysym == "BackSpace":
        apagar_ultimo_digito()
    elif event.keysym == "Escape":
        limpar()

def adicionar_parenteses(p):
    global expressao
    expressao += p
    atualizar_display()

def limpar():
    global valor_atual, expressao
    valor_atual = ""
    expressao = ""
    expressao_var.set("")
    resultado_var.set("")

def apagar_ultimo_digito():
    global valor_atual
    if valor_atual:
        valor_atual = valor_atual[:-1]
        atualizar_display()

def criar_janela():
    global expressao_var, resultado_var, frame_historico, historico_box, botao_historico
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = ctk.CTk()
    app.title("Calculadora")
    app.geometry("350x540")
    app.bind("<Key>", tecla_pressionada)
    app.bind("<Button-1>", clique_geral)
    expressao_var = ctk.StringVar()
    resultado_var = ctk.StringVar()
    frame_historico = ctk.CTkFrame(app, width=330, height=110)
    historico_box = ctk.CTkTextbox(frame_historico, height=100, font=("Poppins", 15))
    historico_box.pack(fill="both", expand=True, padx=4, pady=(4, 0))
    historico_box.configure(state="disabled", cursor="hand2")
    historico_box.tag_config("realce", background="#444", foreground="white")

    def selecionar_expressao(event):
        index = historico_box.index(f"@{event.x},{event.y}")
        linha = index.split(".")[0]
        linha_inicio = f"{linha}.0"
        linha_fim = f"{linha}.0 lineend"
        texto_linha = historico_box.get(linha_inicio, linha_fim).strip()
        if "=" in texto_linha and texto_linha.replace("=", "").strip():
            expr = texto_linha.split("=")[0].strip()
            usar_expressao(expr)

    def realcar_linha(event):
        historico_box.tag_remove("realce", "1.0", "end")
        try:
            index = historico_box.index(f"@{event.x},{event.y}")
            linha = index.split(".")[0]
            linha_inicio = f"{linha}.0"
            linha_fim = f"{linha}.0 lineend"
            texto_linha = historico_box.get(linha_inicio, linha_fim).strip()
            if texto_linha:
                historico_box.tag_add("realce", linha_inicio, f"{linha_fim} +1c")
        except:
            pass

    historico_box.bind("<Motion>", realcar_linha)
    historico_box.bind("<Leave>", lambda e: historico_box.tag_remove("realce", "1.0", "end"))
    historico_box.bind("<Button-1>", selecionar_expressao)

    botao_limpar_hist = ctk.CTkButton(
        frame_historico,
        text="🗑",
        font=("Poppins Semibold", 14),
        command=limpar_historico,
        width=28
    )
    botao_limpar_hist.pack(pady=(4, 4), anchor="e", padx=8)

    botao_historico = ctk.CTkButton(
        master=app,
        text="📜 Histórico",
        width=40,
        height=35,
        font=("Segoe UI Semibold", 16),
        corner_radius=8,
        fg_color="#222",
        hover_color="#444",
        text_color="#00ffcc",
        command=abrir_historico
    )
    botao_historico.place(x=230, y=10)

    label_expressao = ctk.CTkLabel(
        app,
        textvariable=expressao_var,
        font=("Poppins Semibold", 20),
        text_color="white",
        anchor="e",
        height=35
    )
    label_expressao.pack(padx=10, pady=(60, 0), fill="x")

    label_resultado = ctk.CTkLabel(
        app,
        textvariable=resultado_var,
        font=("Poppins Semibold", 40),
        text_color="white",
        anchor="e",
        height=45
    )
    label_resultado.pack(padx=10, pady=(0, 5), fill="x")

    frame = ctk.CTkFrame(app)
    frame.pack(padx=10, pady=8, expand=True, fill="both")

    for r in range(6):
        frame.grid_rowconfigure(r, weight=1)
    for c in range(5):
        frame.grid_columnconfigure(c, weight=1)

    botoes = [
        ("%", calcular_porcentagem), ("CE", lambda: usar_expressao(expressao)), ("C", limpar), ("←", apagar_ultimo_digito),
        ("1/x", calcular_reciproco), ("^", calcular_exponenciacao), ("√", calcular_raiz), ("/", lambda: adicionar_operador("/")),
        ("7", lambda: adicionar_digito(7)), ("8", lambda: adicionar_digito(8)), ("9", lambda: adicionar_digito(9)), ("*", lambda: adicionar_operador("*")),
        ("4", lambda: adicionar_digito(4)), ("5", lambda: adicionar_digito(5)), ("6", lambda: adicionar_digito(6)), ("-", lambda: adicionar_operador("-")), 
        ("1", lambda: adicionar_digito(1)), ("2", lambda: adicionar_digito(2)), ("3", lambda: adicionar_digito(3)), ("+", lambda: adicionar_operador("+")),
        ("±", alternar_sinal), ("0", lambda: adicionar_digito(0)), (",", adicionar_virgula), ("=", calcular_total)
    ]

    for i, (texto, comando) in enumerate(botoes):
        if texto == "":
            continue
        linha, coluna = divmod(i, 4)
        botao = ctk.CTkButton(frame, text=texto, font=("Segoe UI", 20), command=comando)
        botao.grid(row=linha, column=coluna, padx=5, pady=5, sticky="nsew")


    app.mainloop()