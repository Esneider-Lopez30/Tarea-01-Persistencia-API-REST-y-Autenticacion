import flet as ft


def register_screen(page: ft.Page, api_client, ir_a_login):
    email_field = ft.TextField(label="Correo", width=300)
    password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    mensaje = ft.Text(value="")

    def hacer_registro(e):
        if not email_field.value or not password_field.value:
            mensaje.value = "Ingresa correo y contraseña"
            mensaje.color = ft.Colors.RED
            page.update()
            return

        resultado = api_client.registrar(email_field.value, password_field.value)

        if resultado["status"] == 201:
            mensaje.color = ft.Colors.GREEN
            mensaje.value = "Cuenta creada. Ya puedes iniciar sesión."
        else:
            mensaje.color = ft.Colors.RED
            mensaje.value = resultado["data"].get("error", "Error al registrar")
        page.update()

    return ft.Column(
        controls=[
            ft.Text("Crear cuenta", size=24, weight=ft.FontWeight.BOLD),
            email_field,
            password_field,
            mensaje,
            ft.ElevatedButton("Registrarme", on_click=hacer_registro),
            ft.TextButton("¿Ya tienes cuenta? Inicia sesión", on_click=lambda e: ir_a_login()),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
    )