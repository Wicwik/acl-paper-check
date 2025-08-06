from acl_anthology import Anthology

anthology = Anthology.from_repo()

volume = anthology.get("2025.acl-long")

print(volume)

for paper in volume.papers():
    if len(paper.authors) > 0:
        print(paper.title)
        print(paper.authors)