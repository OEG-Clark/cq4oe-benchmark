from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

import os
import json
from typing import List
import time
import argparse
from pydantic import BaseModel, Field
import glob
import xml.etree.ElementTree as ET
from rdflib import Graph



def load_json(file_path):
    with open(file_path, "rb") as f:
        data = json.load(f)
    return data

class Answer(BaseModel):
    reason: str = Field(description="The reasoning process of the entire generation")
    OWL: str = Field(description="The OWL source code representing the ontology")
   
prompt_template = "Answer the user query based on the provided CQs(competency questions).  \n{format_instructions} \nQuery: {query}\n CQs: {list_of_CQs}"
    
def run_llm(llm, parser, query, list_of_CQs):
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["query", "list_of_CQs"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    chain = prompt | llm
    return chain.invoke({"query": query, "list_of_CQs": list_of_CQs})

def is_owl_file(file_path):
    """
 check the root node is RDF/XML
    """
    try:
        tree = ET.parse(file_path)
        print(tree)
        root = tree.getroot()
        # Check if the root element is RDF and has the correct namespace
        return root.tag.endswith('RDF')
    except ET.ParseError:
        return False
    
def convert_files_to_owl(path, save_file, new_ext='.owl', rdf_format='xml'):

    if os.path.isfile(path):
        files = [path]
    elif os.path.isdir(path):
        files = glob.glob(os.path.join(path, "*"))
    else:
        raise FileNotFoundError(f"path not found: {path}")

    for file_path in files:
        if is_owl_file(file_path):
            try:
                g = Graph()
                g.parse(file_path, format=rdf_format)
                #also consider the file has the \n \r in the file document
                for stmt in g:
                    pass    
                g.serialize(destination=save_file, format=rdf_format)
                print(f"convert done: {file_path} -> {save_file}")
            except Exception as e:
                print(f"convert not done ({file_path}): {e}")
        else:
            print(f"not owl: {file_path}")

def get_parser():
    parser = argparse.ArgumentParser(description="LLM-Generated Ontology Baseline")
    parser.add_argument('--user_key', default="sk-gFjuDQ59BhaeO50HXC8AYrcAyPCMd2hHrl7U0GxDzTwCsd5b", help="Gemini Key", type=str)
    parser.add_argument('--model_id', default = "gemini-2.5-pro", help="gemini ai model reference", type=str)
    parser.add_argument('--input_file_path', help="the location of the json file that contains a list of CQs", type=str)
    parser.add_argument('--save_file_path', help="the location of the generated OWL file", type=str)
    return parser

def main():
    para_parser = get_parser()
    args = para_parser.parse_args()
    args_dict = vars(args)
    
    
    query = "Please generate ontology according to the competency questions given below, and please generate the ontology according to the OWL format."
    
    gen_parser = PydanticOutputParser(pydantic_object=Answer)
    os.environ["OPENAI_API_KEY"] = args_dict["user_key"]
    
    llm = ChatOpenAI(
        model=args_dict["model_id"],
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # api_key="...",  # if you prefer to pass api key in directly instaed of using env vars
        # base_url="https://k.bt6.top/v1",
        base_url="https://www.chataiapi.com/v1"
    )
    
    data = load_json(args_dict["input_file_path"])
    AIMesg = run_llm(llm, gen_parser, query, data)
    temp = gen_parser.parse(AIMesg.content)
    raw_owl = temp.OWL
    text_file = open("temp.txt", "w")
    text_file.write(raw_owl)
    text_file.close()
    
    if is_owl_file("temp.txt"):
        print("The generated text is properly formatted accroding to OWL format.")
        convert_files_to_owl("temp.txt", args_dict["save_file_path"])
    else:
        print("Generated text is not properly formatted accroding to OWL format!, Please retry")
    
    os.remove("temp.txt")
    
            
    
    

main()


  