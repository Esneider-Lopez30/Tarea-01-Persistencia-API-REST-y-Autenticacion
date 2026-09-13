import flet as ft


def login_screen(page: ft.Page, api_client, ir_a_notas, ir_a_registro):
    email_field = ft.TextField(label="Correo", width=300)
    password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    mensaje_error = ft.Text(value="", color=ft.Colors.RED)

    def hacer_login(e):
        if not email_field.value or not password_field.value:
            mensaje_error.value = "Ingresa correo y contraseña"
            page.update()
            return

        resultado = api_client.login(email_field.value, password_field.value)

        if resultado["status"] == 200:
            mensaje_error.value = ""
            ir_a_notas()
        else:
            mensaje_error.value = resultado["data"].get("error", "Error al iniciar sesión")
            page.update()

    return ft.Column(
        controls=[
            ft.Text("Iniciar sesión", size=24, weight=ft.FontWeight.BOLD),
            email_field,
            password_field,
            mensaje_error,
            ft.ElevatedButton("Ingresar", on_click=hacer_login),
            ft.TextButton("¿No tienes cuenta? Regístrate", on_click=lambda e: ir_a_registro()),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
    )