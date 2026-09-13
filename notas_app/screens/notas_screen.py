import flet as ft
import httpx
import db_local


def notas_screen(page: ft.Page, api_client, ir_a_login):
    db_local.init_db()

    lista_notas = ft.Column(spacing=10)
    titulo_field = ft.TextField(label="Título", width=300)
    contenido_field = ft.TextField(label="Contenido", width=300, multiline=True)
    estado_sync = ft.Text(value="", size=12)
    estado = {"editando_id": None}

    guardar_button = ft.ElevatedButton("Guardar nota", visible=True)
    actualizar_button = ft.ElevatedButton("Actualizar nota", visible=False)
    cancelar_button = ft.OutlinedButton("Cancelar edición", visible=False)

    def refrescar_lista():
        lista_notas.controls.clear()
        notas = db_local.listar_notas_locales()

        for nota in notas:
            etiqueta = "✅ sincronizada" if nota["sincronizado"] else "⏳ pendiente"
            lista_notas.controls.append(
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(nota["titulo"], weight=ft.FontWeight.BOLD),
                                ft.Text(nota["contenido"] or "", size=12),
                                ft.Text(etiqueta, size=10, color=ft.Colors.GREY),
                            ],
                            expand=True,
                        ),
                        ft.IconButton(icon=ft.Icons.EDIT, data=nota["id"], on_click=editar_click),
                        ft.IconButton(icon=ft.Icons.DELETE, data=nota["id"], on_click=eliminar_click),
                    ]
                )
            )
        page.update()

    def salir_de_edicion():
        estado["editando_id"] = None
        titulo_field.value = ""
        contenido_field.value = ""
        guardar_button.visible = True
        actualizar_button.visible = False
        cancelar_button.visible = False

    def crear_click(e):
        if not titulo_field.value:
            return
        db_local.guardar_nota_local(titulo_field.value, contenido_field.value, sincronizado=False)
        salir_de_edicion()
        refrescar_lista()
        sincronizar(e)

    def actualizar_click(e):
        if not titulo_field.value or estado["editando_id"] is None:
            return
        db_local.actualizar_nota_local(
            estado["editando_id"], titulo_field.value, contenido_field.value, sincronizado=False
        )
        salir_de_edicion()
        refrescar_lista()
        sincronizar(e)

    def editar_click(e):
        nota_id = e.control.data
        nota = next((n for n in db_local.listar_notas_locales() if n["id"] == nota_id), None)
        if not nota:
            return

        titulo_field.value = nota["titulo"]
        contenido_field.value = nota["contenido"]
        estado["editando_id"] = nota_id
        guardar_button.visible = False
        actualizar_button.visible = True
        cancelar_button.visible = True
        page.update()

    def cancelar_click(e):
        salir_de_edicion()
        page.update()

    def eliminar_click(e):
        db_local.eliminar_nota_local(e.control.data)
        refrescar_lista()

    def sincronizar(e):
        pendientes = db_local.notas_pendientes_por_sincronizar()

        if not pendientes:
            estado_sync.value = "Todo sincronizado"
            estado_sync.color = ft.Colors.GREEN
            page.update()
            return

        enviadas = 0
        hubo_error_conexion = False

        for nota in pendientes:
            try:
                if nota["server_id"]:
                    resultado = api_client.actualizar_nota(nota["server_id"], nota["titulo"], nota["contenido"])
                else:
                    resultado = api_client.crear_nota(nota["titulo"], nota["contenido"])
            except httpx.RequestError:
                hubo_error_conexion = True
                break

            if resultado["status"] in (200, 201):
                server_id = nota["server_id"] or resultado["data"].get("id")
                db_local.marcar_sincronizada(nota["id"], server_id)
                enviadas += 1

        if hubo_error_conexion:
            estado_sync.value = "Sin conexión al servidor — quedan notas pendientes por sincronizar"
            estado_sync.color = ft.Colors.ORANGE
        elif enviadas == len(pendientes):
            estado_sync.value = f"Sincronizadas {enviadas} nota(s) con el servidor"
            estado_sync.color = ft.Colors.GREEN
        else:
            estado_sync.value = f"Quedaron {len(pendientes) - enviadas} nota(s) pendientes"
            estado_sync.color = ft.Colors.ORANGE

        page.update()
        refrescar_lista()

    def cerrar_sesion(e):
        api_client.token = None
        ir_a_login()

    guardar_button.on_click = crear_click
    actualizar_button.on_click = actualizar_click
    cancelar_button.on_click = cancelar_click

    refrescar_lista()

    return ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("Mis notas", size=24, weight=ft.FontWeight.BOLD, expand=True),
                    ft.TextButton("Cerrar sesión", on_click=cerrar_sesion),
                ]
            ),
            titulo_field,
            contenido_field,
            ft.Row(
                controls=[guardar_button, actualizar_button, ft.OutlinedButton("Sincronizar ahora", on_click=sincronizar), cancelar_button]
            ),
            estado_sync,
            ft.Divider(),
            lista_notas,
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )