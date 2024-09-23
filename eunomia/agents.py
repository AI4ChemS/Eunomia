import langchain
from langchain.agents import initialize_agent
from llama_index.core import ListIndex
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import get_openai_callback
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI


class Eunomia:
    def __init__(
        self,
        tools,
        model="gpt-4",
        temp=0.1,
        get_cost=False,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        **kwargs,
    ):
        self.get_cost = get_cost
        if type(model) == str:
            if model.startswith("gpt-3.5-turbo") or model.startswith("gpt-4"):
                self.llm = ChatOpenAI(
                    temperature=temp,
                    model_name=model,
                    request_timeout=1000,
                    max_tokens=2000,
                )

         
        else: 
            self.llm = model
        # Initialize agent
        memory = ConversationBufferMemory(memory_key="chat_history")
        self.agent_chain = initialize_agent(
                tools, self.llm, agent=agent_type, verbose=True, memory=memory, **kwargs
            )

    def run(self, prompt):
        with get_openai_callback() as cb:
            result = self.agent_chain.run(input=prompt)
        if self.get_cost:
            print(cb)
        return result
