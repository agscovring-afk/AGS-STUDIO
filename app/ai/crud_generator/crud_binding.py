def bind_crud(page, controller):

    page.controller = controller


    if hasattr(page, "add_btn"):

        page.add_btn.config(
            command=lambda: open_add(page, controller)
        )


    if hasattr(page, "edit_btn"):

        page.edit_btn.config(
            command=lambda: open_edit(page, controller)
        )


    if hasattr(page, "delete_btn"):

        page.delete_btn.config(
            command=lambda: delete_record(page, controller)
        )


    if hasattr(page, "table"):

        load_data(
            page,
            controller
        )



def load_data(page, controller):

    if hasattr(controller, "get_all"):

        data = controller.get_all()

        for item in data:

            page.table.insert(
                "",
                "end",
                values=item
            )



def open_add(page, controller):

    dialog = page.dialog_class(
        page
    )


    page.wait_window(
        dialog
    )


    data = dialog.get_data()


    if data:

        controller.create(
            data
        )

        refresh(
            page,
            controller
        )



def open_edit(page, controller):

    return None



def delete_record(page, controller):

    selected = page.get_selected_id()


    if selected:

        controller.delete(
            selected
        )

        refresh(
            page,
            controller
        )



def refresh(page, controller):

    page.table.delete(
        *page.table.get_children()
    )


    load_data(
        page,
        controller
    )