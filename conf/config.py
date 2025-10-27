import yaml
from pathlib import Path

def load_config():
    """Load configuration from YAML file"""
    config_path = Path(__file__).parent.parent / "config.yml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    
    return config

# Load configuration
config = load_config()

# Telegram Bot Token
TOKEN = config['telegram']['token']

# Bybit API
API_KEY = config['bybit']['api_key']
SECRET_KEY = config['bybit']['secret_key']

# Trading bot
robot_id = config['telegram']['robot_id']
receiver_id = config['telegram']['receiver_id']

# Optional: Export other config values if needed
TRADING_CONFIG = config.get('trading', {})