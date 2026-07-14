
import tkinter as tk


class DashboardPage(tk.Frame):

    def __init__(self,parent):

        super().__init__(parent)


        tk.Label(
            self,
            text="AGS Enterprise Dashboard",
            font=("Arial",26,"bold")
        ).pack(pady=20)



        cards=tk.Frame(self)
        cards.pack(
            fill="x",
            padx=40
        )


        data=[
            ("Companies","12"),
            ("Projects","48"),
            ("Customers","256"),
            ("AI Engine","ONLINE"),
            ("Autonomous","READY"),
            ("Finance","ACTIVE")
        ]


        for i,(title,value) in enumerate(data):

            box=tk.Frame(
                cards,
                width=220,
                height=120,
                relief="ridge",
                borderwidth=2
            )

            box.grid(
                row=i//3,
                column=i%3,
                padx=15,
                pady=15,
                sticky="nsew"
            )

            box.pack_propagate(False)


            tk.Label(
                box,
                text=title,
                font=("Arial",13)
            ).pack(pady=15)


            tk.Label(
                box,
                text=value,
                font=("Arial",20,"bold")
            ).pack()



        activity=tk.Frame(
            self,
            relief="ridge",
            borderwidth=2
        )

        activity.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=20
        )


        tk.Label(
            activity,
            text="AGS Autonomous ERP Intelligence Center",
            font=("Arial",16,"bold")
        ).pack(pady=20)


        tk.Label(
            activity,
            text=
            "System Health: ONLINE\n"
            "AI Agents: READY\n"
            "Enterprise Builder: ACTIVE\n"
            "Database Engine: CONNECTED"
        ).pack()

