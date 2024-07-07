from openai import OpenAI
from dotenv import load_dotenv
import json
import streamlit as st
import pandas as pd
from rag import answer_question 

load_dotenv()

st.set_page_config(
    page_title="Skincare Solutions",
    page_icon="🧴",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #899F87;
    }
    .black-title {
        color: black;
        font-size: 32px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

llm = OpenAI()

function_des = [
    {
        "name": "get_skincare_issues",
        "description": "Get the list of skincare issues of a user, including the affected areas and their descriptions.",
        "parameters": {
            "type": "object",
            "properties": {
                "issues": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "area": {
                                "type": "string",
                                "description": "The area of the body affected by the skincare issue (e.g., face, nose, eyes, hair)."
                            },
                            "description": {
                                "type": "string",
                                "description": "A description of the skincare issue. Summarise the issue."
                            }
                        },
                        "required": ["area", "description"]
                    },
                    "description": "A list of skincare issues, each with an affected area and a description."
                }
            },
            "required": ["issues"],
        }
    }
]

function_des2 = [
    {
        "name": "get_skincare_products",
        "description": "Get the list of skincare products from the suggested solution",
        "parameters": {
            "type": "object",
            "properties": {
                "issues": {
                    "type": "array",
                    "products": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the product"
                            },
                        },
                        "required": ["name"]
                    },
                    "description": "A list of skin-care products, as suggested by the solution response."
                }
            },
            "required": ["issues"],
        }
    }
]

with st.sidebar:
    prompt = st.text_input("Please describe your skincare issues here")
    generate_button = st.button("Generate solutions", type="primary")

    

if generate_button:
    system_prompt = "You are an assistant that helps to extract skincare issues from a user input prompt. Extract only from the prompt."

    # Get the completion from the OpenAI API
    completion = llm.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        functions=function_des,
        function_call="auto"
    )

    output = completion.choices[0].message

    issues = json.loads(output.function_call.arguments).get("issues")

    df = pd.DataFrame(issues)
    df.columns = ["Affected area", "Description"]
    df.index = df.index + 1

   

    with st.sidebar:

      
        st.table(df)

    st.title("Skincare solutions from Organic Travellor")

    instruction = f"""
Using the information below, suggest solutions for the user's skin care issues.Solutions should be based on the affected area and description of the issue and the use case of the solution. One problem may have more than one solution.:
['name': 'Miracle Jelly Daily Facewash', 'ingredients': 'Aloe barbadensis miller (Aloe), Melaleuca alternifolia (Tea tree), Azadirachta indica (Neem), Glycerin, Vitamin E', 'features': 'Vitamin E helps fight dark spots/pigmentation & helps achieve spot free skin, Tea Tree fights pimples and purifies pores, Neem gently fades away any acne scars, Aloe soothes, repairs and brings out natural glow, Glycerin helps to moisturize the skin']
['name': 'Glow Tonic', 'ingredients': 'Hamamelis (Witch hazel), Aloe barbadensis miller (Aloe), Melaleuca alternifolia (Tea tree), Matricaria chamomilla (Chamomile), Rose extracts, Preservative', 'features': 'Tightens and reduces pore size, Replenishes and balances skins natural moisture level, Removes dead skin cells, Adds natural glow, Anti bacterial']
['name': 'Regrowth Hair Oil', 'ingredients': 'Argania spinosa (Argan), Prunus dulcis (Almond), Vitis vinifera (Grapeseed), Simmondsia chinensis (Jojoba), Persea americana (Avocado), Olea europaea L. (Olive), Ricinus communis (Castor), Juniperus virginiana (Cederwood), Lavandula (lavender), Mentha × piperita (Peppermint), Vitamin E', 'features': 'Promotes hair growth after stopping increased hair shedding\nRepairs brittle hair and split ends\nProtects against damage from UV rays\nCombats damaged/dandruff prone hair and gives them more volume\nEasy to wash off because of the lightweight formula']
['name': 'Super C: Vitamin C serum', 'ingredients': 'Sodium Ascorbyl Phosphate 12%, Hyaluronic acid, Tocopherol Acetate, Glycerol, Propanediol, Phenoxyethanol, Ethyl hexyl glycerine, Water', 'features': 'Fights free radicals, Brightens hyperpigmentation, Stimulates collagen production, Reverses oxidative damage, Diminishes the appearance of fine lines and wrinkles', 'use case': 'Suitable for all skin types, especially those with sensitive skin']
['name': 'Brightening Moisturizer', 'ingredients': 'Acrylates/C10-30 Alkyl Acrylate Crosspolymer, Deionized Water, Carbomer, Disodium EDTA, Propylene Glycol, Glycerin, Cetyl Alcohol, Cetostearyl Alcohol, Cetyl Palmitate, Stearic Acid, Kojic Acid, Glyceryl Stearate, PEG-100 Stearate, Alpha Arbutin, Sodium Ascorbyl Phosphate, C12-15 Alkyl Benzoate, Isopropyl MyristateCaprylic/Capric Triglyceride, Dimethicone, Triethanolamine, Centella Asiatica Extract, Morus Alba Bark Extract, Pyrus Malus (Apple) Fruit Extract, Broussonetia Kazinoki Root Extract, Galactoarabinan, Phenoxyethanol, Ethylhexylglycerin, Glyceryl Mono Stearate, Ceteareth-20, Sodium Hyaluronate (As Hyaluronic Acid), Wheat Germ Oil (As Contained Natural Vitamin E), Iron Oxide Yellow', 'features': 'Treats skin discoloration, Fades dark spots, Fights skin hyperpigmentation', 'use case': 'Brightening and targeting pigmentation']
['name': 'Lip Pigmentation Treatment', 'ingredients': 'White Soft Paraffin, Bees Wax, Hydrogenated Castor Oil, Shea Butter, Cocoa Butter, Jojoba Oil, Olive Oil, Octyl Methoxycinamate, Avobenzone, Carnauba Wax , Kojic Acid Dipalmitate, Alpha Arbutin, Ozokerite Wax, Caprylyl Methicone, Vitamin E, Sunflower Seed Oil, Allantoin, Lanolin', 'features': 'Reduces pigmentation around lips, Gives plump and hydrated lips', 'use case': 'Pigmented lips, dark lips']
['name': 'Glow SPF', 'ingredients': 'Broad spectrum protection, tint', 'features': 'SPF 60, universally flattering formula, lightweight, sheer coverage', 'use case': "For someone looking for a formula that doesn't irritate super sensitive skin, is lightweight, doesn't leave a white cast, and provides sheer and natural coverage"]
['name': 'B3 PRO: Pore erasing serum', 'ingredients': 'Hyaluronic Acid, water, Phenoxyethanol, Niacinamide, zinc pca, Glycerin, Propylene Glycol, Ethylhexylglycerin', 'features': 'formulated with 10% Niacinamide and 1% Zinc, minimizes the appearance of pores, refines skin texture, controls and lowers sebum, prevents pores from stretching, stable in heat and light, brightens skin, balances sebum activity, penetrates deeply into the surface, blocks harmful UV rays, suitable for all skin types']
['name': 'Quench: Brightening Serum', 'ingredients': 'Rosa canina L.(Rosehip seed), Argania spinosa (Argan), Vitis vinifera (Grapeseed), Persea americana (Avocado), Boswellia carterii (Frankincense)', 'features': 'Brightens up the skin’s natural complexion, Reduces blemish marks and dark spots, Hydrates the skin, Evens out your skin tone, Softens the skin and helps promote natural glow, The best primer before makeup!', 'use case': 'Made for brightening up your skin and targeting pigmentation, dark spots, dullness and blemish marks. Instantly adds glow and hydration, making your skin look soft and plump. Pakistan’s trusted organic option for brightening up your skin!']
['name': 'Rapid Repair: Skin Repairing Moisturiser', 'ingredients': 'Water (Aqua), Propylene Glycol, Ethoxydiglycol, Niacinamide, Rosa Mosqueta (Rose) Hip Oil, Panthenol, Glycerin , Ceramide NP, Ceramide AP, Sodium Hyaluronate, Sodium Lauroyl Lactylate, Carbomer, Xanthan Gum, , Methylparaben', 'features': 'Repairs your skins damaged barrier, Fights active acne, Minimises pore appearance, Reduces hyperpigmentation']
['name': 'Rapid Repair: Skin Repairing Moisturiser', 'ingredients': 'Water (Aqua), Propylene Glycol, Ethoxydiglycol, Niacinamide, Rosa Mosqueta (Rose) Hip Oil, Panthenol, Glycerin , Ceramide NP, Ceramide AP, Sodium Hyaluronate, Sodium Lauroyl Lactylate, Carbomer, Xanthan Gum, , Methylparaben', 'features': "Repairs skin's damaged barrier, Fights active acne, Minimises pore appearance, Reduces hyperpigmentation"]
['name': 'Pink Ribbon Travel Pouch', 'ingredients': 'N/A', 'features': 'Dimensions: 8 x 10 inches', 'use case': "The perfect travel bag for all the girls obsessed with the clean girl aesthetic. If you're obsessed with the cute Pinterest vibe then this bag is for you! It'll instantly transform your dressing table. A bag big enough to fit your skincare and makeup? YES, also cute enough that everyone around you will want to take a picture!"]
['name': 'Regrowth Hair Oil', 'ingredients': 'Argania spinosa (Argan), Prunus dulcis (Almond), Vitis vinifera (Grapeseed), Simmondsia chinensis (Jojoba), Persea americana (Avocado), Olea europaea L. (Olive), Ricinus communis (Castor), Juniperus virginiana (Cederwood), Lavandula (lavender), Mentha × piperita (Peppermint), Vitamin E', 'features': 'Promotes hair growth after stopping increased hair shedding, Repairs brittle hair and split ends, Protects against damage from UV rays, Combats damaged/dandruff prone hair and gives them more volume, Easy to wash off because of the lightweight formula'],
['name': 'COFFEE UNDER-EYE SERUM' , 'ingredients': 'Coffea arabica (Coffee beans), Prunus dulcis (Almond), Persea americana (Avocado), Vitis vinifera (Grapeseed), Vitamin E, Gold flakes', 'features': '"Decreases the appearance of dark circles, fine lines and puffiness , Greatly moisturizes and hydrates the under-eye area ,Instantly refreshes any tired looking under eye bags ,Light formula can be worn under makeup and prevent concealer creasing']

Issues are in a data-fram below:

{df.to_string(index=False)}

"""

    completion2 = llm.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Help users with thier skin care issues and provide solutions given from the list only.Do not list ingredients directly , rather explain briefly how the ingredients help for the issue while naming some of the ingredients."},
            {"role": "user", "content": instruction
            }
        ],
        
    )
    output2 = completion2.choices[0].message

    st.write(output2.content)
    completion3 = llm.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Your job is to extract the names of the product only from the solution response"},
            {"role": "user", "content": output2.content}
    ],
    functions=function_des,
    function_call="auto"

    )
    out3 = completion3.choices[0].message.content



    inp=f"Summarise the information about the following products :\n {out3} \n Talk about each product in a seperate paragprah and use a proffesional tone.Do not say 'Product being disucusses is ..'. Make sure to talk about user sentiment as well."

    res=answer_question(inp)
    st.markdown("""
<style>
.streamlit-expanderHeader {
    background-color: #0f62fe; /* Change to your desired color */
    color: white;
}
</style>
""", unsafe_allow_html=True)


  

    with st.expander("More information and user sentiments"):

        st.write(res)

   
   
       
   
        




