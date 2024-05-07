import sys, os
from app import create_app
from dotenv import load_dotenv, find_dotenv

env_arg = 'dev' 
if len(sys.argv) > 1:
    env_arg = sys.argv[1]

env_path = '.env.dev'
if env_arg == 'prod':
    env_path = '.env'

env_file_path = find_dotenv(env_path)
if not env_file_path:
    print(f'{env_path} file not found, using environment variables')

load_dotenv(env_file_path)

app = create_app()

if __name__ == "__main__":
    print(f'Running in {env_arg} mode')
    debug = True if os.getenv('APP_MODE', 'dev') == 'dev' else False
    app.run(debug=debug, port=8765)