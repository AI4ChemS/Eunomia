RULES = f"""
There are only 3 options for water stability: 
1. Stable: No change in properties after exposure to moisture or steam, soaking or boiling in water or an aqueous solution.
Retaining its porous structure in solution.
No loss of crystallinity.
insoluble in water or an aqueous solution.
Water adsorption isotherm should have a steep uptake.
Good cycling performance.

2. Unstable 
The MOF will decompose or change properties or has a change in its crystal structure after exposure/soak to a humid environment, steam or if it partially dissolves in water.
Soluble or patrially soluble in water or an aqueous solution.


3. Not provided, 
If you don't know or cannot justfy 1 or 2
"""

WATER_STABILITY_PROMPT = f"""
    You are an expert chemist. The document describes the water stability properties of a few materials including materials, crystal structures
    Metal-Organic Frameworks(MOF) or coordination polymers, coordination networks or ZIF compounds.
    Find the exact full name or chemical formula for materials (crystal structures), and their stability in water.
    As an example, sentence "UiO-66-X compounds with X = NO2, NH2, OH, CH3 and (CH3)2 show enhanced CO2 uptake", contains the five following MOFS:
    [UiO-66-NO2, UiO-66-NH2, UiO-66-OH, UiO-66-CH3, UiO-66-(CH3)2], but does not provide any information their water stability.
    Use this example to guide yourself better on finding other MOFs in the document.
    If the paper does not talk about water stability, list the full MOF names you find and set their "water stability to "Not provided".
    Report Paper's DOI.
    

    Use the following rules to determine water stability:
    {RULES}
    
    Your final answer should contain the following:
    1. The water stability of each MOF.
    2. For each mof:  a probability score ranging between [0, 1]. This probability score shows how certain you are in your answer.
    3. The exact sentences without any changes from the document that justifies your decision. Try to find more than once sentence. This should be "Not provided" if you cannot find water stability.
    4. Paper's DOI. This should be "Not provided" if you cannot find.
    """