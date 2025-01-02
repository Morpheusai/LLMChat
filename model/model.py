#claude api delete
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage,SystemMessage

class Model:
    def __init__(self,provider="openai",model_name="gpt-4o",temperature=0.7,generate_token=1000):
        """
        初始化模型支持多模型切换
        :param provider: 模型提供方 (openai, claude, deepseek)
        :param model_name: 模型名称
        :param base_url: 如果是第三方模型 (如 Deepseek) 则需要指定
        """
        # 根据 provider 初始化不同模型
        self.provider = provider
        self.model_name = model_name
        self.temperature = temperature
        self.generate_token = generate_token
        
        if provider.lower() == "openai":
            #api_key = os.getenv("OPENAI_API_KEY")
            openai_api_key = ""
            self._llm = ChatOpenAI(
                api_key=openai_api_key,
                model=model_name,
                temperature=temperature,
                max_tokens=generate_token,
                streaming=True,
                base_url="https://api.openai.com/v1"
            )
            
        elif provider.lower() == "deepseek":
            #deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
            deepseek_api_key = ""
            self._llm = ChatOpenAI(
                api_key=deepseek_api_key,
                model = model_name,
                temperature=temperature,
                max_tokens=generate_token,
                streaming=True,
                base_url="https://api.deepseek.com"
            )
        elif provider.lower() == "claude":
            #claude_api_key = os.getenv("CLAUDE_API_KEY")
            claude_api_key = ""
            self._llm = ChatAnthropic(
                api_key=claude_api_key,
                model=model_name,
                temperature=temperature,
                max_tokens=generate_token,
                base_url="https://api.anthropic.com"
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")
            
    def __call__(self,user_input):
        messages = [
            SystemMessage(content="You are a helpful and knowledgeable assistant. And please answer in Chinese!,只要有公式时，就用正确的LaTeX语法，并使用'$'来修饰,请注意每一次公示的修饰，请谨慎一点，不要出错！！！"),
            HumanMessage(content=user_input)
            ]
        
        responses = self._llm.invoke(messages)
        return responses.content
if __name__ == "__main__":
    model = Model(provider="deepseek",model_name="deepseek-chat",temperature=0.7,generate_token=1000)
    response = model("请问你的版本号？")
    print(response)
