import time
from llama_cpp import Llama
import os
import importlib.resources

DEFAULT_CONTEXT = "Tu es un chatbot sur le site internet twitch qui répond aux utilisateurs quand ils effectuent une commande"


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Meta-Llama-3-8B-Instruct-Q5_K_S.gguf')
llm = Llama(
    model_path=filename,
    n_ctx=8192,
    n_threads=8,
    n_gpu_layers=35
    )
    

def infer(context, text, max_new_tokens=20, seed=None):
    start_time = time.time()  # Start time measurement

    chat_response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": DEFAULT_CONTEXT+context},
                {
                    "role": "user",
                    "content": text
                }
            ],
        max_tokens = max_new_tokens,
        temperature=0.3, seed=seed
    )
    result = chat_response['choices'][0]['message']['content'].replace("\n\n", "\n")
    result = result.replace("[INST]", "").replace("[\INST]", "").replace("[SYS]","")
    end_time = time.time()  # End time measurement
    inference_time = end_time - start_time 
    print(f"Inference Time: {inference_time} seconds")
    return result

def differ(text, max_new_tokens=20, temperature=0.3, context=DEFAULT_CONTEXT, seed=None, top_k=40):
    answer = llm.create_chat_completion(messages=[
            {"role": "system", "content": context},
            {
                "role": "user",
                "content": text
            }
        ],max_tokens=max_new_tokens,temperature=temperature,seed=seed, top_k=top_k)
    print(answer)
    return answer['choices'][0]['message']['content']
    
def complete(text, max_new_tokens=20, temperature=0.3):
    answer = llm.create_completion(prompt=text,max_tokens=max_new_tokens,temperature=temperature,echo=True)
    print(answer)
    return answer['choices'][0]['text']