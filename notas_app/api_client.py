import httpx
from config import API_BASE_URL


class ApiClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.token = None  # se guarda aquí después de un login exitoso

    def _headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    def registrar(self, email: str, password: str) -> dict:
        resp = httpx.post(
            f"{self.base_url}/register",
            json={"email": email, "password": password}
        )
        return {"status": resp.status_code, "data": resp.json()}

    def login(self, email: str, password: str) -> dict:
        resp = httpx.post(
            f"{self.base_url}/login",
            json={"email": email, "password": password}
        )
        data = resp.json()
        if resp.status_code == 200:
            self.token = data["access_token"]
        return {"status": resp.status_code, "data": data}

    def listar_notas(self) -> dict:
        resp = httpx.get(f"{self.base_url}/notas", headers=self._headers())
        return {"status": resp.status_code, "data": resp.json()}

    def crear_nota(self, titulo: str, contenido: str) -> dict:
        resp = httpx.post(
            f"{self.base_url}/notas",
            json={"titulo": titulo, "contenido": contenido},
            headers=self._headers()
        )
        return {"status": resp.status_code, "data": resp.json()}

    def actualizar_nota(self, nota_id: int, titulo: str, contenido: str) -> dict:
        resp = httpx.put(
            f"{self.base_url}/notas/{nota_id}",
            json={"titulo": titulo, "contenido": contenido},
            headers=self._headers()
        )
        return {"status": resp.status_code, "data": resp.json()}

    def eliminar_nota(self, nota_id: int) -> dict:
        resp = httpx.delete(f"{self.base_url}/notas/{nota_id}", headers=self._headers())
        return {"status": resp.status_code, "data": resp.json()}