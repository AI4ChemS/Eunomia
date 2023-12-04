import os

import langchain

import eunomia

from .prompts import RULES, WATER_STABILITY_PROMPT
from langchain.tools import StructuredTool


class EunomiaTools:
    def __init__(
        self,
        vectorstore=None,
        tool_names=[],
    ):
        self.vectorstore = vectorstore
        self.all_tools = []
        for name in tool_names:
            tool_info = EunomiaTools.all_tools_dict.get(name, {})
            # if tool_info =='eval_justification':
            #     tool_info['description'] = f"""Always use this tool to validate justification."""
            # else:
            self.all_tools.append(
                langchain.agents.Tool(
                    name=name,
                    func=tool_info.get("function")
                    if name != "eval_justification"
                    else StructuredTool.from_function(tool_info.get("function")),
                    description=(tool_info.get("description")),
                )
            )

    def get_tools(self):
        EunomiaTools.vectorstore = self.vectorstore
        return self.all_tools

    def get_cif_from_COD(doi):
        """This tool downloads all the CIF files from Crystallography
          Open Database (COD) for a given input
        doi and returns file names for them"""
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import (
            expected_conditions as EC,
        )
        from selenium.webdriver.support.ui import WebDriverWait

        # Set up Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": os.getcwd(),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
            },
        )

        # Initialize Selenium WebDriver with the specified options
        driver = webdriver.Chrome(options=chrome_options)

        # Navigate to the website
        driver.get("http://www.crystallography.net/cod/search.html")
        doi_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "doi"))
        )
        doi_input.send_keys(doi)

        submit_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//input[@type="submit" and @name="submit" and @value="Send"]',
                )
            )
        )
        submit_button.click()

        list_of_cif_urls_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "archive of CIF files (ZIP)"))
        )
        list_of_cif_urls_link.click()

        # Define the name of the zip file and the directory to unzip
        # to
        zip_file_name = "COD.zip"
        unzip_dir = "CIF_files"

        # Wait until 'COD.zip' exists in the current directory
        import time

        while not os.path.exists("COD.zip"):
            time.sleep(1)
        if not os.path.exists(unzip_dir):
            os.mkdir(unzip_dir)

        # Close the driver
        driver.quit()
        import zipfile

        # Create the directory to unzip to if it doesn't exist
        os.makedirs(unzip_dir, exist_ok=True)

        # Unzip the file
        with zipfile.ZipFile(zip_file_name, "r") as zip_ref:
            zip_ref.extractall(unzip_dir)

        if os.path.exists(zip_file_name):
            os.remove(zip_file_name)
        return str(os.listdir(unzip_dir))

    def rename_cif(file_path):
        """
        Extract the MOF-Name associated with a target key from a CIF file and renames it.

        Parameters:
        - file_path (str): The path to the CIF file.
        """
        target_key = "_cod_data_source_block"
        if file_path.startswith("'"):
            file_path = file_path[1:-1]

        file_path = f"CIF_files/{file_path}"
        value = None
        try:
            with open(file_path, "r") as file:
                for line in file:
                    if line.startswith(target_key):
                        value = line.strip().split()[-1]
        except FileNotFoundError:
            print(f"File {file_path} not found.")

        if value is not None:
            try:
                os.rename(file_path, f"CIF_files/{value}.cif")
            except BaseException:
                if FileExistsError:
                    print("\nCIF file already exists.")

    def get_cif_from_CCDC(doi):
        import os

        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import (
            expected_conditions as EC,
        )
        from selenium.webdriver.support.ui import WebDriverWait

        # Set up Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": os.getcwd(),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
            },
        )

        # Initialize Selenium WebDriver with the specified options
        driver = webdriver.Chrome(options=chrome_options)

        # Initialize Chrome driver
        driver = webdriver.Chrome()

        # Navigate to the website
        driver.get("https://www.ccdc.cam.ac.uk/structures/")

        doi_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Doi"))
        )

        # Type the DOI into the DOI input field
        doi_input.send_keys(doi)

        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@value="Search"]'))
        )
        search_button.click()

        download_button_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "downloadOptionsButton"))
        )
        download_button_dropdown.click()

        # Now wait for the "Download all selected entries" link to be clickable
        # and then click it
        download_selected_entries_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "downloadSelected"))
        )
        download_selected_entries_link.click()
        opt_out_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "howthishelps2"))
        )
        opt_out_link.click()

        no_detail = opt_out_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "nodetailsModalRemove"))
        )
        no_detail.click()

        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "Terms"))
        )
        checkbox.click()
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "download"))
        )
        checkbox.click()

        # Close the driver
        import time

        # need to figure out the name of the cif to check if it has been
        # downloaded, for now just wait 30 seconds before quitting
        time.sleep(30)
        driver.quit()

    def eval_justification(MOF_name, justification):
        """Always use this tool to validate justification.
        This function takes MOF_name and justification as input and checks if the justification
          talks about the water stability perdiction makes sense for the MOF_name."""
        import openai

        model = "gpt-4"
        prompt = f"""
                Do the below sentences actually talk about water stability of the {MOF_name}?
                If not, try to find a better justification for that MOF in the document.

                "{justification}"

                To do this, you should check on steep uptakes, solubility in water,
                change in properties after
                  being exposed to water/steam, change in crystallinity, or mention of
                  water stability in the sentence.
                If the justification can somehow imply water stability/instability, update
                "Water stability" to Stable/Unstable
                  but lower your "Probability score".
                Do not make up answers.
                Do not consider chemical or thermal stability or stability in air as a valid reason.
                """
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message["content"]

    def read_doc(input):
        k = 9
        min_k = 2  # Minimum limit for k
        llm = langchain.OpenAI(temperature=0, model_name="gpt-4")
        result = eunomia.RetrievalQABypassTokenLimit(
            WATER_STABILITY_PROMPT,
            EunomiaTools.vectorstore,
            k=k,
            min_k=min_k,
            llm=llm,
            search_type="mmr",
            fetch_k=50,
            chain_type="stuff",
            memory=None,
        )
        return result

    def recheck_justification(MOF_name):
        input_prompt = f"""
            You are an expert chemist. The document describes the water stability properties of {MOF_name}.

            Use the following rules to determine its water stability:
            {RULES}

            Your final answer should contain the following:
            1. The water stability of the MOF.
            2. The probability score ranging between [0, 1]. This probability score shows
            how certain you are in your answer.
            3. The exact sentences without any changes from the document that justifies your decision.
              Try to find more than once sentence.
            This should be "Not provided" if you cannot find water stability.
            """
        k = 6
        min_k = 2  # Minimum limit for k
        llm = langchain.OpenAI(temperature=0, model_name="gpt-4")
        result = eunomia.RetrievalQABypassTokenLimit(
            input_prompt,
            EunomiaTools.vectorstore,
            k=k,
            min_k=min_k,
            llm=llm,
            search_type="mmr",
            fetch_k=50,
            chain_type="stuff",
            memory=None,
        )
        return result

    def create_dataset(answer):
        parsed_result = eunomia.parse_to_dict(answer)
        results_index_path = "dataset.csv"
        import pandas as pd

        list_of_dicts = []
        for mof, attributes in parsed_result.items():
            temp_dict = {"MOF contained": mof}
            temp_dict.update(
                attributes
            )  # attributes should be a dictionary of corresponding attributes for each MOF
            list_of_dicts.append(temp_dict)
        df = pd.DataFrame(list_of_dicts)

        ordered_columns = [
            "Paper id",
            "DOI",
            "MOF contained",
            "Predicted Stability",
            "Justification",
        ]
        df = df[ordered_columns]
        df.to_csv(results_index_path, index=False)

    all_tools_dict = {
        "create_dataset": {
            "function": create_dataset,
            "description": """This tool creates a csv dataset by parsing the answer.""",
        },
        "recheck_justification": {
            "function": recheck_justification,
            "description": """This tool reads the document again for the specific
              MOF_name and tries to find a better justification for its water stability. """,
        },
        "read_doc": {
            "function": read_doc,
            "description": """Input the users original prompt and get context on water
              stability of metal organic frameworks.
            Always search for the answers using this tool first, don't make up answers yourself.""",
        },
        "eval_justification": {
            "function": eval_justification,
            "description": """Always use this tool to validate justification.
            This function takes MOF_name and justification as input and checks if the justification
              talks about the water stability perdiction makes sense for the MOF_name.""",
        },
        "get_cif_from_CCDC": {
            "function": get_cif_from_CCDC,
            "description": """This tool downloads the CIF file for a given input doi from CCDC""",
        },
        "rename_cif": {
            "function": rename_cif,
            "description": """Extract the MOF-Name associated with a target key from a CIF file and renames it.
                                Parameters:
                                    - file_path (str): The path to the CIF file. """,
        },
        "get_cif_from_COD": {
            "function": get_cif_from_COD,
            "description": """This tool downloads all the CIF files from
            Crystallography Open Database (COD) for a given
              input doi and returns file names for them.""",
        },
    }
