import flet as ft
from component import CustomCard, Filter, NewTask, ButtonAddNewTask, CustomSnackBar
from db_config import create, read

class ToDo(ft.Container):

    def __init__(self, update_appbar_counts, page: ft.Page) -> None:
        super().__init__()

        self.page = page
        self.update_appbar_counts = update_appbar_counts        

        self.padding=15

        self.btn_add_task = ButtonAddNewTask(self.add_task_click)
        self.new_task = NewTask()
        self.filter_task = Filter(self.tabs_changed)
        self.snackbar = CustomSnackBar()

        self.listview = ft.ListView(
            spacing=5,
        )

        # Ponto de entrada para objetos da aplicação
        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            self.new_task,
                            self.btn_add_task
                        ]
                    )
                ),

                ft.Container(
                    content=ft.Column(
                        controls=[
                            self.filter_task,
                            self.listview
                        ],
                    )
                ),
            ]
        )
        


    def did_mount(self) -> None:
        self.listview.controls.clear()
        self.load_data()


    def add_task_click(self, e) -> None:
        if self.new_task.value == "":
            self.snackbar.open = True
            self.page.overlay.append(self.snackbar)
            self.page.update()
            return

        create(self.new_task.value)
        self.new_task.value=""
        self.load_data()
        self.update_appbar_counts(self.page)
        self.update()


    def load_data(self) -> None:
        status = self.filter_task.tabs[self.filter_task.selected_index].text
        self.listview.controls.clear()

        dados = read()
        
        if status == "Ativa":
            for item in dados:
                if item[3] == 0:
                    self.listview.controls.append(
                        CustomCard(
                            id=item[0],
                            status=item[3],
                            txt_title=item[1], 
                            txt_time=item[2],
                            todo_instance=self
                        )
                    )
            self.update()

        elif status == "Completada":    
            for item in dados:
                if item[3] == 1:
                    self.listview.controls.append(
                        CustomCard(
                            id=item[0],
                            status=item[3],
                            txt_title=item[1], 
                            txt_time=item[2],
                            todo_instance=self
                        )
                    )
            self.update()        


    def tabs_changed(self, e) -> None:
        self.load_data()
