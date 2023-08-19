"""Main module."""


def RetrievalQABypassTokenLimit(
    prompt,
    faiss_vectorstore,
    k,
    min_k,
    llm,
    search_type="mmr",
    fetch_k=50,
    chain_type="stuff",
    memory=None,
):
    """
    Run LangChain's RetrievalQA with reducing 'k' until a successful output is obtained without hitting the LLM's token limit.

    Parameters:
    - prompt (str): The input text for the QA chain.
    - faiss_vectorstore (object): The FAISS vector store object used to retrieve relevant documents.
    - k (int): The initial value of 'k', representing the number of documents to initially retrieve.
    - min_k (int): The minimum allowable value for 'k'. The function will stop trying if 'k' reaches this value.
    - llm (object): The language model object used to generate answers.
    - search_type (str): The type of search to perform. Defaults to "mmr": Maximum Marginal Relevance.
    - fetch_k (int): determines the amount of documents to pass to the search_type algorithm; . Defaults to 50.
    - chain_type (str): The type of chain used in RetrievalQA. Defaults to "stuff".
    - memory (object): Adds meomry to the RetrievalQA

    Returns:
    - result (object): The result obtained from the QA chain, or None if the process fails after multiple attempts
                       to avoid the token limit error.
    """
    from langchain.chains import RetrievalQA

    while k >= min_k:
        try:
            retriever = faiss_vectorstore.as_retriever(
                search_type=search_type, search_kwargs={"k": k, "fetch_k": fetch_k}
            )
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm, chain_type=chain_type, retriever=retriever, memory=memory
            )

            # Check to see if we hit the token limit
            result = qa_chain.run(prompt)
            return result  # If successful, return the result and exit the function

        except Exception as e:
            # If an error is caught, reduce the value of k and retry
            print(
                f"\nk={k} results hitting the token limit for the chosen LLM. Reducing k and retrying..."
            )
            k -= 1

    else:
        # This block will run if the loop completes without a 'break' statement
        print(
            "\nFailed to retrieve result after multiple attempts. Minimum k limit reached. Try reducing minimum k value."
        )
        return None  # Return None to indicate that the process failed
