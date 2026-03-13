from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import base64

API_KEY  = "sk-hc-v1-d8fc9e3a93924a1a9033b783cec593ad6b6f572b141f43eaa80d03f0934545f7"
BASE_URL = "https://ai.hackclub.com/proxy/v1"

embeddings = OpenAIEmbeddings(
    model="openai/text-embedding-3-small",
    api_key=API_KEY,
    base_url=BASE_URL
)

pdf = "agr.pdf"

pages  = PyPDFLoader(pdf).load()
chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(pages)

data_rag = Chroma.from_documents(chunks, embedding=embeddings, persist_directory="./db")


def get_context(query):
    docs  = data_rag.as_retriever(search_kwargs={"k": 5}).invoke(query)
    parts = []
    for doc in docs:
        parts.append(f"{doc.page_content}")
    return "\n\n".join(parts) if parts else "No context found."


llm = ChatOpenAI(
    model="gemini-2.5-flash",
    base_url=BASE_URL,
    api_key=API_KEY
)

llm_image = ChatOpenAI(
    model="google/gemini-2.5-flash-image",
    base_url=BASE_URL,
    api_key=API_KEY
)

def path(image_path):
    return image_path


image_url=""



import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model('potato_model.h5')


CLASS_NAMES = ['Potato_Early___blight', 'Potato___healthy', 'Potato___Late_blight']
IMAGE_SIZE  = (200, 200)


def predict_image(img_path):
    img = tf.keras.utils.load_img(img_path, target_size=IMAGE_SIZE)

    img_array = tf.keras.utils.img_to_array(img)

    img_array = tf.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)

    predicted_index = np.argmax(predictions[0])

    predicted_class = CLASS_NAMES[predicted_index]

    confidence = predictions[0][predicted_index] * 100

    print(f"Prediction : {predicted_class}")
    print(f"Confidence : {confidence:.2f}%")
















cnn_prediction=""


messages = [
    SystemMessage(content=f"""
You are a senior plant pathologist AI with deep expertise in fungal and bacterial crop diseases.
Your analysis is used in a real agricultural AI system — accuracy and clarity are critical.

You will receive:
- A crop leaf image
- A CNN model prediction (not always correct — treat it as a hint, not a fact)

CNN Prediction: {cnn_prediction}

Analyze the image independently first, then consider the CNN result.
If they match → strengthen your confidence.
If they conflict → trust your visual analysis more, but mention the disagreement.

Respond in this EXACT format, nothing more, nothing less:

SYMPTOMS: Describe precisely what you observe on the leaf — color changes, necrotic spots, lesions, texture abnormalities, spread pattern. Be specific and scientific. (2-3 sentences)

CNN ALIGNMENT: State "Consistent" or "Inconsistent" — then in one sentence explain whether the CNN prediction matches your visual findings and why.

FINAL DECISION: Choose exactly one → Early Blight / Late Blight / Healthy

CONFIDENCE: Your own confidence in your decision → High / Medium / Low — and one reason why.
"""),

    HumanMessage(content=[
        {
            "type": "text",
            "text": "Examine this crop leaf image with full diagnostic precision. Apply your expertise and follow the format exactly."
        },
        {
            "type": "image_url",
            "image_url": {"url": image_url}
        },
    ])]





def response(image_path):

    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    cnn_prediction = predict_image(image_path)

    messages = [
        SystemMessage(content=f"""
    You are a senior plant pathologist AI.

CNN Prediction: {cnn_prediction}

Respond in this format:

SYMPTOMS:
CNN ALIGNMENT:
FINAL DECISION:
CONFIDENCE:
"""),

        HumanMessage(content=[
            {
                "type": "text",
                "text": "Analyze this potato leaf image."
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_b64
                }
            }
        ])
    ]

    response_message = llm_image.invoke(messages)

    return response_message.content

response_image_llm=response("TEST/early/21ca5caf-147b-4a1a-a2da-edfc1c81b62e___RS_Early.B 8926.JPG")
retriever_content=get_context(response_image_llm)




final_messages = [
    SystemMessage(content="""
You are the AI Farming Health Shield — an elite agricultural AI advisor 
deployed to protect crops and secure food supply for farmers in Egypt and developing countries.

You will receive two inputs:
1. VISUAL ANALYSIS — from a plant pathologist AI that examined the leaf image
2. SCIENTIFIC CONTEXT — retrieved from a peer-reviewed research paper on plant diseases

Your job is to synthesize both into one powerful, clear, actionable report for the farmer.

Rules:
- Trust the visual analysis as your primary source
- Use the scientific context to back up your recommendations with real knowledge
- Write like you are talking directly to the farmer — simple, confident, urgent when needed
- Never be vague — give specific names (organisms, compounds, products)

Respond in this EXACT structure:

DIAGNOSIS
What disease was found, how severe, and what stage.

IMMEDIATE ACTIONS
2-3 things the farmer must do TODAY — ranked by priority.

TREATMENT PLAN
- Biocontrol: specific organism or natural compound to use
- Chemical: specific fungicide/pesticide only if stage is Moderate or Advanced

PREVENTION
2 long-term strategies to stop this from happening again.

EXPECTED OUTCOME
If treated now → estimated yield saved.
If ignored → estimated yield loss and timeline.
"""),

    HumanMessage(content=f"""
=== VISUAL ANALYSIS FROM IMAGE LLM ===
{response_image_llm}

=== SCIENTIFIC CONTEXT FROM RESEARCH PAPER ===
{retriever_content}

Generate the full farmer recommendation report now.
""")
]

final_response = llm.invoke(final_messages)
print(final_response.content.strip())
