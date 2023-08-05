import requests
import argparse
import sys
import os
import json
from pathlib import Path
import yaml
import psycopg2
import importlib.metadata
import waitress
from datetime import datetime


BB_BASE_API_URL = None
BB_API_KEY = None
PERMISSIONS = None
DB_CONNECTION = None
LISTEN_PORT = None


session = None
__version__ = importlib.metadata.version(__package__)


def init(config_file: str) -> None:
    global session

    def load_config(config_file: str) -> None:
        global BB_BASE_API_URL, BB_API_KEY, PERMISSIONS, DB_CONNECTION, LISTEN_PORT
        if config_file:
            c = Path(config_file).expanduser()
            if not c.exists():
                fail(f"Could not find config file: {c}")
            with c.open() as f:
                y = yaml.safe_load(f)
                BB_BASE_API_URL = y["bb_base_api_url"]
                BB_API_KEY = y["bb_api_key"]
                PERMISSIONS = y["permissions"]
                DB_CONNECTION = y["db_connection"]
                LISTEN_PORT = y["listen_port"]
        else:
            print("No config file was specified. Using environment variables")
            for env in ["BB_BASE_API_URL", "BB_API_KEY", "PERMISSIONS", "DB_CONNECTION", "LISTEN_PORT"]:
                if env not in os.environ:
                    fail(f"Environment variable {env} not set")
            BB_BASE_API_URL = os.environ["BB_BASE_API_URL"]
            BB_API_KEY = os.environ["BB_API_KEY"]
            try:
                PERMISSIONS = json.loads(os.environ["PERMISSIONS"])
            except json.JSONDecodeError as e:
                fail(f"Environment variable PERMISSIONS muste be valid json:\nsupplied: {PERMISSIONS}\nerror:{e}")
            DB_CONNECTION = os.environ["DB_CONNECTION"]
            LISTEN_PORT = os.environ["LISTEN_PORT"]

    load_config(config_file)
    session = requests.Session()
    session.headers.update({"x-budibase-api-key": BB_API_KEY})


def fail(msg: str):
    print(f"ERROR: {msg}")
    sys.exit(1)


def run_backend():
    from flask import Flask, jsonify
    #from threading import Thread

    app = Flask(__name__)

    @app.route("/")
    def index():
        return f"This is the buditool (version: {__version__}): https://git.itsnow.biz/kamille/buditool", 200

    @app.route("/sync")
    def sync():
        print("Webhook called")
        #Thread(target=sync_db_permissions).start()
        err, err_msg = sync_db_permissions()
        if err:
            return jsonify(error=str(err_msg)), 500
        else:
            return jsonify(status="ok"), 200

    print(f"Starting webhook backend on port {LISTEN_PORT} (version {__version__})")
    # run debug server if started with poetry run python lg_april_permissions/__init__.py -c settings.yaml --serve
    if __name__ == '__main__':
        app.run(debug=True, port=LISTEN_PORT)
    else:
        waitress.serve(app, port=LISTEN_PORT)


def show_apps() -> None:
    try:
        resp = session.post(BB_BASE_API_URL + "applications/search")
        if resp.status_code != 200:
            fail(f"Status code: {resp.status_code}\n{resp.text}")
        j = resp.json()
    except Exception as e:
        fail(e)
    print(json.dumps(j, indent=4))


def get_user(userid: str) -> {}:
    # we need to soft fail here if we get a 400 status code (user does not exist, otherwise sync_db_permissions will stop)
    # we need to hard fail here if we get a 500 stauts code => cronjob will fail => an email is sent
    try:
        resp = session.get(BB_BASE_API_URL + "users/" + userid)
        if resp.status_code > 200 and resp.status_code < 500:
            print(f"Status code: {resp.status_code}\n{resp.text}")
            return
        elif resp.status_code >= 500:
            fail(f"Status code: {resp.status_code}:\n{resp.text}")
        j = resp.json()
    except Exception as e:
        print(f"ERROR getting user: {e}")
        return
    return j


def get_users() -> dict:
    try:
        resp = session.post(BB_BASE_API_URL + "users/search")
        if resp.status_code != 200:
            fail(f"Status code: {resp.status_code}\n{resp.text}")
        j = resp.json()
    except Exception as e:
        fail(e)
    users = j['data']
    return users


def show_users() -> None:
    users = get_users()
    print(json.dumps(users, indent=4))


def show_users_by_app(filter_app_id: str) -> None:
    users = get_users()
    for user in users:
        for app_id, permission in user['roles'].items():
            if app_id == filter_app_id:
                name = f"{user['firstName']} {user['lastName']}"
                print(f"{user['_id']} | {name:<35} | {user['email']:<40} | {permission}")


def bikoe_migration():
    """Jede, die Zugriff auf die Protest-Buffet App hat, bekommt BASIC Rechte für die Bikö-Krönung App - wird nur einmal benötigt"""
    buffet_app_id = "app_6bb0b333c2fd43fb98f4b54a67e17c14"
    biko_kroenung_id = "app_f06982298ecc47b7b5ab9019c7fbd1a8"

    def add_bikeo_permissions(userid: str):
        print(f"Adding BikÖ permissions for user {userid}")
        u = get_user(userid)
        roles = u['data']['roles']
        print(f"Rollen vorher:\n{json.dumps(roles, indent=4)}")
        perm = {biko_kroenung_id: "BASIC"}
        roles.update(perm)

        u = update_user_roles(userid, roles)
        roles = u['data']['roles']
        print(f"Rollen danach:\n{json.dumps(roles, indent=4)}")

    users = get_users()
    for user in users:
        for app_id, permission in user['roles'].items():
            if app_id == buffet_app_id:
                name = f"{user['firstName']} {user['lastName']}"
                print(f"{user['_id']} | {name:<35} | {user['email']:<40} | {permission}")
                add_bikeo_permissions(user['_id'])


def show_user(userid: str) -> None:
    u = get_user(userid)
    if u:
        print(json.dumps(u, indent=4))


def update_user_roles(userid: str, roles: dict) -> None:
    try:
        data = {"roles": roles}
        resp = session.put(BB_BASE_API_URL + "users/" + userid, json=data)
        if resp.status_code != 200:
            fail(f"Status code: {resp.status_code}\n{resp.text}")
        j = resp.json()
    except Exception as e:
        fail(e)
    return j


def add_permissions(userid: str):
    print(f"Adding permissions for user {userid}")
    u = get_user(userid)
    if not u:
        return
    roles = u['data']['roles']
    if PERMISSIONS.items() <= roles.items():
        print(f"User {userid} already has the valid permissions. Skipping ...")
        return

    print(f"User {userid} lacks some permissions. Updating ...")
    print(f"Permissions before:\n{json.dumps(roles, indent=4)}")
    roles.update(PERMISSIONS)
    u = update_user_roles(userid, roles)
    roles = u['data']['roles']
    print(f"Permissions after:\n{json.dumps(roles, indent=4)}")


def remove_permissions(userid: str):
    print(f"Removing permissions for user {userid}")
    u = get_user(userid)
    if not u:
        return
    roles = u['data']['roles']
    print(f"Rollen vorher:\n{json.dumps(roles, indent=4)}")

    for app_id in PERMISSIONS.keys():
        roles.pop(app_id, None)
        # fix: strange behaviour of Budibase
        if "dev" in app_id:
            app_id_without_dev = app_id.replace("dev_", "")
            roles.pop(app_id_without_dev, None)

    roles = u['data']['roles']
    u = update_user_roles(userid, roles)
    roles = u['data']['roles']
    print(f"Rollen danach:\n{json.dumps(roles, indent=4)}")


def sync_db_permissions() -> (bool, str):
    print(f"Syncing permissions with database at {datetime.now().strftime('%H:%M:%S')}")
    try:
        conn = psycopg2.connect(DB_CONNECTION)
        cur = conn.cursor()
        cur.execute('SELECT fk_bikoe FROM "April_Permissions"')
        permissions = cur.fetchall()
        for permission in permissions:
            fk_bikoe = int(permission[0])
            print(f"Processing Bikö {fk_bikoe}")
            cur.execute('SELECT "Vorname", "Nachname", "RL_user_id" FROM "Kontaktinfo" WHERE id = %s', (fk_bikoe,))
            vorname, nachname, bb_user_id = cur.fetchone()
            if bb_user_id.startswith("ro_ta_users_"):
                bb_user_id = bb_user_id.replace("ro_ta_users_", "")
            if "https://bb.itsnow.biz/app/aktionsphasen-portal" in bb_user_id:
                print(f"WARNING: bb_user_id in Table Kontaktinfo has an invalid value: {bb_user_id}")
                # soft fail
                continue
            print(f" Budibase user id: {bb_user_id} ({vorname} {nachname})")
            add_permissions(bb_user_id)
    except Exception as e:
        return True, str(e)
    print(f"Syncing permissions was successful at {datetime.now().strftime('%H:%M:%S')}")
    return False, ""


def show_version():
    print(f"{sys.argv[0]} v{__version__}")
    sys.exit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="show user (needs bb user id)")
    parser.add_argument("--list-apps", action="store_true", help="list all bb apps")
    parser.add_argument("--list-users", action="store_true", help="list all bb users")
    parser.add_argument("--show-users-by-app", help="list all users and their permissions for a specific <app id>")
    parser.add_argument("-a", "--add-permissions", help="add permissions for user (needs bb user id)")
    parser.add_argument("-r", "--remove-permissions", help="remove permissions for user (needs bb user id)")
    parser.add_argument("-s", "--sync", action="store_true", help="synchronize permissions with db")
    parser.add_argument("-c", "--config", help="config file")
    parser.add_argument("--serve", action="store_true", help="run backend with /sync to run --sync by webhook")
    parser.add_argument("--version", action="store_true", help="show version")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_usage()
        sys.exit()

    if args.version:
        show_version()

    init(args.config)
    if args.user:
        show_user(args.user)
    elif args.list_apps:
        show_apps()
    elif args.list_users:
        show_users()
    elif args.add_permissions:
        add_permissions(args.add_permissions)
    elif args.remove_permissions:
        remove_permissions(args.remove_permissions)
    elif args.show_users_by_app:
        show_users_by_app(args.show_users_by_app)
    elif args.sync:
        err, err_msg = sync_db_permissions()
        if err:
            print(err_msg)
            sys.exit(1)
    elif args.serve:
        run_backend()


if __name__ == '__main__':
    main()
