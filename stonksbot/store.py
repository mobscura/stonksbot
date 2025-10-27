import yaml
from pathlib import Path
from conf.config import TRADING_CONFIG

# Global storage for class-level attributes
_store_data = {
    '_system': TRADING_CONFIG.get('system', False),
    '_mode': TRADING_CONFIG.get('mode', False),
    '_tp': TRADING_CONFIG.get('tp', '1-2-3-5'),
    '_stop': TRADING_CONFIG.get('stop', 2.25),
    '_risk': TRADING_CONFIG.get('risk', 0.63),
    '_leverage': TRADING_CONFIG.get('leverage', 25),
    '_multiplier': TRADING_CONFIG.get('multiplier', 1)
}

class StoreMeta(type):
    """Metaclass to handle Store.attribute = value syntax and auto-save to config"""
    def __setattr__(cls, name, value):
        if name in ['system', 'mode', 'tp', 'stop', 'risk', 'leverage', 'multiplier']:
            _store_data['_' + name] = value
            cls._update_config_file()
        else:
            super().__setattr__(name, value)
    
    def __getattr__(cls, name):
        if name in ['system', 'mode', 'tp', 'stop', 'risk', 'leverage', 'multiplier']:
            return _store_data['_' + name]
        raise AttributeError(f"'{cls.__name__}' has no attribute '{name}'")

class Store(metaclass=StoreMeta):
    _config_path = Path(__file__).parent.parent / "config.yml"
    
    @classmethod
    def _update_config_file(cls):
        """Update the trading section in config.yml"""
        import tempfile
        import shutil
        
        try:
            # Read the current config
            with open(cls._config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file) or {}
            
            # Get values from global storage
            config['trading'] = {
                'system': bool(_store_data['_system']),
                'mode': bool(_store_data['_mode']),
                'tp': str(_store_data['_tp']),
                'stop': float(_store_data['_stop']),
                'risk': float(_store_data['_risk']),
                'leverage': int(_store_data['_leverage']),
                'multiplier': int(_store_data['_multiplier'])
            }
            
            # Write to a temporary file first to avoid corrupting the original
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', 
                                             suffix='.yml', delete=False) as temp_file:
                yaml.dump(config, temp_file, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False, indent=2)
                temp_path = temp_file.name
            
            # Only replace the original file if write succeeded
            shutil.move(temp_path, cls._config_path)
            
        except Exception as e:
            print(f"Error updating config file: {e}")
    
    def __init__(self):
        # Instance properties delegate to class
        pass
    
    # Instance properties for backward compatibility
    @property
    def system(self):
        return _store_data['_system']

    @system.setter
    def system(self, value):
        _store_data['_system'] = value
        Store._update_config_file()

    @property
    def mode(self):
        return _store_data['_mode']

    @mode.setter
    def mode(self, value):
        _store_data['_mode'] = value
        Store._update_config_file()

    @property
    def tp(self):
        return _store_data['_tp']

    @tp.setter
    def tp(self, value):
        _store_data['_tp'] = value
        Store._update_config_file()

    @property
    def stop(self):
        return _store_data['_stop']

    @stop.setter
    def stop(self, value):
        _store_data['_stop'] = value
        Store._update_config_file()

    @property
    def risk(self):
        return _store_data['_risk']

    @risk.setter
    def risk(self, value):
        _store_data['_risk'] = value
        Store._update_config_file()

    @property
    def leverage(self):
        return _store_data['_leverage']

    @leverage.setter
    def leverage(self, value):
        _store_data['_leverage'] = value
        Store._update_config_file()

    @property
    def multiplier(self):
        return _store_data['_multiplier']

    @multiplier.setter
    def multiplier(self, value):
        _store_data['_multiplier'] = value
        Store._update_config_file()

    # Access to private attributes for backward compatibility
    @property
    def _system(self):
        return _store_data['_system']

    @property
    def _mode(self):
        return _store_data['_mode']

    @property
    def _tp(self):
        return _store_data['_tp']

    @property
    def _stop(self):
        return _store_data['_stop']

    @property
    def _risk(self):
        return _store_data['_risk']

    @property
    def _leverage(self):
        return _store_data['_leverage']

    @property
    def _multiplier(self):
        return _store_data['_multiplier']