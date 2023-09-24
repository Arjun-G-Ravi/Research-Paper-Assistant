import torch
from transformers import (
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    pipeline,
    AutoTokenizer,

)
def fetch_model(input_text):
    bnb_config = BitsAndBytesConfig(
        load_in_4bit= True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=False,
    )

    model = AutoModelForCausalLM.from_pretrained(
    "NousResearch/Llama-2-7b-chat-hf",
    quantization_config=bnb_config,
    device_map= {"": 0}
    )
    model.config.use_cache = False
    model.config.pretraining_tp = 1
    tokenizer = AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf", trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right" # Fix overflow issue with fp16 training

    # qn = input()
    # qn = 'Why are you here?'
    text = f"You are AIRA, a confident, friendly and ethical robotic assistant. You provide safe, direct, honest, and unbiased answers. If a question is unclear or false, you explain why. If you don't know the answer, you admit it.\n"
    prompt = text + 'Human:'+input_text + '\nAIRA:'

    pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=200)
    result = pipe(f"{prompt}")
    ans = result[0]['generated_text']
    print(''.join(ans.split('\\n')[:3]))
