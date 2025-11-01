# 大模型配置
MODEL_CONFIGS = {
    "GPT-4o": {
        "api_base": "https://api.openai.com/v1",
        "model_name": "gpt-4o",
        "api_type": "openai",  # OpenAI 兼容 API
        "is_preset": True,
    },
    "GPT-5": {
        "api_base": "https://api.openai.com/v1",
        "model_name": "gpt-5",
        "api_type": "openai",  # OpenAI 兼容 API
        "is_preset": True,
    },
    "Claude": {
        "api_base": "https://api.anthropic.com",
        "model_name": "claude-3-5-sonnet-latest",
        "api_type": "claude",  # Claude 有自己的 API
        "is_preset": True,
    },
    "通义千问": {
        "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model_name": "qwen-max",
        "api_type": "openai",  # OpenAI 兼容 API
        "is_preset": True,
    },
    "DeepSeek": {
        "api_base": "https://api.deepseek.com/v1",
        "model_name": "deepseek-chat",
        "api_type": "openai",  # OpenAI 兼容 API
        "is_preset": True,
    },
    "智谱AI": {
        "api_base": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "model_name": "glm-4v-plus-0111",
        "api_type": "zhipu",  # 智谱 AI 有自己的客户端
        "is_preset": True,
    },
    "豆包": {
        "api_base": "https://ark.cn-beijing.volces.com/api/v3/",
        "model_name": "doubao-seed-1-6-251015",
        "api_type": "openai",  # OpenAI 兼容 API
        "is_preset": True,
    }
}

# OpenAI API 兼容模型的标识（用于菜单显示和配置文件键名）
CUSTOM_MODEL_KEY = "OpenAI API 兼容模型"
