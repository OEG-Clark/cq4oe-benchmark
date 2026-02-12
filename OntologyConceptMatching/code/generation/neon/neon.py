from pydantic import BaseModel, Field
from agno.agent import Agent, RunOutput
from agno.models.deepseek import DeepSeek
from agno.workflow import Loop, Step, Workflow
from agno.workflow.types import StepOutput

import os
import json
import subprocess
from typing import List
from pathlib import Path
import tempfile

import xml.etree.ElementTree as ET
from rdflib import Graph
from rdflib import Graph, RDF, OWL, RDFS
from rdflib.term import BNode
import requests
import argparse
from bs4 import BeautifulSoup

OOPS_API = "https://oops.linkeddata.es/rest"
REQUEST_TEMPLATE = "/home/jovyan/LLMOnto/Benchmark/OntologyConceptMatching/neon_code/templates/oops_request_template.xml"

class Answer(BaseModel):
    reason: str = Field(description="The reasoning process of the entire generation")
    OWL: str = Field(description="The OWL source code representing the ontology")
    
def is_owl(onto_str: str = "") -> bool:
    """
    check the root node is RDF/XML
    """
    try:
        root = ET.fromstring(onto_str)
        # root = tree.getroot()
        # Check if the root element is RDF and has the correct namespace
        return root.tag.endswith('RDF')
    except ET.ParseError:
        return False
    
    
def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

    
def reason_ontology(onto_str: str) -> tuple[str, str]:
    """
    Reason the ontology using the Hermit reasoner.
    :param ontology_file: The path to the ontology file.
    :type ontology_file: str | Path
    :return: The reasoned ontology.
    :rtype: tuple[str, str]
    """
    # convert the ontology to OWL/XML
    ontology = Graph().parse(data=onto_str, format="xml")
    ontology.serialize(format="xml", destination="temp.xml")

    # open the ontology in the Hermit reasoner
    hermit = subprocess.run(["java", "-jar", "/home/jovyan/LLMOnto/Benchmark/OntologyConceptMatching/neon_code/hermit/HermiT.jar", '-k',
                            'temp.xml'],
                            capture_output=True,
                            text=True)

    return hermit.stdout, hermit.stderr


class OOPSValidation:
    """
    OOPS! validation of the produced ontology.
    """
    def __init__(self, onto_str:str | Path | Graph):
            
        self.ontology = Graph().parse(data=onto_str, format="xml")
        self.oops_api = OOPS_API
        with open(REQUEST_TEMPLATE, "r") as f:
            self.request_template = f.read()

        self.request_body = self._compose_request()

    def _compose_request(self,
                         output_format: str = 'XML',
                         pitfalls: str = '') -> str:
        """
        Compose the request to the OOPS! API.
        :param output_format: The output format of the OOPS! API.
        :type output_format: str
        :param pitfalls: The pitfalls to check for expressed as a string of
                            comma-separated values.
        :type pitfalls: str
        :return: The request to the OOPS! API.
        :rtype: str
        """
        # format the ontology parameter
        formatted_ontology = f'<![CDATA[ {self.ontology} ]]></OntologyContent>'
        formatted_request = self.request_template.replace('</OntologyContent>',
                                                          formatted_ontology)

        # format the output format parameter
        if output_format not in ['XML', 'RDF/XML']:
            raise ValueError(f'Invalid output format: {output_format}')
        formatted_output = f'{output_format}</OutputFormat>'
        formatted_request = formatted_request.replace('</OutputFormat>',
                                                      formatted_output)

        # format the pitfalls parameter
        if pitfalls:
            formatted_pitfalls = f'{pitfalls}</Pitfalls>'
            formatted_request = formatted_request.replace('</Pitfalls>',
                                                          formatted_pitfalls)

        return formatted_request

    def validate(self) -> str:
        """
        Validate the ontology using the OOPS! API.
        :return: The OOPS! validation results.
        :rtype: dict
        """
        # print(self.request_body)
        try:
            response = requests.post(url=self.oops_api,
                                     data=self.request_body,
                                     allow_redirects=False).text
            # print(response)
            # format the text as xml
            response = BeautifulSoup(response, features="xml").prettify()
            return response
        except Exception as e:
            raise Exception(f"Error connecting to the OOPS! API: {e}") from e
            
            
class NEONWorkflow(Workflow):
    """NEON-GPT Workflow following the methodology from the paper"""
    
    def __init__(self, competency_questions: str):
        super().__init__(name="NEON-GPT Workflow")
        self.cqs = competency_questions
        self.ontology_gen_agent = Agent(
            model=DeepSeek(id="deepseek-reasoner"),
            name="Ontology Agent",
            role="Ontology specialist",
            instructions="You are an experienced knowledge engineer, and you are modelling a specific domain. Based on the provided competency questions, produce the ontology source code following the OWL format. \nMake it as complete as possible, and focus on the concepts, properties, domains and ranges that you think is applicable from the competency questions.\n Please generate the ontology in XML format.",
            output_schema=Answer
        )
        
        self.ontology_syntax_agent = Agent(
            model=DeepSeek(id="deepseek-reasoner"),
            instructions="You are an experienced knowledge engineer. Now please fix syntax errors in the provided OWL/XML code",
            output_schema=Answer
        )

        self.ontology_hermit_agent = Agent(
            model=DeepSeek(id="deepseek-reasoner"),
            name="HERMIT Agent",
            role="Ontology Debugging specialist",
            instructions="You are an experienced ontology engineer. Now you have a debugging-suggestion report for a specific ontology from HERMIT. The purpose of HERMIT is to determine whether or not the ontology is consistent and identify subsumption relationships between classes. Please carefully analyse the HERMIT report and the source code for the ontology, debug the source code ontology and generate the updated version of the ontology.",
            output_schema=Answer
        )

        self.ontology_oops_agent = Agent(
            model=DeepSeek(id="deepseek-reasoner"),
            name="OOPS Agent",
            role="Ontology Debugging specialist",
            instructions="You are an experienced ontology engineer. Now you have a debugging suggestion report for a specific ontology from the OOPS. The purpose of OOPS is to support ontology developers during ontology validation, which can be divided into diagnosis and repair. Please carefully analyse the OOPS report and the source code for the ontology, debug the source code ontology and generate the updated version of the ontology.",
            output_schema=Answer
        )
        
    def run(self, neon_method):
        """Execute the full NEON workflow"""
        
        # Step 1: Generate initial ontology draft (Specification & Conceptualization)
        if neon_method:
            print("Executing NEON workflow:")
            print("Step 1: Generating initial ontology draft...")
            gen_response = self.ontology_gen_agent.run(self.cqs)
            # initial_ontology = gen_response.content.OWL
            ontology = gen_response.content.OWL
            print(is_owl(ontology))
            
            while True:
                if is_owl(ontology):
                    print("Syntax validation passed")
                    break
                else:
                    ontology = self._syntax_validation_loop(ontology)
                
            # Step 3: Consistency checking with Hermit
            print("Step 2: Consistency checking with Hermit...")
            ontology = self._consistency_check_loop(ontology)
            while True:
                if is_owl(ontology):
                    print("Syntax validation passed")
                    break
                else:
                    ontology = self._syntax_validation_loop(ontology)
            print("Consistency checking passed")

            # Step 4: Pitfall resolution with OOPS
            print("Step 3: Pitfall resolution with OOPS...")
            ontology = self._pitfall_resolution_loop(ontology)
            while True:
                if is_owl(ontology):
                    print("Syntax validation passed")
                    break
                else:
                    ontology = self._syntax_validation_loop(ontology)
            print("Pitfall resolution completed")
        else:
            print("Executing normal workflow:")
            gen_response = self.ontology_gen_agent.run(self.cqs)
            ontology = gen_response.content.OWL
            while True:
                if is_owl(ontology):
                    print("Syntax validation passed")
                    break
                else:
                    ontology = self._syntax_validation_loop(ontology)
            print("Syntax validation passed")
        return ontology
    
    def _syntax_validation_loop(self, ontology: str) -> str:
        try:
            root = ET.fromstring(ontology)
            return ontology  # Syntax is valid
        except ET.ParseError as e:
            print(f"  Syntax error detected: {str(e)}...")

            # Create prompt for fixing syntax errors
            syntax_prompt = f"""
            I have an OWL ontology with syntax errors. Please fix the syntax issues.

            Ontology:
            {ontology}

            Error message:
            {str(e)}

            Please return ONLY the corrected RDF/XML code.
            """

            # Use a simple agent for syntax fixing
            response = self.ontology_syntax_agent.run(syntax_prompt)
            ontology = response.content.OWL
        
        return ontology
    
    def _consistency_check_loop(self, ontology: str) -> str:
        """Step 3: Check and fix consistency with Hermit"""
        stdout, stderr = reason_ontology(ontology)
            
        if stderr:
            print(f"  Consistency error detected: {stderr}...")

            # Use Hermit agent to debug
            hermit_prompt = f"""
            I have an OWL ontology with consistency errors according to the Hermit reasoner.

            Ontology:
            {ontology}

            Hermit error report:
            {stderr}

            Please analyze and fix the consistency issues.
            """

            response = self.ontology_hermit_agent.run(hermit_prompt)
            ontology = response.content.OWL
        else:
            pass
        return ontology
    
    def _pitfall_resolution_loop(self, ontology: str) -> str:
        oops = OOPSValidation(ontology)
        oops_response = oops.validate()
        oops_prompt = f"""
        I have an OWL ontology with the following OOPS pitfall report.
        Ontology:
        {ontology}
        OOPS pitfall report:
        {oops_response}
        Please analyze and fix the identified pitfalls.
        """
        response = self.ontology_oops_agent.run(oops_prompt)
        ontology = response.content.OWL
        return ontology
            


            
            
def final_onto(cqs_path, neon_method):
    """Execute the complete NEON-GPT workflow"""
    print("=== NEON-GPT Workflow ===")
    print("Loading competency questions...")
    with open(cqs_path, "rb") as f:
        cqs = json.load(f)
    
    start_prompt = "All competency questions are provided here:\n"
    
    for cq in cqs:
        start_prompt += cq
        start_prompt += "\n"
    
    workflow = NEONWorkflow(start_prompt)
    final_ontology = workflow.run(neon_method)
    if neon_method:
    
        if final_ontology:
            print("\n" + "="*50)
            print("WORKFLOW COMPLETED SUCCESSFULLY!")
            print("="*50)

            # Save the final ontology
            with open("final_ontology.owl", "w") as f:
                f.write(final_ontology)
            print(f"✓ Ontology saved")

            # Validate it
            print(f"✓ Is valid OWL: {is_owl(final_ontology)}")

            # Run final Hermit check
            stdout, stderr = reason_ontology(final_ontology)
            if not stderr:
                print("✓ Passes Hermit reasoner check")

            return final_ontology
        else:
            print("\nWorkflow failed to produce valid ontology")
            return None
    else:
        return final_ontology


def get_parser():
    parser = argparse.ArgumentParser(description="Evaluation of the generated ontology")
    parser.add_argument('--api_key', default = "XXX", help="deepseek offical api key", type=str)
    parser.add_argument('--neon_method',  default = "false", help="Flag of whether neon method is implmented", type=str)
    parser.add_argument('--cqs_file', help="the location of generated ontology file ", type=str)
    parser.add_argument('--save_file', help="the location of ground truth ontology file", type=str)
    return parser


def main():
    para_parser = get_parser()
    args = para_parser.parse_args()
    args_dict = vars(args)
    os.environ['DEEPSEEK_API_KEY'] = args_dict["api_key"]
    cqs_path = args_dict["cqs_file"]
    save_path = args_dict["save_file"]
    neon_method = str2bool(args_dict["neon_method"])
    ontology = None
    idx = 1
    while ontology is None:
        print(f"running index: {idx}")
        ontology = final_onto(cqs_path, neon_method)
        idx += 1
    with open(save_path, "w") as f:
        f.write(ontology)
        
        
main()
