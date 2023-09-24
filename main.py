from Paper_fetcher import fetch_paper, get_text
from model_fetcher_cpp import fetch_model


arxiv_url = 'https://arxiv.org/abs/1706.03762'
paper_location = fetch_paper(arxiv_url)
paper_as_text = get_text(paper_location)
print(paper_as_text)
# print(len(paper_as_text))

fetch_model(paper_as_text)

# the context size is too small. Maybe this can be done only with GPT4 ?

