import logging, logging.config
import yaml, sys, re
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
sys.path.append(str(APP_DIR))

class LoggingInfo(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f'{Path(__file__).parent.parent.resolve()}/.env',
        env_prefix = 'LOG_',
        extra='ignore',
    )
    level_loggers: str
    level_app_console: str
    level_file: str
    dir: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_logging()

    def setup_logging(self):
        log_dir = Path(self.dir)
        log_dir.mkdir(exist_ok=True)

        with open(f'{BASE_DIR}/logging.yml', 'r') as f:
            config_data = f.read()

        def replacer_env_var(match):
            var = match.group(1)
            default = match.group(2) if match.group(2) else 'DEBUG'
            log_prefix = self.model_config.get('env_prefix', '').lower()
            level = getattr(self, var.lower().replace(log_prefix,''), default)
            return level

        def replacer_log_path(match):
            var_path = match.group(1)
            log_prefix = self.model_config.get('env_prefix', '').lower()
            path = getattr(self, var_path.lower().replace(log_prefix,''), '')
            return f'{path}/{match.group(2)}'

        pattern_var = r'\$\{([a-zA-Z_]+):-([a-zA-Z]+)\}'
        pattern_log_path = r'\$\{([A-Za-z_]+)\}\/([a-zA-Z_]+.log)'
        config_data = re.sub(pattern_var, replacer_env_var, config_data)
        config_data = re.sub(pattern_log_path, replacer_log_path, config_data)

        log_config = yaml.safe_load(config_data)
        self._validate_config(log_config)
        logging.config.dictConfig(log_config)
        return self

    @staticmethod
    def _validate_config(config_data):
        required_sections = ['version', 'formatters', 'handlers', 'loggers']
        for section in required_sections:
            if section not in config_data:
                raise ValueError(f'Required section {section} is missing')
        for logger, logger_conf in config_data['loggers'].items():
            for handler in logger_conf['handlers']:
                if handler not in config_data['handlers']:
                    raise ValueError(f'Required handler {handler} is missing')

class LoggingConfig(LoggingInfo):
    root: logging.Logger = logging.getLogger('root')
    app: logging.Logger = logging.getLogger('app')
    app_pre: logging.Logger = logging.getLogger('app.presentation')
    app_business: logging.Logger = logging.getLogger('app.business')
    app_data: logging.Logger = logging.getLogger('app.data')

class PostgresConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f'{Path(__file__).parent.parent.resolve()}/.env',
        env_prefix='POSTGRES_',
        case_sensitive=False,
        extra="ignore"
    )
    host: str
    port: int
    user: str
    password: SecretStr
    db: str

    @property
    def url(self):
        return f'postgresql://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}'

class Config(BaseSettings):
    postgres: PostgresConfig = PostgresConfig()
    logging: LoggingConfig = LoggingConfig()

config = Config()