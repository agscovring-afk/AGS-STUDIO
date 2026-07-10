"""
AGS ERP V2
UI Application Starter
"""

import customtkinter as ctk

from app.ui.main_window import MainWindow
from app.ui.pages.company_page import CompanyPage

from app.controllers.company_controller import CompanyController
from app.services.company_service import CompanyService
from app.repositories.company_repository import CompanyRepository



def start():

    repository = CompanyRepository()

    service = CompanyService(
        repository
    )

    controller = CompanyController(
        service
    )


    app = MainWindow()


    app.show_page(
        lambda parent: CompanyPage(
            parent,
            controller
        )
    )


    app.mainloop()



if __name__ == "__main__":

    start()
