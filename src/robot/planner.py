import replicate

class Planner:
    @staticmethod
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
