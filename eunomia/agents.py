import langchain
from langchain.agents import initialize_agent
from llama_index import GPTListIndex, GPTIndexMemory
from langchain.callbacks import get_openai_callback
from langchain.agents import AgentType


class Eunomia:
    def __init__(
        self,
        tools,
        model="text-davinci-003",
        temp=0.1,
        get_cost=False,
        max_iterations=40,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        **kwargs,
    ):
        if model.startswith("gpt-3.5-turbo") or model.startswith("gpt-4"):
            self.llm = langchain.chat_models.ChatOpenAI(
                temperature=temp,
                model_name=model,
                request_timeout=1000,
                max_tokens=2000,
            )
        elif model.startswith("text-"):
            self.llm = langchain.OpenAI(temperature=temp, model_name=model)
        self.get_cost = get_cost
        self.max_iterations = max_iterations

        # Initialize agent
        index = GPTListIndex([])
        memory = GPTIndexMemory(
            index=index,
            memory_key="chat_history",
            query_kwargs={"response_mode": "compact"},
        )
        self.agent_chain = initialize_agent(
            tools, self.llm, agent=agent_type, verbose=True, memory=memory, **kwargs
        )

    def run(self, prompt):
        with get_openai_callback() as cb:
            result = self.agent_chain.run(input=prompt)
        if self.get_cost:
            print(cb)
        return result
