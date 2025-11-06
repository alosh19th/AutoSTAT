#!/usr/bin/env bash
set -e

APP_NAME="AutoSTAT"
ENV_NAME="autostat_env"
PYTHON_VERSION="3.12"

echo "========================================="
echo "AutoSTAT 环境配置脚本"
echo "========================================="

if ! command -v conda &> /dev/null
then
    echo "未检测到 conda。请先安装 Miniconda 或 Anaconda："
    echo "https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

if conda info --envs | grep -q "$ENV_NAME"
then
    echo "已检测到环境 '$ENV_NAME'，将直接使用。"
else
    echo "正在创建 Conda 环境 '$ENV_NAME' ..."
    conda create -y -n "$ENV_NAME" python="$PYTHON_VERSION"
fi

echo "激活环境中..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"

echo "正在使用 pip 安装 requirements_mac.txt ..."
if [ -f "requirements_mac.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements_mac.txt
else
    echo "⚠️ 未找到 requirements_mac.txt，跳过依赖安装。"
fi

echo "正在安装 Playwright ..."
pip install playwright

echo "正在下载 Playwright 浏览器驱动（playwright install）..."
playwright install

echo "正在安装 Watchdog..."
pip install watchdog

echo "========================================="
echo " $ AutoSTAT 环境配置完成！"
read -p "是否现在启动 AutoSTAT ?(y/n) " choice
if [ "$choice" = "y" ]; then
    streamlit run app.py
fi
echo "========================================="



