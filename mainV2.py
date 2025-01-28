import ast

from openai import OpenAI

# Initialize LM Studio client
client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
MODEL = "qwen2.5-3b-instruct"

def the_sum(a: int, b: int) -> int:
    """Returns the sum of two numbers"""
    return a + b

THE_SUM = {
    'type': 'function',
    'function': {
        'name': 'the_sum',
        'description': 'Returns the sum of two numbers',
        'parameters': {
            'type': 'object',
            'properties': {
                'a': {
                    'type': 'int',
                    'description': 'The first number'
                },
                'b': {
                    'type': 'int',
                    'description': 'The second number'
                }
            },
            'required': ['a', 'b']
        },
    }
}

def the_format_uppercase(text: str) -> str:
    """Returns the input text in uppercase"""
    return text.upper()

THE_FORMAT_UPPERCASE = {
    'type': 'function',
    'function': {
        'name': 'the_format_uppercase',
        'description': 'Returns the input text in uppercase',
        'parameters': {
            'type': 'object',
            'properties': {
                'text': {
                    'type': 'string',
                    'description': 'The input text'
                }
            },
            'required': ['text']
        },
    }
}

def the_list_of_numbers(n: int, size: int) -> list:
    """Returns a list of numbers from 0 to n"""
    return [n for n in range(size)]

THE_LIST_OF_NUMBERS = {
    'type': 'function',
    'function': {
        'name': 'the_list_of_numbers',
        'description': 'Returns a list of numbers from 0 to n',
        'parameters': {
            'type': 'object',
            'properties': {
                'n': {
                    'type': 'int',
                    'description': 'The number n'
                },
                'size': {
                    'type': 'int',
                    'description': 'The size of the list'
                }
            },
            'required': ['n', 'size']
        },
    }
}

def the_send_email(to: str, subject: str, body: str) -> str:
    """Sends an email"""
    return f"Email sent to {to} with subject '{subject}' and body '{body}'"

THE_SEND_EMAIL = {
    'type': 'function',
    'function': {
        'name': 'the_send_email',
        'description': 'Sends an email',
        'parameters': {
            'type': 'object',
            'properties': {
                'to': {
                    'type': 'string',
                    'description': 'The recipient email address'
                },
                'subject': {
                    'type': 'string',
                    'description': 'The subject of the email'
                },
                'body': {
                    'type': 'string',
                    'description': 'The body of the email'
                }
            },
        },
    }
}

def run():

    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistent amd help people to choose the right function."
            )
        }
    ]

    the_input = input("Enter your question:")

    messages.append({'role': 'user', 'content': the_input})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=[THE_SUM, THE_FORMAT_UPPERCASE, THE_LIST_OF_NUMBERS, THE_SEND_EMAIL]
    )

    if response.choices[0].message.tool_calls:
        result = None
        for tool_call in response.choices[0].message.tool_calls:

            arguments = tool_call.function.arguments
            if arguments:
                arguments = ast.literal_eval(arguments)

            print(f"Function: {tool_call.function.name}")
            print(f"Arguments: {arguments}")

            if tool_call.function.name == 'the_sum':
                result = the_sum(arguments['a'],arguments['b'])
            elif tool_call.function.name == 'the_format_uppercase':
                result = the_format_uppercase(arguments['text'])
            elif tool_call.function.name == 'the_list_of_numbers':
                result = the_list_of_numbers(arguments['n'], arguments['size'])

        if result:
            print(f"Result: {result}")
    else:
        print(response.choices[0].message.content)

if __name__ == "__main__":
    run()