from llama_index.llms import OpenAI

resp = OpenAI(model="ft:gpt-3.5-turbo-0613:personal::8fzzIldV").complete("Paul Graham is ")

print(resp)