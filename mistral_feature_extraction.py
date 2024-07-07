
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory



# Define the Person class
class Person(BaseModel):
    """Information about skin care problems of a person"""
    issue_area: Optional[str] = Field(default=None, description="The area of problem, such as face, hair, eyes, or scalp, etc.")
    issue_desc: Optional[str] = Field(
        default=None, description="The description of skin care problem"
    )

# Define the Data class
class Data(BaseModel):
    """Extracted data about skincare problem"""
    people: List[Person]

# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value. "
            "You will work to extract information about different skin care problems of a user."
            "One attribute will only have one item."
        ),
        ("human", "{text}"),
    ]
)

# Set up the language model
text = "i have pigmentation on my lips and i have hairfall. i also have lines on my neck and have uneven face skin tone"
llm = ChatMistralAI(model="mistral-large-latest", temperature=0, api_key="")
runnable = prompt | llm.with_structured_output(schema=Data)

output = runnable.invoke({"text": text})
print(output)
output_dict = output.dict()

# Display output or process it further as needed
st.json(output_dict)



   
