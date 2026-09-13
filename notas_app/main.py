import flet as ft
from api_client import ApiClient
from screens.login_screen import login_screen
from screens.register_screen import register_screen
from screens.notas_screen import notas_screen


def main(page: ft.Page):
    page.title = "Notas"
    page.window.width = 400
    page.window.height = 650

    api_client = ApiClient()

    def mostrar_login():
        page.controls.clear()
        page.add(login_screen(page, api_client, ir_a_notas=mostrar_notas, ir_a_registro=mostrar_registro))
        page.update()

    def mostrar_registro():
        page.controls.clear()
        page.add(register_screen(page, api_client, ir_a_login=mostrar_login))
        page.update()

    def mostrar_notas():
        page.controls.clear()
        page.add(notas_screen(page, api_client, ir_a_login=mostrar_login))
        page.update()

    mostrar_login()


ft.run(main)