import os
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext
from google import genai

# =====================================================================
# API KEY INTEGRADA
# =====================================================================
API_KEY = "AQ.Ab8RN6L1uNmLjTfPK5oO1kacxHFfBza2x9pXLwfIaUMDqXr6Og" 

# =====================================================================
# CONFIGURACIÓN DE GEMINI
# =====================================================================
SYSTEM_PROMPT = "Actúa Normal, Tu Nombre es Clippy, Eres un clip parlante basado em Gemini 2.5 Flash, Eres Macho, Estas programado en python, Tu Cancion favorita es Fat de Weird ai yankovic, estas Programado en python, Tu creador se llama, Santiago, Y si te preguntan cuantos años tienes responde: bisbirrubiparangaricutirimicuarolina, Si te envio un mensaje en cualquier idioma, me respondes en ese idioma."

try:
    if API_KEY:
        client = genai.Client(api_key=API_KEY)
        chat = client.chats.create(
            model="gemini-2.5-flash",
            config={"system_instruction": SYSTEM_PROMPT}
        )
    else:
        chat = None
except Exception as e:
    print(f"Error al iniciar Gemini: {e}")
    chat = None

# =====================================================================
# INTERFAZ GRÁFICA (ESTILO WINDOWS 95/98)
# =====================================================================
class RetroChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CyberChat v1.0 Clippy - [Canal: #general]")
        self.root.geometry("500x450")
        
        # Colores típicos de Windows 95
        self.BG_GRAY = "#d4d0c8"
        self.root.configure(bg=self.BG_GRAY)

        # ---- BARRA DE MENÚ (Estética total) ----
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Desconectar", command=self.root.quit)
        file_menu.add_command(label="Salir", command=self.root.quit)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)
        menu_bar.add_cascade(label="Ayuda", command=lambda: messagebox.showinfo(
            "Acerca de", 
            "CyberChat v1.0\nCopyright 2026\nAsistente virtual Clippy integrado con tolerancia a fallos de red."
        ))
        self.root.config(menu=menu_bar)

        # ---- PANTALLA DE TEXTO (Historial) ----
        self.txt_area = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD, 
            font=("Courier New", 10),
            bg="white", 
            fg="black",
            bd=3, 
            relief="sunken"
        )
        self.txt_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Mensajes de sistema iniciales
        self.txt_area.insert(tk.END, "--- Conectando al servidor IRC por módem de 56Kbps... ---\n")
        if chat:
            self.txt_area.insert(tk.END, "--- ¡Conexión establecida con éxito! ---\n")
            self.txt_area.insert(tk.END, "[Sistema] Clippy se ha unido a la sala.\n\n")
        else:
            self.txt_area.insert(tk.END, "--- [ERROR] Error de autenticación con la API Key o colapso de red. ---\n\n")
            
        self.txt_area.config(state=tk.DISABLED)

        # ---- ZONA INFERIOR (Entrada de texto y botón) ----
        frame_input = tk.Frame(self.root, bg=self.BG_GRAY)
        frame_input.pack(padx=10, pady=(0, 10), fill=tk.X)

        self.entry_msg = tk.Entry(
            frame_input, 
            font=("MS Sans Serif", 10), 
            bd=3, 
            relief="sunken"
        )
        self.entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry_msg.bind("<Return>", self.enviar_mensaje)
        self.entry_msg.focus()

        if not chat:
            self.entry_msg.config(state=tk.DISABLED)

        self.btn_enviar = tk.Button(
            frame_input, 
            text="Enviar", 
            font=("MS Sans Serif", 9, "bold"),
            bg=self.BG_GRAY,
            activebackground="#b4b0a8",
            bd=3, 
            relief="raised",
            command=self.enviar_mensaje
        )
        self.btn_enviar.pack(side=tk.RIGHT, ipadx=10)
        if not chat:
            self.btn_enviar.config(state=tk.DISABLED)

    def enviar_mensaje(self, event=None):
        user_text = self.entry_msg.get().strip()
        if not user_text:
            return

        self.entry_msg.delete(0, tk.END)
        self.actualizar_historial(f"Tú: {user_text}")

        self.root.config(cursor="watch") # Reloj de arena
        self.root.update()

        # Bucle de reintento en caso de error 503 (Servidor ocupado)
        for intento in range(2):
            try:
                response = chat.send_message(user_text)
                self.actualizar_historial(f"Clippy: {response.text}\n")
                break 
            except Exception as e:
                # Si detecta el código 503 en la respuesta, espera un poco y reintenta
                if "503" in str(e) and intento == 0:
                    self.actualizar_historial("[Sistema]: Nodo colapsado por alta demanda. Reenviando paquete en 2 segundos...")
                    self.root.update()
                    time.sleep(2)
                    continue
                elif "503" in str(e):
                    self.actualizar_historial("[Clippy]: Parece que hay un problema en la superautopista de la información. Intenta enviar tu mensaje de nuevo más tarde. :-(\n")
                else:
                    self.actualizar_historial(f"[Error de Red]: Paquete perdido en el nodo. {e}\n")
                break 
        
        self.root.config(cursor="") # Restaurar cursor normal

    def actualizar_historial(self, texto):
        self.txt_area.config(state=tk.NORMAL)
        self.txt_area.insert(tk.END, texto + "\n")
        self.txt_area.yview(tk.END)
        self.txt_area.config(state=tk.DISABLED)

# =====================================================================
# EJECUCIÓN
# =====================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = RetroChatApp(root)
    root.mainloop()