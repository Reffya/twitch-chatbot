import time
from llama_cpp import Llama

LLM_MODEL_PATH = "datas/Meta-Llama-3-8B-Instruct-Q5_K_S.gguf"

DEFAULT_CONTEXT = "Tu es un chatbot sur le site internet twitch qui répond aux utilisateurs quand ils effectuent une commande"

class LLM_Model:
    def __init__(self):
        self.llm = Llama(
            model_path=LLM_MODEL_PATH,
            n_ctx=8192,
            n_threads=8,
            n_gpu_layers=35
        )

    def infer(self, context, text, max_new_tokens=20):
        start_time = time.time()  # Start time measurement

        chat_response = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": DEFAULT_CONTEXT+context},
                {
                    "role": "user",
                    "content": text
                }
            ],
            max_tokens = max_new_tokens,
            temperature=0.3
        )
        result = chat_response['choices'][0]['message']['content'].replace("\n\n", "\n")
        result = result.replace("[INST]", "").replace("[\INST]", "").replace("[SYS]","")
        end_time = time.time()  # End time measurement
        inference_time = end_time - start_time 
        print(f"Inference Time: {inference_time} seconds")
        return result
