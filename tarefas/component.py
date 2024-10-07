import flet as ft
from db_config import status, delete, update

class ButtonAddNewTask(ft.FloatingActionButton):
    def __init__(self, add_click) -> None:
        super().__init__()

        self.icon=ft.icons.ADD
        self.on_click=add_click
        self.tooltip="Adicionar uma terefa"
        self.bgcolor="#031954"
        self.foreground_color=ft.colors.WHITE


class NewTask(ft.TextField):
    def __init__(self):
        super().__init__()

        self.expand=True
        self.bgcolor="#d4e1f9"
        self.color="#000000"
        self.border_color=ft.colors.BLUE
        self.hint_text="O que precisa ser feito?"
        self.text_style=ft.TextStyle(weight="Bold")


class Filter(ft.Tabs):
    def __init__(self, fnc_tabs_changed):
        super().__init__()    
        
        self.selected_index=0
        self.on_change=fnc_tabs_changed
        self.tabs=[
            ft.Tab(text="Ativa"), 
            ft.Tab(text="Completada")
        ]
        self.label_color=ft.colors.YELLOW
        self.divider_color="#5271bf"
        self.indicator_color=ft.colors.WHITE
        self.unselected_label_color="#031954"


class CustomSnackBar(ft.SnackBar):
    def __init__(self):
        super().__init__(self)    

        self.content=ft.Text("Escreva uma nova tarefa!", size=16, color=ft.colors.WHITE)
        self.bgcolor="#630a4a"
        self.action="Fechar"
        self.action_color=ft.colors.WHITE


class CustomCard(ft.Card):
    def __init__(self, id: int, txt_title: str, txt_time: str, status: int, todo_instance):
        super().__init__()

        self.id = id
        self.text_title = txt_title
        self.data = bool(status)
        self.status = bool(status)
        self.todo_instance = todo_instance


        self.list_tile=ft.Column(
            spacing=0,
            controls=[
                ft.ListTile(
                    leading=ft.Checkbox(value=self.status, on_change=self.status_change, active_color=ft.colors.GREEN),
                    title=ft.Text(txt_title, size=14, color="#ffffff"),
                    subtitle=ft.Text(txt_time, size=12, color="#000000"),
                    trailing=ft.PopupMenuButton(
                        tooltip="Menu de opções",
                        icon_color=ft.colors.YELLOW,
                        icon_size=30,
                        items=[
                            ft.PopupMenuItem(icon=ft.icons.UPDATE, text="Editar", on_click=self.show_edit_task),
                            ft.PopupMenuItem(icon=ft.icons.DELETE, text="Excluir", on_click=self.delete_task),
                        ]
                    ),
                    bgcolor=ft.colors.BLUE,
                    shape=ft.RoundedRectangleBorder(10),
                    visible=True
                ),
            ]  
        )

        self.text_field_edit=ft.TextField(
            expand=True,
            bgcolor=ft.colors.LIME_200,
            color="#000000",
            value=self.text_title,
            text_style=ft.TextStyle(weight="Bold"),
        )

        self.edit_row=ft.Container(
            bgcolor="#3350a1",
            content=ft.Row(
                visible=False,
                spacing=10,
                controls=[
                    self.text_field_edit,

                    ft.IconButton(
                        icon=ft.icons.DONE_OUTLINE_OUTLINED,
                        icon_color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREEN_500,
                        tooltip="Atualizar tarefa",
                        on_click=self.show_edit_task,
                    ),
                ]
            )
        )

        self.content=ft.Container(
            content=ft.Column(
                spacing=0,
                controls=[
                    self.list_tile,
                    self.edit_row
                ]
            )
        )


    def status_change(self, e) -> None:
        status(self.id, 1 if e.data == 'true' else 0)
        self.todo_instance.load_data()
        self.todo_instance.update()
        self.todo_instance.update_appbar_counts(self.todo_instance.page)


    def delete_task(self, e) -> None:
        delete(self.id)
        self.todo_instance.load_data()
        self.todo_instance.update_appbar_counts(self.todo_instance.page)
        self.todo_instance.update()


    def show_edit_task(self, e) -> None:
        if self.list_tile.visible:
            self.list_tile.visible = False
            self.edit_row.content.visible = True
        else:
            self.list_tile.visible = True
            self.edit_row.content.visible = False
            update(self.id, self.text_field_edit.value)
            self.todo_instance.load_data()
            
        self.todo_instance.update()