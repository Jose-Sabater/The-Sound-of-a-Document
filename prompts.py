""" This file contains all the prompts used in the project. """

SOURCE_DECISION = {
    "system_message": "You are helpful assistant that will reply as short as possible",
    "user_messages": [
        """<Context>
    You need to find the answer to the question
        <Question> 
            {question}
        </Question>     
    and you have the following sources available:
</Context>

<Sources>
    1. CSV : contains personal information about when I was in specific countries
    2. SQL : contains temperature information in different cities around the world for the past 20 years
    3. Chroma : contains wikipedia scraped information about countries
</Sources>

<Instructions>
    Return which source you want to use for the query , only the source.
</Instructions> """
    ],
    "assistant_messages": [],
}

CSV_PROMPT = {
    "system_message": "You are a JSON machine that can only type JSON",
    "user_messages": [
        "What source would you like to use to answer the question: {question}",
        """<Context>
    Here is the csv file formatted as a list of tuples with the following elements for each tuple:
    <Format>
        Element 1: Row nr
        Element 2: Country
        Element 3: City
        Element 4: Date of visit
        Element 5: Who I was with
        Element 6: Reason for visit
    </Format>
    <Data>
        {data}
    </Data>
</Context>
<Instructions>
    Answer the question in the following format based on the data above, reply only JSON:
    <Format>
        "Answer": the answer to the question in one sentence,
        "Missing_information": True/False (if the answer is not in the data)
</Instructions>""",
    ],
    "assistant_messages": [
        "I would like to use the CSV source, which contains personal information about trips"
    ],
}

SQL_PROMPT = {
    "system_message": "You are a SQL machine that can only type SQL ",
    "user_messages": [
        """What source would you like to use to answer the question: 
        <Question>
            {question}
        </Question>
            """,
        """<Context>
    You have one table available called Temperature with the following schema.
    <Table Schema>
        (0, 'region', 'TEXT', 0, None, 0)
        (1, 'country', 'TEXT', 0, None, 0)
        (2, 'state', 'TEXT', 0, None, 0)
        (3, 'city', 'TEXT', 0, None, 0)
        (4, 'month', 'INTEGER', 0, None, 0)
        (5, 'day', 'INTEGER', 0, None, 0)
        (6, 'year', 'INTEGER', 0, None, 0)
        (7, 'avgtemperaturef', 'REAL', 0, None, 0)
        (8, 'avgtemperaturec', 'REAL', 0, None, 0)
    </Table Schema>
</Context>
<Instructions> 
   Your task is to return a SQL query to answer the question, only SQL without any other text 
</Instructions>""",
    ],
    "assistant_messages": [
        "I would like to use the SQL source, which contains temperature information in different cities around the world for the past 20 years"
    ],
}

SQL_PROMPT_FOLLOWUP = {
    "system_message": "You are helpful assistant ",
    "user_messages": [
        """What source would you like to use to answer the question: 
        <Question>
            {question}
        </Question>
            """,
        """<Context>
                From querying the SQL database witht he following query:
                <Query>
                    {query}
                </Query>
                You get the following result:
                <Result>
                    {result}
                </Result>
            </Context>
            <Instructions>
                Answer the question in the following format based on the data above, reply only JSON:
                <Format>
                    "Answer": the answer to the question in one sentence,
                    "Missing_information": True/False (if the answer is not in the data)
            </Instructions>""",
    ],
    "assistant_messages": [
        "I would like to use the SQL source, which contains temperature information in different cities around the world for the past 20 years"
    ],
}


CHROMA_PROMPT = {
    "system_message": "You are a JSON machine that can only type JSON",
    "user_messages": [
        """What source would you like to use to answer the question: 
        <Question>
            {question}
        </Question>
            """,
        """<Context>
    You have the following information available from the Chroma database:
    <Data>
        {data}
    </Data>

</Context>
<Instructions>
    Answer the question in the following format based on the data above, reply only JSON:
    <Format>
        "Answer": the answer to the question in one sentence,
        "Missing_information": True/False (if the answer is not in the data)
</Instructions>""",
    ],
    "assistant_messages": [
        "I would like to use the Chroma source, which contains wikipedia scraped information about countries"
    ],
}
