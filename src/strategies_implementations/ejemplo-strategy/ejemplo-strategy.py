import json
import time
import sys
from hl7apy.core import Message

class ExampleStrategy():

    @classmethod
    def execute(cls, text: str):
        
        # EHR build algorithm
        # Message representation
        message = Message("ADT_A01", version="2.5")
        # MSH - Message Header
        current_time = time.localtime()
        message.msh.msh_7 = time.strftime("%Y%m%d%H%M%S", current_time)
        message.msh.msh_9 = "ADT^A01^ADT_A01"

        # EVN - Event Type
        message.evn.evn_2 = message.msh.msh_7
        message.evn.evn_4 = "01"

        # PID - Patient Identification
        message.pid.pid_5.pid_5_2 = "Pepe El Ejemplo"

        # Sample Observation
        message.obx.obx_5 = "Esguince"
        message.obx.obx_11 = "Paracetamol"

        # Sample diagnosis
        message.dg1.dg1_4 = "Dolor"
        message.dg1.dg1_6 = "F"

        # Output representation
        output_as_dict = {
            'output': message.to_er7(trailing_children=True),
        }
        return output_as_dict

if __name__ == '__main__':
    # Get strategy input
    standard_input = input()
    input_dict = json.loads(standard_input)
    strategy_input = input_dict['input']
    # Run execute command
    strategy_output = ExampleStrategy.execute(strategy_input)
    # Serialize the output
    serialized_output = json.dumps(strategy_output)
    # Return serialized output through stdout
    print(serialized_output)
