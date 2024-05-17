import sys, os
from app import create_app, db
from dotenv import load_dotenv, find_dotenv
import argparse


parser = argparse.ArgumentParser(
    description='Run the application with specified environment.'
)
parser.add_argument(
    '--env',
    choices=['dev', 'prod'],
    default='dev',
    help='Set the environment (default: dev)'
)
parser.add_argument(
    '--initdb',
    action='store_true',
    help='Initialize the database'
)

args = parser.parse_args()
env_path = '.env.dev' if args.env == 'dev' else '.env'

env_file_path = find_dotenv(env_path)
if not env_file_path:
    print(f'{env_path} file not found, using environment variables')

load_dotenv(env_file_path, override=True)

app = create_app()


if __name__ == "__main__":

    if args.initdb:
        with app.app_context():
            db.create_all()
            print('Initialized the database.')
    else:
        print(f'Running in {args.env} mode')
        debug = True if os.getenv('APP_MODE', 'dev') == 'dev' else False
        app.run(debug=debug, port=8765, host='0.0.0.0')