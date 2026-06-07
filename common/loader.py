# common/loader.py
import os
import re
import yaml
import warnings
from pathlib import Path

# 敏感信息的默认值（仅用于公开的测试环境）
_DEFAULT_SECRETS = {
    "SAUCEDEMO_PASSWORD": "secret_sauce",
}

def _replace_env_vars(data):
    """递归替换数据中的 ${ENV_VAR} 占位符，未设置则使用默认值并警告"""
    if isinstance(data, str):
        for match in re.finditer(r'\$\{(\w+)\}', data):
            var_name = match.group(1)
            env_value = os.getenv(var_name, "")
            if not env_value:
                if var_name in _DEFAULT_SECRETS:
                    env_value = _DEFAULT_SECRETS[var_name]
                    warnings.warn(
                        f"环境变量 {var_name} 未设置，使用默认值（仅用于公开测试）",
                        stacklevel=2
                    )
                else:
                    raise ValueError(f"环境变量 {var_name} 未设置，且没有默认值")
            data = data.replace(f"${{{var_name}}}", env_value)
        return data
    elif isinstance(data, dict):
        return {k: _replace_env_vars(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_replace_env_vars(item) for item in data]
    return data

def load_yaml(filename: str):
    """加载 testdata 目录下的 YAML 文件并处理环境变量"""
    path = Path(__file__).parent.parent / "testdata" / filename
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return _replace_env_vars(raw)