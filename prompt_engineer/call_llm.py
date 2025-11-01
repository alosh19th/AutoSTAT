from openai import OpenAI, OpenAIError
from anthropic import Anthropic, AnthropicError
import zai
from zai import ZhipuAiClient

import streamlit as st
import pandas as pd
from typing import List, Dict


class LLMClient:
    def __init__(self, model_configs: dict, api_keys: dict, model: str):

        self.model = model
        self.model_configs = model_configs
        self.api_keys = api_keys
        self.memory = []
        self.df = None

    def call(self, prompt) -> str:

        model_name = st.session_state.selected_model
        config = self.model_configs.get(model_name, {})
        api_key = self.api_keys.get(model_name)

        if not api_key:
            return "请先在设置中配置 API 密钥"
        
        system_msg = (
            "你是一个专业的数据分析助手。"
        )

        try:
            # 获取 API 类型
            api_type = config.get("api_type", "openai")
            
            # 根据 API 类型选择不同的调用方式
            if api_type == "openai":
                # OpenAI 兼容的 API（包括 OpenAI、DeepSeek、通义千问、豆包等）
                try:
                    client = OpenAI(
                        api_key=api_key,
                        base_url=config.get("api_base", "https://api.openai.com/v1")
                    )
                    
                    response = client.chat.completions.create(
                        model=config.get("model_name", "gpt-4o"),
                        messages=[
                            {"role": "system", "content": system_msg},
                            {"role": "user", "content": prompt},
                        ],
                        stream=False
                    )
                    return response.choices[0].message.content
                
                except OpenAIError as e:
                    msg = f"API 调用失败：{str(e)}"
                    st.error(msg)
                    return f"调用失败，请检查密钥或网络（{msg}）"
                except Exception as e:
                    msg = f"发生未知错误：{str(e)}"
                    st.error(msg)
                    return msg
            
            elif api_type == "claude":
                # Claude 使用 Anthropic SDK
                try:
                    client = Anthropic(api_key=api_key)
                    
                    response = client.messages.create(
                        model=config.get("model_name", "claude-3-5-sonnet-latest"),
                        max_tokens=4096,
                        system=system_msg,
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    return response.content[0].text
                
                except AnthropicError as e:
                    msg = f"Claude API 调用失败：{str(e)}"
                    st.error(msg)
                    return f"调用失败，请检查密钥或网络（{msg}）"
                except Exception as e:
                    msg = f"发生未知错误：{str(e)}"
                    st.error(msg)
                    return msg

            elif api_type == "zhipu":
                # 智谱 AI 使用自己的客户端
                # 参考 https://github.com/zai-org/z-ai-sdk-python
                try:
                    client = ZhipuAiClient(
                        api_key=api_key,
                        base_url=config.get("api_base", "https://open.bigmodel.cn/api/paas/v4")
                    )
                    
                    response = client.chat.completions.create(
                        model=config.get("model_name", "glm-4v-plus-0111"),
                        messages=[
                            {"role": "system", "content": system_msg},
                            {"role": "user", "content": prompt}
                        ],
                        thinking={"type": "enabled"}
                    )
                    desc = response.choices[0].message.content if hasattr(
                        response.choices[0].message, "content"
                    ) else str(response.choices[0].message)
                    return desc.replace("<|begin_of_box|>", "").replace("<|end_of_box|>", "").strip()

                except zai.core.APIStatusError as e:
                    msg = f"智谱 API 状态错误：{str(e)}"
                    st.error(msg)
                    return f"调用失败，请检查密钥或网络（{msg}）"
                except zai.core.APITimeoutError as e:
                    msg = f"智谱 API 请求超时：{str(e)}"
                    st.error(msg)
                    return f"调用失败，请检查密钥或网络（{msg}）"
                except Exception as e:
                    msg = f"发生未知错误：{str(e)}"
                    st.error(msg)
                    return msg

            else:
                return f"不支持的 API 类型：{api_type}"

        except Exception as e:
            msg = f"{model_name} 调用异常：{e}"
            st.error(msg)
            return f"大模型调用失败，请检查 API 密钥或网络连接（{msg}）"

    
    def add_memory(self, entry: Dict[str, str]) -> None:

        self.memory.append(entry)


    def load_memory(self) -> List[Dict[str, str]]:

        return self.memory


    def clear_memory(self) -> None:

        self.memory.clear()


    def add_df(self, input_df) -> None:

        self.df = input_df
        

    def load_df(self) -> pd.DataFrame:

        return self.df
    

    def clear_df(self) -> None:

        self.df = None


    def has_df(self) -> bool:

        return self.df is None
