import time
import sys
import pickle
from hl7apy.core import Message
from transformers import pipeline


class DefaultADT_A01():
    """
    Concrete implementation of the Natural Language Processing (NLP) step in a 3 step pipeline.
    This implementation includes the NLP techniques necessary to build an Electronic Heath Record (EHR).
    The techniques used in this implementation are named-entity recognition (NER) and dependency parsing.
    This is a default sample implementation that can serve as an example for more specific ones.


    This implementation will output a probably incomplete Admit/Visit Notification ADT_A01 HL7 message.
    For further information:
    https://hl7-definition.caristix.com/v2/HL7v2.5/TriggerEvents/ADT_A01


    The library for HL7 message creation is HL7apy.
    Further information and documentation:
     https://crs4.github.io/hl7apy/index.html
    """

    @classmethod
    def execute(cls, text: str):
        """
        Concrete implementation of the Natural Language Processing (NLP) step in a 3 step pipeline.
        :param str text: The text to perform NLP on
        :return: The EHR and the results of the named-entity recognition for depuration and checking purposes.
        :rtype: str
        """
        # NER
        clinical_ner_result = cls.clinical_ner(text)
        generic_ner_result = cls.generic_ner(text)
        # Tag extraction into strings
        body_parts = cls.ner_tag_extractor(clinical_ner_result, text, "ANAT")
        chem_entities = cls.ner_tag_extractor(
            clinical_ner_result, text, "CHEM")
        pathologic_conditions = cls.ner_tag_extractor(
            clinical_ner_result, text, "DISO")
        procedures = cls.ner_tag_extractor(clinical_ner_result, text, "PROC")
        names = cls.ner_tag_extractor(generic_ner_result, text, "PER")

        # Dependency parsing - not used in this early version - wont load to save time
        # nlp = spacy.load("es_dep_news_trf")
        # doc = nlp(text)

        # EHR build algorithm
        # Message representation
        message = Message("ADT_A01", version="2.5")
        # MSH - Message Header
        current_time = time.localtime()
        message.msh.msh_7 = time.strftime("%Y%m%d%H%M%S", current_time)
        message.msh.msh_9 = "ADT^A01^ADT_A01"
        message_representation = message.to_er7(trailing_children=True)

        # EVN - Event Type
        message.evn.evn_2 = message.msh.msh_7
        message.evn.evn_4 = "01"
        message_representation += f"\n{message.to_er7(trailing_children=True)}"

        # PID - Patient Identification
        # Flintstonesque name extraction
        surnames = None
        # Assuming the is only the patients name and no nk1 sequence
        if len(names) > 0:
            full_name = names[0].split()
        else:
            full_name = "None"
        if len(full_name) > 0:
            surnames = " ".join(full_name[1:])
        if surnames is not None:
            message.pid.pid_5.pid_5_1 = surnames.capitalize()
        message.pid.pid_5.pid_5_2 = full_name[0].capitalize()
        message_representation += f"\n{message.to_er7(trailing_children=True)}"

        # Sample Observation
        message.obx.obx_5 = "---".join(pathologic_conditions)
        message.obx.obx_11 = "---".join(chem_entities)
        message_representation += f"\n{message.to_er7(trailing_children=True)}"

        # Sample diagnosis
        message.dg1.dg1_4 = "---".join(pathologic_conditions)
        message.dg1.dg1_6 = "F"
        message_representation += f"\n{message.to_er7(trailing_children=True)}"

        # Output representation
        ner_as_str = f"\nClinical NER:\n{str(clinical_ner_result)}"
        ner_as_str += f"\n\nBody parts and anatomy:\n{body_parts}"
        ner_as_str += f"\nChemical entities and pharmacological substances:\n{chem_entities}"
        ner_as_str += f"\nPathologic conditions:\n{pathologic_conditions}"
        ner_as_str += f"\nDiagnostic and therapeutic procedures:\n{procedures}"
        ner_as_str += f"\n\n\nGeneric NER:\n{str(generic_ner_result)}"
        ner_as_str += f"\n\nIdentified names:\n{names}"
        output_as_str = f"\nElectronic health record:\n{message.to_er7(trailing_children=True)}\n\nNamed-entity recognition:\n{ner_as_str}\n\n"
        output_as_dict = {
            'output': message.to_er7(trailing_children=True),
            'ner': [
                {
                    'name': 'clinical',
                    'result': clinical_ner_result,
                    'tags': 
                        [
                            {
                                'name': 'ANAT',
                                'description': "body parts and anatomy (e.g. garganta, 'throat')",
                                'detected_entities': body_parts
                            },
                            {
                                'name': 'CHEM',
                                'description': "chemical entities and pharmacological substances (e.g. aspirina,'aspirin')",
                                'detected_entities': chem_entities
                            },
                            {
                                'name': 'DISO',
                                'description': "pathologic conditions (e.g. dolor, 'pain')",
                                'detected_entities': pathologic_conditions
                            },
                            {
                                'name': 'PROC',
                                'description': "diagnostic and therapeutic procedures, laboratory analyses and medical research activities (e.g. cirugía, 'surgery')",
                                'detected_entities': procedures
                            },
                        ],
                },
                {
                    'name': 'generic',
                    'result': generic_ner_result,
                    'tags': 
                        [
                            {
                                'name': 'LOC',
                                'description': "Location",
                                'detected_entities': None
                            },
                            {
                                'name': 'MISC',
                                'description': "Miscellaneous",
                                'detected_entities': None
                            },
                            {
                                'name': 'ORG',
                                'description': "Organization",
                                'detected_entities': None
                            },
                            {
                                'name': 'PER',
                                'description': "Person",
                                'detected_entities': names
                            },
                        ],
                }
            ]
        }
        return output_as_dict

    @classmethod
    def clinical_ner(cls, text: str) -> list:
        """
        Clinical named-entity recognition model.
        Source: https://huggingface.co/lcampillos/roberta-es-clinical-trials-ner
        TAGS:
            ANAT: body parts and anatomy (e.g. garganta, 'throat')
            CHEM: chemical entities and pharmacological substances (e.g. aspirina,'aspirin')
            DISO: pathologic conditions (e.g. dolor, 'pain')
            PROC: diagnostic and therapeutic procedures, laboratory analyses and medical research activities (e.g. cirugía, 'surgery')
        :param str text: The text to perform named-entity recognition on
        :return: The result of the clinical named-entity recognition
        :rtype: list of dicts of the type: [{'entity': 'B-DISO', 'score': 0.998966, 'index': 8, 'word': 'Ġdolor', 'start': 40, 'end': 45}]
        """
        ner = pipeline(model="lcampillos/roberta-es-clinical-trials-ner")
        return ner(text)

    @classmethod
    def generic_ner(cls, text: str) -> list:
        """
        Generic named-entity recognition model.
        Source: https://huggingface.co/mrm8488/bert-spanish-cased-finetuned-ner
        TAGS:
            LOC:  Location
            MISC: Miscellaneous
            ORG:  Organization
            PER:  Person
        :param str text: The text to perform named-entity recognition on
        :return: The result of the generic named-entity recognition
        :rtype: list of dicts such as [{'entity': 'B-PER', 'score': 0.9991167, 'index': 3, 'word': 'Juan', 'start': 13, 'end': 17}]
        """
        ner = pipeline(model="mrm8488/bert-spanish-cased-finetuned-ner")
        return ner(text)

    @classmethod
    def ner_tag_extractor(cls, ner, text: str, tag: str):
        identified_tags = []
        for dictionary in ner:
            if dictionary["entity"] == f"B-{tag}":
                identified_tags.append(
                    text[dictionary["start"]:dictionary["end"]])
            if dictionary["entity"] == f"I-{tag}":
                identified_tags[-1] += " " + \
                    (text[dictionary["start"]:dictionary["end"]])
        return identified_tags


if __name__ == '__main__':
    # Get strategy input
    strategy_input = sys.argv[1]
    # Run execute command
    strategy_output = DefaultADT_A01.execute(strategy_input)
    # Serialize the output
    serialized_output = pickle.dumps(strategy_output)
    # Return serialized output through stdout
    sys.stdout.buffer.write(serialized_output)
