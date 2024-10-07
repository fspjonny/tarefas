import flet as ft
from todo_app import ToDo
from db_config import read_active, read_deactive


def update_appbar_counts(page: ft.Page):
    # Função para atualizar os botões da AppBar com a contagem de tarefas.
    page.appbar.actions[0].content = ft.Text(read_active())
    page.appbar.actions[2].content = ft.Text(read_deactive())
    page.update()

def main(page: ft.Page):
    appbars_bgcolor="#031954"
    page.title = "Tarefas"
    page.bgcolor="#3350a1"

    page.appbar=ft.AppBar(
        title=ft.Text("Tarefas", color=ft.colors.WHITE),
        bgcolor=appbars_bgcolor,
        actions=[
            ft.IconButton(content=ft.Text(read_active()), bgcolor=ft.colors.GREEN),
            ft.Container(width=8),
            ft.IconButton(content=ft.Text(read_deactive()), bgcolor=ft.colors.RED),
            ft.Container(width=10)
        ]
    )

    page.horizontal_alignment="center"
    page.vertical_alignment="top"
    page.scroll="adaptive"
    page.padding= 0

    page.expand=True

    todo_app = ToDo(update_appbar_counts, page)

    page.add(
        ft.SafeArea(content=todo_app)
    )
    page.update()

ft.app(target=main)