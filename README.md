# 🧪 自动化测试框架 - SauceDemo

![CI Status](https://github.com/mylevi07/test_project/actions/workflows/test.yml/badge.svg)

## 项目简介
基于 PyTest 的企业级分层自动化测试框架，支持 API + UI 自动化，集成 GitHub Actions 持续集成，采用数据驱动与敏感信息环境变量管理。

## 技术栈
- **语言**：Python 3.14
- **框架**：PyTest + Requests + Playwright
- **报告**：pytest-html
- **CI/CD**：GitHub Actions
- **数据驱动**：YAML + @pytest.mark.parametrize + 环境变量注入

## 项目结构
├── common/ # 通用封装（API客户端、Web基类、日志、数据加载器）
├── config/ # 环境配置（YAML）
├── pages/ # 页面对象（PO模式）
├── testcases/ # 测试用例（API + UI）
│ ├── test_api/ # API 测试（JSONPlaceholder）
│ └── test_ui/ # UI 测试（SauceDemo）
├── testdata/ # 测试数据（YAML，敏感信息用环境变量占位）
├── logs/ # 运行日志
├── screenshots/ # 截图
├── .github/ # CI/CD 配置（GitHub Actions）
└── requirements.txt # 依赖清单


## 快速开始
```bash
# 1. 安装依赖
pip install -r requirements.txt
playwright install chromium

# 2. 设置密码环境变量
$env:SAUCEDEMO_PASSWORD = "secret_sauce"

# 3. 运行测试
pytest testcases/ -v --html=report.html --self-contained-html

# 4. 切换环境
pytest testcases/ --env=staging

核心特性
分层架构：config / common / pages / testcases 职责分离

数据驱动：YAML 管理测试数据，@pytest.mark.parametrize 参数化

安全机制：敏感信息通过 ${ENV_VAR} 占位符 + 环境变量注入，不提交明文密码

Page Object：封装页面元素与操作，WebBase 基类提供通用操作复用

CI/CD：GitHub Actions 自动执行全量回归，生成 HTML 报告

日志与截图：运行日志写入 logs/，失败自动截图到 screenshots/

