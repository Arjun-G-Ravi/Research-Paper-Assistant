from llama_cpp import Llama



def fetch_model(prompt):
  model_path = '/home/arjun/Desktop/code llama- summariser/codellama-13b-instruct.ggmlv3.Q4_K_M.bin'
  llama_2 = Llama(model_path=model_path, n_gpu_layers=-1, verbose=False, n_ctx=2048) 
  input = 'You are AIRA, an AI powered robot who is willing to assist anybody. When the human asks a question, you answer helpfully, correctly and respectfully. The answers are always short and direct. It generally does not exeed three sentences. If the question is wrong or confusing, you should politely tell the human that it is not true. \nHuman:' + prompt + 'AIRA: '

  response = llama_2(
          input,
          stream=True,
          temperature=.01,
          # max_tokens=4096,
          # stop=["Human"]
        )
  ans = ''
  for i in response:
      ans += i['choices'][0]['text']
      # display(i['choices'][0]['text'])
      if i['choices'][0]['text'] == '\n' or i['choices'][0]['text'] == '.': #
          print(ans)
          ans = ''

  print(ans)    