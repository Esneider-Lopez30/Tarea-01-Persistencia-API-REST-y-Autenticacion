import sqlite3
from datetime import datetime, timezone

DB_PATH = "notas_local.db"


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # así podemos leer columnas por nombre, no solo por índice
    return conn


def init_db():
    conn = conectar()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id INTEGER,
            titulo TEXT NOT NULL,
            contenido TEXT,
            sincronizado INTEGER NOT NULL DEFAULT 0,
            actualizado_en TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def listar_notas_locales():
    conn = conectar()
    filas = conn.execute("SELECT * FROM notas ORDER BY actualizado_en DESC").fetchall()
    conn.close()
    return [dict(fila) for fila in filas]


def guardar_nota_local(titulo: str, contenido: str, server_id: int = None, sincronizado: bool = False):
    conn = conectar()
    conn.execute(
        "INSERT INTO notas (server_id, titulo, contenido, sincronizado, actualizado_en) VALUES (?, ?, ?, ?, ?)",
        (server_id, titulo, contenido, int(sincronizado), datetime.now(timezone.utc).isoformat())
    )
    conn.commit()
    conn.close()


def actualizar_nota_local(id_local: int, titulo: str, contenido: str, sincronizado: bool = False):
    conn = conectar()
    conn.execute(
        "UPDATE notas SET titulo = ?, contenido = ?, sincronizado = ?, actualizado_en = ? WHERE id = ?",
        (titulo, contenido, int(sincronizado), datetime.now(timezone.utc).isoformat(), id_local)
    )
    conn.commit()
    conn.close()


def eliminar_nota_local(id_local: int):
    conn = conectar()
    conn.execute("DELETE FROM notas WHERE id = ?", (id_local,))
    conn.commit()
    conn.close()


def marcar_sincronizada(id_local: int, server_id: int):
    conn = conectar()
    conn.execute(
        "UPDATE notas SET sincronizado = 1, server_id = ? WHERE id = ?",
        (server_id, id_local)
    )
    conn.commit()
    conn.close()


def notas_pendientes_por_sincronizar():
    conn = conectar()
    filas = conn.execute("SELECT * FROM notas WHERE sincronizado = 0").fetchall()
    conn.close()
    return [dict(fila) for fila in filas]