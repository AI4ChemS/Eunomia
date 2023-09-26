import json
from typing import List

from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import OutputFixingParser, PydanticOutputParser
from pydantic import BaseModel, Field


def parse_to_dict(result, paper_id):
    """
    Parses the given result into a structured dictionary format.

    This function first defines the data model for MOF (Metal-Organic Framework)
    using the Pydantic library. It then parses the result using a parser
    tailored for the MOF model, and finally, it constructs a dictionary with
    MOF names as keys and other MOF details as values.

    Parameters:
    - result (str): The result string to be parsed.
    - paper_id (str/int): The ID associated with a particular research paper or source.

    Returns:
    - dict: A dictionary containing MOFs' names as keys and their details (predicted
            stability, score, justification, and paper id) as values.

    Raises:
    - ValueError: If there's an issue while parsing the result.

    Example Usage:
    >>> result = "some_output_string_from_model"
    >>> paper_id = "12345"
    >>> parsed_dict = parse_to_dict(result, paper_id)
    """

    class MOF(BaseModel):
        """Pydantic data model for a Metal-Organic Framework (MOF)."""

        name: str = Field(description="name of a MOF")
        stability: str = Field(
            description="choose only one: stable or unstable or not provided"
        )
        score: float = Field(description="probability score of prediction")
        justification: str = Field(description="justification for prediction")
        DOI: str = Field(description="DOI of the paper")

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
        json.loads(result, strict=False)
    except json.JSONDecodeError:
        # If not, convert it to a valid JSON string
        result = json.dumps({"dummy_key": result})
    # Try parsing the result using the enhanced parser
    try:
        parsed_result = llm_parser.parse(result)
    except ValueError as e:
        raise ValueError(f"Failed to parse MOF: {e}")

    # Construct a dictionary with MOFs' details using comprehension
    dict_response = {
        mof.name: {
            "Predicted Stability": mof.stability,
            "Score": mof.score,
            "Justification": mof.justification,
            "DOI": mof.DOI,
        }
        for mof in parsed_result.MOFs
    }

    # Update the dictionary to include the paper id for each MOF
    new_dict = {
        key: {**value, "Paper id": paper_id} for key, value in dict_response.items()
    }

    return new_dict
