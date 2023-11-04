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


if __name__ == "__main__":
    args = parse_args()
    print("Questa è una prova del parser")
