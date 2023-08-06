import logging
import os

from auto_app import APIAutoApp


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Run FastAPI application.')
    parser.add_argument('--config', type=str, required=False, help='Path to the configuration file.')
    parser.add_argument('--env_type', type=str, default="development", required=False,
                        help='Environment to run the application in.')
    parser.add_argument('--host', type=str, default="0.0.0.0", help='Host to run the application on.')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the application on.')
    parser.add_argument('--run', action='store_true', help='Run the application.')
    parser.add_argument('--demo', action='store_true',
                        help='Run the Streamlit demo. (alpha - does not accept any of the other kwargs for running the app')
    args = parser.parse_args()

    if args.demo:  # todo make this use the microservice rather than running with its own settings, UI should just be UI
        import subprocess
        subprocess.run(["streamlit", "run", "route_generation/streamlit_demo.py"])
        return
    if not os.path.isfile(args.config):
        logging.error(f"Configuration file {args.config} does not exist.")
        raise FileNotFoundError(f"Configuration file {args.config} does not exist.")

    apiautoapp = APIAutoApp()

    if args.run:
        app = apiautoapp.build_app()
        apiautoapp.run(host=args.host, port=args.port, app=app)
    else:
        return apiautoapp.build_app()


if __name__ == "__main__":
    main()
