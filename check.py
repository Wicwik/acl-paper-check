from acl_anthology import Anthology
from collections import defaultdict
import pandas as pd
from llm import get_model, predict


model, tokenizer = get_model()

answer = predict("From which country is following institue: Kempelen Institute of Intelligent Technologies", model, tokenizer)
print(answer)

anthology = Anthology.from_repo()
anthology.load_all()

volume = anthology.get("2025.acl-long")

print(volume)

countries = defaultdict(int)

def ask_llm(institution):
    ""

def get_country():
    return ""

papers_with_aff = {"title": [], "affiliations": []}
all_affiliations = set()

for paper in volume.papers():
    affiliations = set()
    if len(paper.authors) > 0:
        # print(paper.title)

        for author in paper.authors:
            if author.affiliation:
                if "and" in author.affiliation:
                    affiliations = affiliations | set(author.affiliation.split(" and "))
                else:
                    affiliations.add(author.affiliation)

            affiliations = set(list(map(lambda x: x.strip(",").strip(), list(affiliations))))

    if affiliations:
        papers_with_aff["title"].append(paper.title)
        papers_with_aff["affiliations"].append(affiliations)

        all_affiliations = all_affiliations | affiliations

df = pd.DataFrame(papers_with_aff)
df.to_csv("affiliations_per_paper.csv")

df = pd.DataFrame({"affiliation": sorted(list(all_affiliations))})
df.to_csv("affiliations.csv")