import os
from langchain.agents import Tool, tool


@tool
def get_cif_from_COD(doi):
    '''This tool downloads all the CIF files from Crystallography Open Database (COD) for a given input doi and returns file names for them'''
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
        # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    
    # Initialize Selenium WebDriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)
    
    # Navigate to the website
    driver.get("http://www.crystallography.net/cod/search.html")
    doi_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'doi'))
    )
    doi_input.send_keys(doi)
    
    submit_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//input[@type="submit" and @name="submit" and @value="Send"]'))
    )
    submit_button.click()
    
    list_of_cif_urls_link = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.LINK_TEXT, 'archive of CIF files (ZIP)'))
    )
    list_of_cif_urls_link.click()


    # Define the name of the zip file and the directory to unzip to
    zip_file_name = 'COD.zip'
    unzip_dir = 'CIF_files'
    
    # Wait until 'COD.zip' exists in the current directory
    import time
    while not os.path.exists('COD.zip'):
        time.sleep(1)
    if not os.path.exists(unzip_dir):
        os.mkdir(unzip_dir)

    
    # Close the driver
    driver.quit()
    import zipfile
    
    # Create the directory to unzip to if it doesn't exist
    os.makedirs(unzip_dir, exist_ok=True)
    
    # Unzip the file
    with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
        zip_ref.extractall(unzip_dir)

    if os.path.exists(zip_file_name):
        os.remove(zip_file_name)
    return str(os.listdir(unzip_dir))
    

@tool
def rename_cif(file_path):
    """
    Extract the MOF-Name associated with a target key from a CIF file and renames it.

    Parameters:
    - file_path (str): The path to the CIF file. 
    """
    target_key ='_cod_data_source_block'
    if file_path.startswith("'"):
        file_path = file_path[1:-1]
    
    file_path = f"CIF_files/{file_path}"
    value = None
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith(target_key):
                    value = line.strip().split()[-1]
    except FileNotFoundError:
        print(f"File {file_path} not found.")

    if value is not None:
        try:
            os.rename(file_path, f"CIF_files/{value}.cif")
        except:
            if FileExistsError:
                print('\nCIF file already exists.')
                pass



@tool
def get_cif_from_ccdc(doi):
    '''This tool downloads the CIF file for a given input doi from CCDC'''
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import os
    
        # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    
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
    
    # Now wait for the "Download all selected entries" link to be clickable and then click it
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
    # need to figure out the name of the cif to check if it has been downloaded, for now just wait 30 seconds before quitting
    time.sleep(30)
    driver.quit()
