from tqdm import tqdm
import json
from typing import List

from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import OutputFixingParser, PydanticOutputParser
from pydantic import BaseModel, Field

from eunomia.agents import Eunomia
import eunomia

from langchain.agents import Tool, tool
from langchain.llms import OpenAI

from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings


def read_jsonl(filename):
    """
    Read a jsonlines file into a list of dictionaries.

    Args:
        filename (str): Path to input file.

    Returns:
        ([dict]): List of dictionaries.
    """

    with open(filename, "r") as f:
        lines = f.readlines()
        samples = []
        for le in lines:
            samples.append(json.loads(le))
        return samples


# @tool
def format_output(answer):
    """
    Format the agent's answer into a python list of JSONs
    """

    class MOF(BaseModel):
        """Pydantic data model for a MOF."""

        name: str = Field(description="name of a MOF")
        formula: str = Field(description="formula of a MOF")
        description: list = Field(description="description of a MOF")
        guest_species: list = Field(description="guest_species of a MOF")
        applications: list = Field(description="applications of a MOF")

    class MOFList(BaseModel):
        """Pydantic data model for a list of MOFs."""

        MOFs: List[MOF]

    # Initialize a Pydantic output parser for the MOF list model
    parser = PydanticOutputParser(pydantic_object=MOFList)

    # Enhance the parser with capabilities to handle specific LLM outputs
    llm_parser = OutputFixingParser.from_llm(
        parser=parser, llm=ChatOpenAI(temperature=0, model="gpt-4")
    )

    # Check if result is a valid JSON string
    try:
        json.loads(answer, strict=False)
    except json.JSONDecodeError:
        # If not, convert it to a valid JSON string
        answer = json.dumps({"dummy_key": answer})
    # Try parsing the answer using the enhanced parser
    try:
        parsed_result = llm_parser.parse(answer)
    except ValueError as e:
        raise ValueError(f"Failed to parse MOF: {e}")

    # Construct a dictionary with MOFs' details using comprehension
    parsed_response = [
        {
            "name_of_mof": MOF.name,
            "mof_formula": MOF.formula,
            "mof_description": MOF.description,
            "guest_species": MOF.guest_species,
            "applications": MOF.applications,
        }
        for MOF in parsed_result.MOFs
    ]

    return parsed_response


run_ID = 1

mof_annotations_file = f"../data/NERRE/mof_results/run_{run_ID}.jsonl"
run = read_jsonl(mof_annotations_file)

prompt_mof = """You are an expert chemist. Read context, find all the MOFs and answer the following questions for each one:
name of MOF? MOF chemical formula? MOF description? guest species? applications?

Use this rules:
MOF names cannot be general like: "copper terephthalate metal–organic frameworks".
For chemical formula, exclude anything that contains words or the word "MOF" or single elements like just "Ag" or "Zn".
MOF description is a list of details about a MOF’s processing history, defects, modifications, or the sample’s morphology.
Guest species is a list of chemical molecules (like CO2, CH4, N2, H2, VOCs, etc.) that have been incorporated,
 stored, or absorbed in the MOF.
Applications is a list summary of applications or high-level use cases or major property classes for the MOF.
Applications may represent different levels of device-level implementation. Make the answer short like:
 "gas-separation", "heterogeneous
catalyst", "Diels-Alder reactions"



There may be more than a single MOF in the context. If so, answer all the questions for each one you find.

Your findings should be structured like this:

[{"name_of_mof": ...

"mof_formula": ...

"mof_description": [...]

"guest_species": [...]

"applications" : [...]}]


If the context don't mention each item, leave them empty and use the following format:
"name_of_mof": ""
"mof_formula": ""
"mof_description": [""]
"guest_species": [""]
"applications" : [""]

Do not make up answers and use the exact words from the context.
Format the output into a python list of JSONs.

"""


for i, r in enumerate(run):
    print(f"\nProcessing prompt {i}:\n")
    text_input = r["prompt"]

    docs_processor = eunomia.LoadDoc(text_input=text_input)
    # sliced_pages = docs_processor.process(
    #     chunk_size=2000, chunk_overlap=5, chunking_type="fixed-size"
    # )
    sliced_pages = docs_processor.process(
        chunk_size=300, chunk_overlap=10, chunking_type="NLTK"
    )

    Embedding_model = "text-embedding-ada-002"
    faiss_index = FAISS.from_documents(
        sliced_pages, OpenAIEmbeddings(model=Embedding_model)
    )

    # this is the MOF case

    @tool
    def read_context(input):
        """
        Input the users original prompt and get context to answer to questions.
        Always search for the answers using this tool first, don't make up answers yourself.
        """

        k = 8
        min_k = 4  # Minimum limit for k
        llm = OpenAI(temperature=0, model_name="gpt-4")
        result = eunomia.RetrievalQABypassTokenLimit(
            prompt_mof,
            faiss_index,
            k=k,
            min_k=min_k,
            llm=llm,
            search_type="mmr",
            fetch_k=50,
            chain_type="stuff",
            memory=None,
        )
        return result

    agent = Eunomia(tools=[read_context], model="gpt-4", get_cost=True, temp=0)

    results = agent.run(prompt=prompt_mof)

    # parsed_results = format_output(results)
    parsed_results = json.loads(results)

    ground_truth_json = json.loads(r["completion"].replace("\n\nEND\n\n", "").strip())

    dict = {
        "prompt": r["prompt"],
        "Eunomia": parsed_results,
        "NERRE": r["gpt3_completion"],
        "ground-truth": ground_truth_json,
    }

    with open(f"../data/NERRE/mof_results/{run_ID}/run_{run_ID}_{i}.json", "w") as f:
        json.dump(dict, f, indent=4)
