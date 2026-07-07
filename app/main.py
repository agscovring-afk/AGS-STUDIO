"""Application entry point for AGS ERP V2."""

import argparse
import os

from app.repositories.company_repository import CompanyRepository
from app.controllers.company_controller import CompanyController


def get_controller(db=None):
    repo = CompanyRepository(db or os.path.join(os.getcwd(), "ags_erp.db"))
    return CompanyController(repo)


# ==========================
# Database
# ==========================

def cmd_init_db(args):
    controller = get_controller(args.db)
    controller.init_db()
    print("✅ Database initialized.")


# ==========================
# Company
# ==========================

def cmd_create_company(args):
    controller = get_controller(args.db)

    cid = controller.create_company(
        args.legal_name,
        args.commercial_name,
        args.code,
        args.currency,
        args.language,
    )

    print(f"✅ Company created (ID={cid})")


def cmd_list_companies(args):
    controller = get_controller(args.db)

    companies = controller.list_companies(args.all)

    if not companies:
        print("No companies found.")
        return

    print("-" * 90)

    for c in companies:
        status = "Active" if c.is_active else "Inactive"

        print(
            f"{c.id:3} | "
            f"{c.legal_name:25} | "
            f"{c.code:10} | "
            f"{c.currency:5} | "
            f"{status}"
        )

    print("-" * 90)


# ==========================
# MAIN
# ==========================

def main():

    parser = argparse.ArgumentParser("AGS ERP V2")

    sub = parser.add_subparsers(dest="command")

    # init-db
    p = sub.add_parser("init-db")
    p.add_argument("--db")
    p.set_defaults(func=cmd_init_db)

    # create-company
    p = sub.add_parser("create-company")
    p.add_argument("--legal-name", required=True)
    p.add_argument("--commercial-name", required=True)
    p.add_argument("--code", default="COMP001")
    p.add_argument("--currency", default="DZD")
    p.add_argument("--language", default="fr")
    p.add_argument("--db")
    p.set_defaults(func=cmd_create_company)

    # list-companies
    p = sub.add_parser("list-companies")
    p.add_argument("--all", action="store_true")
    p.add_argument("--db")
    p.set_defaults(func=cmd_list_companies)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()