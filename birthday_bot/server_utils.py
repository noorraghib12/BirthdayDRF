import regex as re
import os
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv
load_dotenv()
import re
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from datetime import datetime,timedelta
from datetime import datetime
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.output_parsers import BooleanOutputParser
from langchain.schema.runnable import RunnableMap,RunnablePassthrough,RunnableLambda
from pydantic import BaseModel,Field,model_validator
from langchain.pydantic_v1 import validator
from langchain.output_parsers import DatetimeOutputParser
from typing import List
import regex as re
from PyPDF2 import PdfReader
from langchain_community.document_loaders import Docx2txtLoader
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r'google_cred.json'
from google.cloud import translate_v2 
from itertools import repeat
from bltk.langtools import Tokenizer as BnTokenizer
import regex as re
import concurrent
translate_model=translate_v2.Client()
bn_tokenizer = BnTokenizer()
embeddings=OpenAIEmbeddings() 
llm = OpenAI(model_name="text-davinci-003")


def fetch_bangla_text(str_):
    n=str_.find(':')
    return (str_[:n],str_[n+1:])



def split_date_text(elem):
    if isinstance(elem,str):
        colon_pat=r'(?<=(?:January|February|March|April|July|August|September|November|December).*[0-9]{4}):'
        # return re.split(colon_pat,elem)
        date_,events_=re.split(colon_pat,elem)
        return date_,events_

        
def split_bengali_sentences(text):
    # Define the regex pattern
    sentence_pattern = r'(?:[।?!]|[\n\r])+[\s\u200B]*|[\n\r]+'

    # Apply the regex pattern to split sentences
    sentences = re.split(sentence_pattern, text)

    # Remove any empty strings from the list
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    return sentences  



def bangla_in_query_check(query):
    init_len=len(query)
    bn_in_query="".join(i for i in query if i in ["।"] or 2432 <= ord(i) <= 2559 or ord(i)== 32)
    if len(bn_in_query)<0.10*init_len:
        return 'english'
    elif len(bn_in_query)>=0.80*init_len:
        return 'bangla'
        
    else:
        raise ValueError('Please make sure query is in either Bengali or English or a sentence with majority English or Bengali.')
    


# with concurrent.futures.ThreadPoolExecutor() as executor:
#     futures = []
#     for url in wiki_page_urls:
#         futures.append(executor.submit(get_wiki_page_existence, wiki_page_url=url))
#     for future in concurrent.futures.as_completed(futures):
#         print(future.result())


def para_translate(para):
    date_,events_bn=fetch_bangla_text(para)
    events_bn=split_bengali_sentences(events_bn)
    return translate_model.translate([date_]+events_bn)





def list_from_paragraph(response):
    
    event_list=[]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures=[]
        for para in response:
            futures.append(executor.submit(para_translate,para=para))

    for future in concurrent.futures.as_completed(futures):
        inp_list_translated=future.result()
        date_=inp_list_translated[0]['translatedText']
        event_bn=[i['input'] for i in inp_list_translated[1:]]
        event_en=[i['translatedText'] for i in inp_list_translated[1:]]
        for i in range(len(event_bn)):
            
        # date_,events_en,events_bn=inp_list_translated['translatedText'][0],inp_list_translated['translatedText'][1:],inp_list_translated['input'][1:]


        
        
        # date_,event_en=split_date_text(para['translatedText'])
        # event_en=[i for i in event_en.split('.') if len(i)!=0]
        # event_bn=fetch_bangla_text(para['input'])[1]
        # event_bn_list=split_bengali_sentences(event_bn)
            event_list.append(
                {'date':date_,
                'event_bn':event_bn[i],
                'event_en':event_en[i],
                }
            )
        if not event_list[-1]['same_parse']:
            event_list[-1]['diff']=para['input']
    return event_list
        



def regex_text_splitter(pdf_path='test_grey (1).pdf', deli_='\n\n'):


    if isinstance(pdf_path,str):
        if 'pdf' in pdf_path[-4:]:
            reader=PdfReader(pdf_path)
            text=""
            for page in reader.pages:
                text+=page.extract_text()
                    
        
    
        else:
            loader=Docx2txtLoader(pdf_path)
            data=loader.load()
            text=""
            for page in data:
                text+=page.page_content
    
        split_patt=r'((?:জানুয়ারি|ফেব্রুয়ারি|মার্চ|এপ্রিল|জুলাই|আগস্ট|সেপ্টেম্বর|নভেম্বর|ডিসেম্বর))'              
        text=re.sub(split_patt,r'{}\1'.format(deli_),text)
        inp_list=[i.strip() for i in text.split(deli_) if (i.strip() and i.find(':')!=-1)]
        
        inp_pretranslate=[i.strip().replace('\n', r"") for i in inp_list]
        # inp_list_translated=translate_model.translate(inp_pretranslate)
        final_list=list_from_paragraph(inp_pretranslate)
        return final_list
    else:

        extended_list=[]
        for pdf in pdf_path:
            extended_list.extend(regex_text_splitter(pdf,deli_=deli_))
    
        return extended_list
    


class eventBoolRetrieve(BaseModel):
    event_truth: bool =Field(description="Validatition of whether the Alleged Event ever truly occured according to the given list of Historical Events")
    event_date: datetime =Field(description= "The date fetched from the retrieved event")
    
    @model_validator(mode='after')
    def vali_date(self):
        if self.event_truth==False:
            self.event_date=None
        return self


event_verify_prompt=PromptTemplate(template="""Each sentence is a specific historical event in the Historical Events. Given the list of historical events, determine if the alleged event ever truly occurred. Answer only in boolean format. If you're not sure, just reply with 'False'.
Historical Events: {retrieved}      

Alleged Event: {queried}
""",
input_variables=['queried','retrieved'],
)
bool_parse=BooleanOutputParser(true_val='True',false_val='False')






def convert2days(string):
    days_dict={'month':30,'week':7,'year':365,'day':1}
    date_pat=re.compile(r'((?P<year>\d* )(?:year|YEAR|years|YEARS|))?(?: and |, | )?((?P<month>\d* )(?:month|MONTH|months|MONTHS))?(?: and |, | )?((?P<week>\d* )(?:week|WEEK|weeks|WEEKS))?(?: and |, | )?((?P<day>\d* )(?:day|DAY|days|DAYS|))')
    regx=re.match(date_pat,string)
    res={key:int(value) for key,value in regx.groupdict().items() if value is not None}
    tot_days=sum([res[key]*days_dict[key] for key in res.keys()])
    return timedelta(days=tot_days)

def get_date(event,mode):
    if mode=='db' and event:
        date_str=(event[0].page_content).split(':')[0]
        date_str=date_str.split(" (")[0]
        return_date=datetime.strptime(date_str.strip(),"%B %d, %Y")
        return return_date
    elif mode=='input':
        date_,event_= event.split(':')
        date_=date_.split(" (")[0]
        return datetime.strptime(date_.strip(),"%B %d, %Y"),event_
    else:
        date_str=None
        return date_str
    


def get_final_date(d_):
    if not d_['event_truth']:
        return "Sorry, this event never occurred, or it is not within our event database"
    if d_['before_after']=='after':
        return (d_['event_date']+d_['delta']).strftime("%B %d, %Y") 
    else:
        return (d_['event_date']-d_['delta']).strftime("%B %d, %Y")




#main base class for fetched event data
class eventDetails(BaseModel):
    ''' Used to extract important information related to an individual's birthday'''
    time_span:str = Field(description="Timespan from the event that occurs before or after the birth of person as mentioned in the query")
    before_after:str =Field(description="Whether the birth of the person in question happened before or after the event")
    event: str = Field(description="Description of the event related to the person's birthday")

    @validator('time_span',allow_reuse=True)
    def span_validate(cls,field):
        return convert2days(field)

#main tagging and extraction function
functions=[
    convert_pydantic_to_openai_function(eventDetails, name='event_details'),
]
# main conversation prompt
prompt=ChatPromptTemplate.from_messages([
    ('system',"You are an assistant to a confectionary store currently working on finding people's birthdays based on certain events that happened before or after them. Refer to 'event_details' function to extract information whenever you are asked about inferring someone's birthdays. Answer conventional questions with conventional replies. Do not make up false information. If you dont know something, simply say you dont know. If you cant find enough context to extract required information from birth date related queries, say that there isnt enough context to infer birthday. In the case you cant get all the required parameters during function calls, say there wasnt enough context."),
    ('user', "{statement}")]
)

json_parser=JsonOutputFunctionsParser()

#chain for extracting birthdays from queries and retrieved documents
vectorstore_dir="./static/vectorstore_db"
db=Chroma(persist_directory=vectorstore_dir,embedding_function=embeddings)


def get_main_chain(db:Chroma=db):
    retriever=db.as_retriever(search_type='similarity_score_threshold',search_kwargs={'score_threshold':0.75, 'k':1})
    model=ChatOpenAI().bind(functions=functions) 
    event_bool_chain= event_verify_prompt | llm | bool_parse
    chain2= json_parser | RunnableMap(
        {
            'retrieved': lambda x: retriever.get_relevant_documents(x['event']),
            "queried": lambda x: x['event'],
            'delta': lambda x: convert2days(x['time_span']),
            'before_after':lambda x:x['before_after']    
        }
    ) | RunnablePassthrough.assign(event_date=lambda x:get_date(x['retrieved'],mode='db')) | RunnablePassthrough.assign(event_truth=event_bool_chain)| get_final_date



    chain=RunnableMap({'statement':lambda x:translate_model.translate(x,target_language='en')['translatedText']}) | prompt | model | RunnableLambda(lambda x : chain2 if len(x.content)==0 else x.content) 
    return chain

if __name__=="__main__":
    chain=get_main_chain()
    print(chain.invoke("What did you eat today ?"))
    print(chain.invoke("পৌষ ১৯৭৯ এ মেহেরপুরে অনশন শুরু হওয়ার ১ বছর, ২ মাস ১০ দিন আগে জাহিদের জন্ম হয়। সে কখন জন্মগ্রহণ করেছিল ?"))