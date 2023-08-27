from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message

import os
import yaml
from streamlit_option_menu import option_menu
from langchain.agents import create_json_agent, AgentExecutor
from langchain.agents.agent_toolkits import JsonToolkit
from langchain.chains import LLMChain
from langchain.llms.openai import OpenAI
from langchain.requests import TextRequestsWrapper
from langchain.tools.json.tool import JsonSpec
import streamlit.components.v1 as com

st.set_page_config(page_title="profesearch", page_icon=None, layout="wide", initial_sidebar_state="collapsed", menu_items=None)
from utils import *
# @st.cache_resource  # 👈 Add the caching decorator

# st.image(image="Toronto_1.png",use_column_width="auto")
# navbar = option_menu(
#     menu_title=None,
#     options= ["browse ai" , "table" , "about"],
#     icons=  ["robot" , "table", "book"],
#     menu_icon="cast",
#     orientation="horizontal",
#     default_index=0,

#                 )

main_html = """<html>
    <head>
        <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
        <style>
            /* resets */
            body { margin:0px; padding:0px; }

            /* main */
            header {
                height: 360px;
                z-index: 10;
            }
            .header-banner {
                background-color: #333;
                background-image: url('https://www.utsc.utoronto.ca/hr/sites/utsc.utoronto.ca.hr/files/styles/3_1_full_width_banner/public/images/page/UofT7685_20140909_UTSCStudentsWalktoClass_9902-lpr.jpeg?h=9df75cb1&itok=bG9DYg6R');
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;
                width: 100%;
                height: 300px;
            }

            header h1 {
                background-color: rgba(18,72,120, 0.8);
                color: #fff;
                padding: 0 1rem;
                position: absolute;
                top: 2rem; 
                left: 2rem;
            }

            .fixed-header {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%; 
            }

            nav {
                width: 100%;
                height: 60px;
                background: #292f36;
                postion: fixed;
                z-index: 10;
            }

            nav div {
                color: white;
                font-size: 2rem;
                line-height: 60px;
                position: absolute;
                top: 0;
                left: 2%;
                visibility: hidden;
            }
            .visible-title {
                visibility: visible;
            }

            nav ul { 
                list-style-type: none;
                margin: 0 2% auto 0;
                padding-left: 0;
                text-align: right;
                max-width: 100%;
            }
            nav ul li { 
                display: inline-block; 
                line-height: 60px;
                margin-left: 10px;
            }
            nav ul li a {
                text-decoration: none; 
                color: #a9abae;
            }

            /* demo content */
            body { 
                color: #292f36;
                font-family: helvetica;
                line-height: 1.6;
            }
            .content{ 
                margin: 0 auto;
                padding: 4rem 0;
                width: 960px;
                max-width: 100%;
            }
            article {
                float: left;
                width: 720px;
            }
            article p:first-of-type {
                margin-top: 0;
            }
            aside {
                float: right;
                width: 120px;
            }
            p img {
                max-width: 100%;
            }

            @media only screen and (max-width: 960px) {
                .content{ 
                    padding: 2rem 0;
                }
                article {
                    float: none;
                    margin: 0 auto;
                    width: 96%;
                }
                article:last-of-type {  
                    margin-bottom: 3rem;
                }
                aside {  
                    float: none;
                    text-align: center;
                    width: 100%;
                }
            }

        </style>
    </head>
    <body>
        <header>
            <div class="header-banner">
                <h1>profesearch</h1>
            </div>
            <div class="clear"></div>
            <nav>
                <div class="site-title">Finland</div>
                <ul>
                    <li><a href="/archive">Archive</a></li>
                    <li><a href="/events">Events</a></li>
                    <li><a href="/contact">Contact</a></li>
                <ul>
            </nav>
        </header>
        <script>
            $(window).scroll(function(){
            if ($(window).scrollTop() >= 300) {
                $('nav').addClass('fixed-header');
                $('nav div').addClass('visible-title');
            }
            else {
                $('nav').removeClass('fixed-header');
                $('nav div').removeClass('visible-title');
            }
        });
        </script>
    </body>
</html>"""
style_css = """
header.css-18ni7ap.ezrtsby2{
    visibility: hidden;

}

div.block-container.css-z5fcl4.ea3mdgi4
{
    padding-top: 0px;
    padding-left: 0px;
    padding-right: 10px;

}
"""
# if navbar == "table":
# with open('index.html') as mainHTML:
#     com.html(mainHTML.read() ,height=360)
com.html(main_html , height=360)
# with open("style.css") as style:
#     # com.html(f"<style>{style.read()}</style>" , height=0)
#      st.markdown(f"<style>{style.read()}</style>" , unsafe_allow_html=True)
st.markdown(f"<style>{style_css}</style>" , unsafe_allow_html=True)
st.write("""
# Chatbot ProfeSearch
         
Connecting Graduate Students with Professors
""")

# with open('main.html') as mainHTML:
#     com.html(mainHTML.read() , height=0)
# with open('main.html') as mainHTML:
#     st.markdown(style.read() , unsafe_allow_html=True)

# openai.api_key = st.secrets["a_key"]
model = load_model()
# os.environ["OPENAI_API_KEY"] = st.secrets["a_key"]
 
     
# # #####################################################json
# with open("simpl_inf.yml") as f:
#     data = yaml.load(f, Loader=yaml.FullLoader)
# json_spec = JsonSpec(dict_=data, max_value_length=400)
# json_toolkit = JsonToolkit(spec=json_spec)

# json_agent_executor = create_json_agent(
#     llm=ChatOpenAI(model_name="text-babbage-001", openai_api_key= st.secrets["a_key"],max_tokens=100) #text-babbage-002
#     , toolkit=json_toolkit, verbose=True
# )

# # ######################################################



# # pinecone.init(api_key=st.secrets["pinecone_key"], environment='gcp-starter')
# # index = pinecone.Index('chatbot')
index = pincone_intit()



# # st.header("prof")
        
# # st.subheader("Chatbot ProfeSearch \n Connecting Graduate Students with Professors")
# com.html( """<p>hear is a robot that can help you </p>""",width=260, height=50)
# if 'responses' not in st.session_state:
#     st.session_state['responses'] = ["How can I assist you?"]

# if 'requests' not in st.session_state:
#     st.session_state['requests'] = []

# llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key= st.secrets["a_key"])

# if 'buffer_memory' not in st.session_state:
#             st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)




# system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, 
# and if the answer is not contained within the text below, say 'I don't know'""")


# human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

# prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

# conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

def res(input):

    return f"""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    <div class="card">
    <div class="card-body">
    <p>{input}</p>
    </div>
    </div>
    <script>
     var paragraf = document.getElementsByTagName("p")
     paragraf.addClass("card-text")
     var h5_ = document.getElementsByTagName("h5")
     h5_.addClass("card-title")
    </script>
"""

query = st.text_input("Query: ", key="input" )
if query:
    with st.spinner("typing..."):
        refined_query = query_refiner_2(query) # convert user query to a nice query
        st.write(refined_query)
        input_em = model.encode(refined_query).tolist()
        # input_em = model.encode(query).tolist()
        result = index.query(input_em, top_k=6, includeMetadata=True)
        print("result" , result)
# #############################################################################################################cleaning data
        # for i in range(0 , len(result['matches'])):
        #     # result['matches'][i]['metadata']['text'] = result['matches'][i]['metadata']['text'].replace("\\n" ," ")
        #     # # result['matches'][i]['metadata']['text'] = result['matches'][i]['metadata']['text'].replace("https://" ,"")
        #     # result['matches'][i]['metadata']['text'] = result['matches'][i]['metadata']['text'].replace("page_url" ,"url")
        #     # result['matches'][i]['metadata']['text'] = result['matches'][i]['metadata']['text'].replace(", " ,",")
        #     # result['matches'][i]['metadata']['text'] = result['matches'][i]['metadata']['text'].replace(": " ,":")
        #     # result['matches'][i]['metadata']['text'] = result['matches'][i]['metadata']['text'].replace(". " ,".")


        #     if "{" in result['matches'][i]['metadata']['text']:
        #         if len(result['matches'][i]['metadata']['text'].split("{" , 1)[1]) > len(result['matches'][i]['metadata']['text'].split("{" , 1)[0]):
        #             result['matches'][i]['metadata']['text'] = "{"+result['matches'][i]['metadata']['text'].split("{" , 1)[1]
        #         else:
        #             result['matches'][i]['metadata']['text'] = "{"+result['matches'][i]['metadata']['text'].split("{" , 1)[0]
            
# ##########################################################################################################################
        context = result['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text'] 
        context2 =result['matches'][2]['metadata']['text']+"\n"+result['matches'][3]['metadata']['text']
        context3 =result['matches'][4]['metadata']['text']+"\n"+result['matches'][5]['metadata']['text']
        # print("context" , context)
        # response_json = json_agent_executor.run(query ) # json
        # print("json: ",response_json)
        # babbage_promt = f"""answer user request based Text.\nText:\n```{context2 + context3}``` \nuser request:```{refined_query}```"""

        prompt = f"""your task is helping a user to find appropriate a list of professors interested in the specified research area . just anser based Text.\n\n Text:\n```{context}``` \n\n user request:\n ```{refined_query}```"""
        # babbage_response = get_completion(babbage_promt)
        response = get_completion(prompt)
        #print(response)
        st.markdown(res(response.choices[0].message["content"]), unsafe_allow_html=True)
        # st.markdown(res(context + "\n" + context2 + "\n" + context3), unsafe_allow_html=True)
        # st.markdown(res(response_json), unsafe_allow_html=True)


# # container for chat history
# response_container = st.container()
# # container for text box
# textcontainer = st.container()


# with textcontainer:
#     s = st.text_area(label="Query:",key="text_area_key",height=2)
#     query = st.text_input("Query: ", key="input" )
#     if query:
#         with st.spinner("typing..."):
#             conversation_string = get_conversation_string()
#             # st.code(conversation_string)
#             refined_query = query_refiner(conversation_string, query) # convert user query to a nice query
#             st.subheader("Refined Query:")
#             st.write(refined_query)
#             print("refined" ,refined_query)

#             # context = find_match(refined_query)
#             input_em = model.encode(refined_query).tolist()
#             result = index.query(input_em, top_k=8, includeMetadata=True)
#             #############################################################################################################cleaning data
#             for i in range(0 , len(result['matches'])):
#                 result['matches'][i]['metadata']['text'] = result['matches'][i]['metadata']['text'].replace("\\n" ," ")
#                 result['matches'][i]['metadata']['text'] = result['matches'][i]['metadata']['text'].replace("https://" ,"")
#                 result['matches'][i]['metadata']['text'] = result['matches'][i]['metadata']['text'].replace("page_url" ,"url")
#                 result['matches'][i]['metadata']['text'] = result['matches'][i]['metadata']['text'].replace(", " ,",")
#                 result['matches'][i]['metadata']['text'] = result['matches'][i]['metadata']['text'].replace(": " ,":")
#                 result['matches'][i]['metadata']['text'] = result['matches'][i]['metadata']['text'].replace(". " ,".")


#                 if "{" in result['matches'][i]['metadata']['text']:
#                     if len(result['matches'][i]['metadata']['text'].split("{" , 1)[1]) > len(result['matches'][i]['metadata']['text'].split("{" , 1)[0]):
#                         result['matches'][i]['metadata']['text'] = "{"+result['matches'][i]['metadata']['text'].split("{" , 1)[1]
#                     else:
#                         result['matches'][i]['metadata']['text'] = "{"+result['matches'][i]['metadata']['text'].split("{" , 1)[0]
#             ##########################################################################################################################

#             context = result['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text']
#             context2 =result['matches'][2]['metadata']['text']+"\n"+result['matches'][3]['metadata']['text']
#             context3 = result['matches'][4]['metadata']['text']+"\n"+result['matches'][5]['metadata']['text']
#             context4 =result['matches'][6]['metadata']['text']+"\n"+result['matches'][7]['metadata']['text']

#             print("result" , result)
#             # print(context)  # sum of results
#             response1 = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{refined_query}") #convert response "the problem"
#             print("response1" , response1) 
#             response2 = conversation.predict(input=f"Context:\n {context2} \n\n Query:\n{refined_query}")
#             print("response2" , response2) 
#             response3 = conversation.predict(input=f"Context:\n {context3} \n\n Query:\n{refined_query}")
#             print("response3" , response3) 
#             response4 = conversation.predict(input=f"Context:\n {context4} \n\n Query:\n{refined_query}")
#             print("response4" , response4) 

#             # response5 = json_agent_executor.run(refined_query) # json
#             # print("response5" , response5) 

#             # response = conversation.predict(input=f"Context:\n {response1+response2+response3} \n\n Query:\n{query}")
#             prompt = f"""your task is helping a user to find appropriate professor . just anser based on provided Text.do not add  anything other than provided Text:\n```{response1+response2+response3 +response4 }``` \n\nuser request:\n ```{refined_query}```"""
#             response = get_completion(prompt)

#             # print("response" , response.choices[0].message["content"])  
        # st.session_state.requests.append(query)
#         st.session_state.responses.append(response.choices[0].message["content"]) 
        

# with response_container:
#     if st.session_state['responses']:

#         for i in range(len(st.session_state['responses'])):
#             message(st.session_state['responses'][i],key=str(i))
#             if i < len(st.session_state['requests']):
#                 message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')

          