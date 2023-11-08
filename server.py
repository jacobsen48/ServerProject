import argparse
import os
import socket


def parse_args():
    """Funzione per la descrizione che avviene avviando l'app con argomento -h o --help"""
    parser = argparse.ArgumentParser(
        description="Web Server di Alberto Iacobelli mat: 300792"
    )
    parser.add_argument(
        "--base",
        default=".",
        help="Posizione (directory) del sito web",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Porta su cui il server è in ascolto",
    )
    return parser.parse_args()


def gestione_richiesta(socket_c, base_d):
    """Funzione per la gestione della richiesta"""
    dato_richiesto = socket_c.recv(1024).decode("utf-8")
    linea_richiesta = dato_richiesto.split("\n")
    linea_richiesta = linea_richiesta[0]
    metodo, percorso, protocollo = linea_richiesta.strip().split()
    print("metodo:", metodo)
    print("percorso:", percorso)
    print("protocollo:", protocollo)

    if metodo != "GET":
        risposta = "HTTP/1.1 501 non implementato\n\nMetodo non implementato"
    else:
        if percorso == "/":
            percorso = "/index.html"

        percorso_file = os.path.join(base_d, percorso.lstrip("/"))

        if percorso.endswith(".css"):
            # Gestisci i file CSS
            if os.path.exists(percorso_file):
                with open(percorso_file, "rb") as file:
                    contenuto_risposta = file.read()
                risposta = (
                    "HTTP/1.1 200 OK\nContent-Type: text/css\n\n"
                    + contenuto_risposta.decode("utf-8")
                )
            else:
                risposta = "HTTP/1.1 404 Non Trovato\n\nFile CSS non trovato"

        elif percorso.endswith(".js"):
            # Gestisci i file javascript
            if os.path.exists(percorso_file):
                with open(percorso_file, "rb") as file:
                    contenuto_risposta = file.read()
                risposta = (
                    "HTTP/1.1 200 OK\nContent-Type: application/javascript\n\n"
                    + contenuto_risposta.decode("utf-8")
                )
            else:
                risposta = "HTTP/1.1 404 Non Trovato\n\nFile JavaScript non trovato"

        elif percorso.endswith((".jpg", ".jpeg", ".png", ".gif")):
            # Gestisci i file delle immagini
            content_type = (
                "image/jpeg"
                if percorso.endswith((".jpg", ".jpeg"))
                else "image/png"
                if percorso.endswith(".png")
                else "image/gif"
            )

            if os.path.exists(percorso_file):
                with open(percorso_file, "rb") as file:
                    contenuto_risposta = file.read()
                risposta = f"HTTP/1.1 200 OK\nContent-Type: {content_type}\n\n"
                socket_c.send(risposta.encode("utf-8"))
                socket_c.send(contenuto_risposta)
            else:
                risposta = "HTTP/1.1 404 Non trovato\n\nFile immagine non trovato"
                socket_c.send(risposta.encode("utf-8"))

        else:
            if os.path.exists(percorso_file):
                with open(percorso_file, "rb") as file:
                    contenuto_risposta = file.read()
                risposta = (
                    "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
                    + contenuto_risposta.decode("utf-8")
                )
            else:
                risposta = "HTTP/1.1 404 Non trovato\n\nFile non trovato"

        socket_c.send(risposta.encode("utf-8"))
        socket_c.close()


def main():
    """Definizione della funzione main"""
    args = parse_args()
    base_directory = args.base
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", args.port))
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.listen(1)

    print(f"Server in ascolto su http//127.0.0.1:{args.port}/")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connessione da: {client_address}")
        gestione_richiesta(client_socket, base_directory)


if __name__ == "__main__":
    main()
