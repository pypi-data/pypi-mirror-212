from config_mgmt_server.app import config_mgmt_server


def main() -> str:
    """Entry point for the application script"""
    config_mgmt_server()
    return "Success"