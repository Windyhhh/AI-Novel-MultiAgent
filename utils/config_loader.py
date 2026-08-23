"""配置加载工具"""
import os
import yaml
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置管理类"""
    
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self.config = self._load_yaml_config()
        self._load_env_config()
    
    def _load_yaml_config(self):
        """加载YAML配置文件"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    def _load_env_config(self):
        """加载环境变量配置"""
        self.hepai_api_key = os.getenv("HEPAI_API_KEY")
        self.hepai_base_url = os.getenv("HEPAI_BASE_URL", "https://aiapi.ihep.ac.cn/apiv2")
        self.hepai_model = os.getenv("HEPAI_MODEL", "hepai/deepseek-r1:671b")
        
        # 飞书配置
        self.feishu_app_id = os.getenv("FEISHU_APP_ID")
        self.feishu_app_secret = os.getenv("FEISHU_APP_SECRET")
        self.feishu_doc_token = os.getenv("FEISHU_DOC_TOKEN")
    
    def get(self, key, default=None):
        """获取配置项"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def set(self, key, value):
        """设置配置项"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def save(self):
        """保存配置到文件"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)

# 全局配置实例
config = Config()

