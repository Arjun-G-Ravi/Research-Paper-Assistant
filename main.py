from Paper_fetcher import fetch_paper, get_text
from model_fetcher import fetch_model


arxiv_url = 'https://arxiv.org/abs/1706.03762'
paper_location = fetch_paper(arxiv_url)
paper_as_text = get_text(paper_location)
print(paper_as_text)
# print(len(paper_as_text))

# fetch_model(paper_as_text)

