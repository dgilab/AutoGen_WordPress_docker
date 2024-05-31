import tkinter as tk
from tkinter import ttk
import yaml
import subprocess

class PopupForm(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Formulario Docker Compose")
        self.geometry("500x600")

        self.entries = {}
        self.values = {}

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style(self)
        style.configure('TLabel', background='lightgrey', font=('Arial', 12))
        style.configure('TEntry', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 12), background='lightblue', foreground='black')

        fields = [
            "Nombre del contenedor para MySQL",
            "Nombre del contenedor para Wordpress puerto(8080)",
            "Nombre del contenedor para PhpMyAdmin puerto(8081)",
            "Nombre de usuario para MySQL",
            "Contraseña para el usuario de MySQL",
            "Nombre de la Base de datos",
            "HostName para Wordpress",
            "HostName para PhpMyAdmin"
        ]
        
        for field in fields:
            label = ttk.Label(self, text=field + ":")
            label.pack(pady=5, padx=20, fill='x')
            entry = ttk.Entry(self)
            entry.pack(pady=5, padx=20, fill='x')
            self.entries[field] = entry

        submit_button = ttk.Button(self, text="Enviar", command=self.submit)
        submit_button.pack(pady=15)

    def submit(self):
        self.values['bd'] = self.entries["Nombre del contenedor para MySQL"].get()
        self.values['wordpre'] = self.entries["Nombre del contenedor para Wordpress"].get()
        self.values['php'] = self.entries["Nombre del contenedor para PhpMyAdmin"].get()
        self.values['dbuser'] = self.entries["Nombre de usuario para MySQL"].get()
        self.values['dbpass'] = self.entries["Contraseña para el usuario de MySQL"].get()
        self.values['dbname'] = self.entries["Nombre de la Base de datos"].get()
        self.values['hnps'] = self.entries["HostName para Wordpress"].get()
        self.values['hnphp'] = self.entries["HostName para PhpMyAdmin"].get()

        self.destroy()
        main(self.values)

def main(values):
    bd = values['bd']
    wordpre = values['wordpre']
    php = values['php']
    dbuser = values['dbuser']
    dbpass = values['dbpass']
    dbname = values['dbname']
    hnps = values['hnps']
    hnphp = values['hnphp']

    data = {
        "version": "3",
        "services": {
            wordpre: {
                "image": "wordpress",
                "ports": ["8080:80"],
                "environment": {
                    "WORDPRESS_DB_HOST": bd,
                    "WORDPRESS_DB_USER": dbuser,
                    "WORDPRESS_DB_PASSWORD": dbpass,
                    "WORDPRESS_DB_NAME": dbname
                },
                "volumes": ["wordpress:/var/www/html"],
                "hostname": hnps
            },
            php: {
                "image": "phpmyadmin/phpmyadmin",
                "ports": ["8081:80"],
                "environment": {
                    "PMA_HOST": bd,
                    "MYSQL_ROOT_PASSWORD": dbpass
                },
                "hostname": hnphp
            },
            bd: {
                "image": "mysql:5.7",
                "environment": {
                    "MYSQL_DATABASE": dbname,
                    "MYSQL_USER": dbuser,
                    "MYSQL_PASSWORD": dbpass,
                    "MYSQL_ROOT_PASSWORD": dbpass
                },
                "volumes": ["db_data:/var/lib/mysql"],
            }
        },
        "volumes": {
            "wordpress": {},
            "db_data": {}
        }
    }

    try:
        with open('docker-compose.yml', 'w') as file:
            yaml.dump(data, file, default_flow_style=False, sort_keys=False)
        print("Archivo 'docker-compose.yml' generado con éxito.")
    except Exception as e:
        print(f"Error al generar el archivo YAML: {e}")

    try:
        subprocess.run(["docker-compose", "up", "--build"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar docker-compose: {e}")

if __name__ == "__main__":
    app = PopupForm()
    app.mainloop()