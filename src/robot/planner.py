import replicate

def execute_prompt(prompt: str) -> str:
    input = {
        "prompt": prompt,
        "max_tokens": 1024
    }
    result = ""
    for event in replicate.stream(
        "meta/meta-llama-3.1-405b-instruct",
        input=input
    ):
        result += event
    return result

def broadcast_state():
    '''Converts state into a natural language'''

def decodes_broadcast():
    '''Convert natural langue into state update'''
    # Updates internal state

def distance():
    return

if __name__ == "__main__":
    input = {
        "prompt": "Tina has one brother and one sister. How many sisters do Tina's siblings have?",
        "max_tokens": 1024
    }

    for event in replicate.stream(
        "meta/meta-llama-3.1-405b-instruct",
        input=input
    ):
        print(event, end="")
    #=> "Tina has one brother and one sister. From the brother's ...