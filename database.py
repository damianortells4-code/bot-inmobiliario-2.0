import sqlite3
from datetime import datetime

from config import DB_PATH
from urls import normalizar_url_anuncio

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS anuncios (
    link TEXT PRIMARY KEY,
    titulo TEXT,
    fecha TEXT
)
"""
)

conn.commit()


def anuncio_existente(link: str) -> bool:
    clave = normalizar_url_anuncio(link)
    cursor.execute("SELECT link FROM anuncios WHERE link=?", (clave,))
    return cursor.fetchone() is not None


def guardar_anuncio(link: str, titulo: str) -> None:
    clave = normalizar_url_anuncio(link)
    cursor.execute(
        "INSERT OR IGNORE INTO anuncios VALUES (?, ?, ?)",
        (clave, titulo, datetime.now().isoformat()),
    )
    conn.commit()
