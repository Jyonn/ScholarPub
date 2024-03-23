file = 'Li CHEN.txt'

with open(file, 'r') as f:
    lines = f.readlines()


def detect_paper(paper: dict):
    if 'Title' not in paper:
        return False
    if 'Authors' not in paper:
        return False

    if 'Conference' not in paper and 'Journal' not in paper:
        return False
    paper['Venue'] = paper['Conference'] if 'Conference' in paper else paper['Journal']
    if 'Publication date' not in paper:
        return False
    paper['Publication date'] = paper['Publication date'][:4]

    if 'ARXIV' in paper['Venue'].upper() or 'CORR' in paper['Venue'].upper():
        return False
    return True


papers = []

current_paper = {}
for line in lines:
    if line == '\n':
        if detect_paper(current_paper):
            papers.append(current_paper)
        current_paper = {}
        continue
    if line.endswith('\n'):
        line = line[:-1]
    if not current_paper:
        current_paper['Title'] = line
    else:
        key, value = line.split(': ', 1)
        current_paper[key] = value

if detect_paper(current_paper):
    papers.append(current_paper)


for paper in papers:
    print('\\item ', end='')
    print(paper['Authors'], end='. ')
    print(paper['Title'], end='. ')
    print(f'\\textit{{{paper["Venue"]}}}, ', end='')
    print(paper['Publication date'], end='.\n')
