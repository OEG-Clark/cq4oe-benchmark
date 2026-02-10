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
REQUEST_TEMPLATE = "/home/jovyan/LLMOnto/Benchmark/neon/templates/oops_request_template.xml"

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
    hermit = subprocess.run(["java", "-jar", "/home/jovyan/LLMOnto/Benchmark/neon/hermit/HermiT.jar", '-k',
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
        
    def run(self):
        """Execute the full NEON workflow"""
        
        # Step 1: Generate initial ontology draft (Specification & Conceptualization)
        print("Step 1: Generating initial ontology draft...")
        gen_response = self.ontology_gen_agent.run(self.cqs)
        ontology = gen_response.content.OWL
        
        # Validate it's proper OWL
        if not is_owl(ontology):
            print("ERROR: Initial ontology is not valid OWL")
            return None
            
        print("✓ Initial ontology generated")
        
        # Step 2: Syntax validation loop
        print("\nStep 2: Syntax validation...")
        ontology = self._syntax_validation_loop(ontology)
        if not ontology:
            return None
        print("✓ Syntax validation passed")
        
        # Step 3: Consistency checking with Hermit
        print("\nStep 3: Consistency checking with Hermit...")
        ontology = self._consistency_check_loop(ontology)
        if not ontology:
            return None
        print("✓ Consistency checking passed")
        
        # Step 4: Pitfall resolution with OOPS
        print("\nStep 4: Pitfall resolution with OOPS...")
        ontology = self._pitfall_resolution_loop(ontology)
        if not ontology:
            return None
        print("✓ Pitfall resolution completed")
        
        return ontology
    
    def _syntax_validation_loop(self, ontology: str, max_attempts: int = 3) -> str:
        """Step 2: Validate and fix syntax errors"""
        for attempt in range(max_attempts):
            # Parse to check syntax
            try:
                Graph().parse(data=ontology, format="xml")
                return ontology  # Syntax is valid
            except Exception as e:
                print(f"  Syntax error detected (attempt {attempt + 1}/{max_attempts}): {str(e)[:100]}...")
                
                # Create prompt for fixing syntax errors
                syntax_prompt = f"""
                I have an OWL ontology with syntax errors. Please fix the syntax issues.
                
                Ontology:
                {ontology}
                
                Error message:
                {str(e)}
                
                Please return ONLY the corrected OWL/XML code.
                """
                
                # Use a simple agent for syntax fixing
                response = Agent(
                    model=DeepSeek(id="deepseek-reasoner"),
                    instructions="Fix syntax errors in OWL/XML code",
                    output_schema=Answer
                ).run(syntax_prompt)
                
                if response and response.content.OWL:
                    ontology = response.content.OWL
                else:
                    print(f"  Failed to fix syntax after {max_attempts} attempts")
                    return None
        
        print(f"  Max syntax validation attempts ({max_attempts}) reached")
        return None
    
    def _consistency_check_loop(self, ontology: str, max_attempts: int = 3) -> str:
        """Step 3: Check and fix consistency with Hermit"""
        for attempt in range(max_attempts):
            stdout, stderr = reason_ontology(ontology)
            
            if stderr and "Error" in stderr:
                print(f"  Consistency error detected (attempt {attempt + 1}/{max_attempts}): {stderr[:100]}...")
                
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
                
                if response and response.content.OWL and is_owl(response.content.OWL):
                    ontology = response.content.OWL
                else:
                    print("  Failed to get valid response from Hermit agent")
                    break
            else:
                # No consistency errors
                return ontology
        
        print(f"  Could not resolve all consistency issues after {max_attempts} attempts")
        return None
    
    def _pitfall_resolution_loop(self, ontology: str, max_attempts: int = 3) -> str:
        """Step 4: Check and fix pitfalls with OOPS"""
        for attempt in range(max_attempts):
            oops = OOPSValidation(ontology)
            try:
                oops_response = oops.validate()
                
                # Check if it's an error response or actual pitfalls
                if "unexpected_error" in oops_response:
                    print(f"  OOPS API error: {oops_response[:100]}...")
                    # Might be a temporary API issue, try one more time
                    if attempt < max_attempts - 1:
                        continue
                    else:
                        return ontology  # Return ontology as-is if OOPS fails
                
                # Check if there are actual pitfalls
                soup = BeautifulSoup(oops_response, "xml")
                pitfalls = soup.find_all("oops:hasAffectedElement")
                
                if not pitfalls:
                    print("  ✓ No pitfalls detected by OOPS")
                    return ontology
                
                print(f"  Detected {len(pitfalls)} pitfalls (attempt {attempt + 1}/{max_attempts})")
                
                # Use OOPS agent to debug
                oops_prompt = f"""
                I have an OWL ontology with the following OOPS pitfall report.
                
                Ontology:
                {ontology}
                
                OOPS pitfall report:
                {oops_response}
                
                Please analyze and fix the identified pitfalls.
                """
                
                response = self.ontology_oops_agent.run(oops_prompt)
                
                if response and response.content.OWL and is_owl(response.content.OWL):
                    ontology = response.content.OWL
                else:
                    print("  Failed to get valid response from OOPS agent")
                    break
                    
            except Exception as e:
                print(f"  Error in OOPS validation: {str(e)}")
                if attempt == max_attempts - 1:
                    return ontology  # Return as-is
        
        return ontology


            
            
def final_onto(cqs_path):
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
    final_ontology = workflow.run()
    
    if final_ontology:
        print("\n" + "="*50)
        print("WORKFLOW COMPLETED SUCCESSFULLY!")
        print("="*50)
        
        # Save the final ontology
        with open("final_ontology.owl", "w") as f:
            f.write(final_ontology)
        print(f"✓ Ontology saved to final_ontology.owl")
        
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


def get_parser():
    parser = argparse.ArgumentParser(description="Evaluation of the generated ontology")
    parser.add_argument('--api_key', default = "XXX", help="deepseek offical api key", type=str)
    parser.add_argument('--cqs_file', help="the location of the json file contains a list of competency questions ", type=str)
    parser.add_argument('--save_file', help="the location to save the generated ontology", type=str)
    return parser


def main():
    para_parser = get_parser()
    args = para_parser.parse_args()
    args_dict = vars(args)
    os.environ['DEEPSEEK_API_KEY'] = args_dict["api_key"]
    cqs_path = args_dict["cqs_file"]
    save_path = args_dict["save_file"]
    ontology = None
    idx = 1
    while ontology is None:
        print(f"running index: {idx}")
        ontology = final_onto(cqs_path)
        idx += 1
    with open(save_path, "w") as f:
        f.write(ontology)
        
        
main()
