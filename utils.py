
from sentence_transformers import SentenceTransformer, util #pinecone_key_2="1ea8f5bc-2aeb-4d98-aaa1-325acd7258a0"
from transformers import GPT2TokenizerFast
import pinecone
import openai
import streamlit as st
openai.api_key = st.secrets["a_key"]

# st.cache_resource.clear()
# @st.cache_resource
# def load_model():
#     return SentenceTransformer('all-mpnet-base-v2') #all-MiniLM-L6-v2
@st.cache_resource
def load_model_1():
    return SentenceTransformer('all-MiniLM-L12-v1')
@st.cache_resource
def load_model_2():
    return SentenceTransformer('all-MiniLM-L6-v2')
@st.cache_resource
def load_model_3():
    return SentenceTransformer('bert-base-nli-mean-tokens') 

@st.cache_resource
def load_model_4():
    return SentenceTransformer('paraphrase-MiniLM-L12-v2')

@st.cache_resource
def pincone_intit_768():
    pinecone.init(api_key=st.secrets["pinecone_key"], environment='gcp-starter') #pinecone_key="e6fe16b5-86c0-461d-8efe-5911c598122e"
    return pinecone.Index('chatbot')

@st.cache_resource
def pincone_intit_384():
    pinecone.init(api_key=st.secrets["pinecone_key_2"], environment='gcp-starter') #pinecone_key_2="1ea8f5bc-2aeb-4d98-aaa1-325acd7258a0"
    print(pinecone.list_indexes())
    return pinecone.Index('chatbot')

@st.cache_resource
def gpt2():
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    return tokenizer



# model = load_model()
model_1 = load_model_1()
model_2 = load_model_2()
model_3 = load_model_3()
j_model = load_model_4()
index = pincone_intit_768()
index_2 = pincone_intit_384()

tokenizer = gpt2()
def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

university = "toronto university"
def query_refiner(conversation, query):
    response = openai.Completion.create(
    model="gpt-3.5-turbo",
    prompt=f"""your task is helping a user to find appropriate some {university} professors . 
    Given the following user query and conversation log, formulate a question that would be the most relevant 
    to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:""",
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response['choices'][0]['text']

def query_refiner_2(query):
    prompt=f"""your task is helping a user to find appropriate some {university} professors information like their 'contacts' and 'researches' and 'url'.formulate a question that would be the most relevant to provide the user .\n\nuser request: {query}\n\nRefined Query:"""
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
    model= "gpt-3.5-turbo", #"text-davinci-003", curie 
    messages=messages,
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0].message["content"] 

def find_match(input):
    # input_em = model.encode(input).tolist()
    # result = index.query(input_em, top_k=10, includeMetadata=True)

    input_em = model_1.encode(input).tolist()
    result_1 = index_2.query(input_em, top_k=10, includeMetadata=True)

    input_em = model_2.encode(input).tolist()
    result_2 = index_2.query(input_em, top_k=10, includeMetadata=True)

    input_em = model_3.encode(input).tolist()
    result_3 = index.query(input_em, top_k=10, includeMetadata=True)
    result_list = []
    query_embedding = j_model.encode(input)
    for resul in result_2["matches"]:
        dic = {}
        passage_embedding = j_model.encode(resul["metadata"]["text"])
        dic["text"] = resul["metadata"]["text"]
        dic["score"] = float(str(util.cos_sim(query_embedding, passage_embedding)[0][0]).split("(")[1].split(")")[0])
        result_list.append(dic)

    for resul in result_1["matches"]:
        dic = {}
        passage_embedding = j_model.encode(resul["metadata"]["text"])
        dic["text"] = resul["metadata"]["text"]
        dic["score"] = float(str(util.cos_sim(query_embedding, passage_embedding)[0][0]).split("(")[1].split(")")[0])
        result_list.append(dic)

    for resul in result_3["matches"]:
        dic = {}
        passage_embedding = j_model.encode(resul["metadata"]["text"])
        dic["text"] = resul["metadata"]["text"]
        dic["score"] = float(str(util.cos_sim(query_embedding, passage_embedding)[0][0]).split("(")[1].split(")")[0])
        result_list.append(dic)

    result_list =  sorted(result_list, key=lambda d: d['score'] , reverse=True)
    result = ""
    for j in range(20):
        result = result + result_list[j]["text"] + ";;"

    i = 1
    while count_tokens("".join(result.split(";;")[:-i])) > 1000:
        i = i + 1

    result = "".join(result.split(";;")[:-i])
 
    # print("result" , result)
    return result  #['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text']+"\n"+result['matches'][2]['metadata']['text']+"\n"+result['matches'][3]['metadata']['text'] 

def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses'])-1):        
        conversation_string += "Human: "+st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: "+ st.session_state['responses'][i+1] + "\n"
    return conversation_string

def get_completion(prompt, model="gpt-3.5-turbo"): # gpt-3.5-turbo-16k
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    # print(response)
    return response 

def get_completion_cheaper(prompt, model="text-babbage-002"): #gpt-3.5-turbo-16k
    messages = [{"role": "user", "content": prompt}]
    response = openai.Completion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    # print(response)
    return response