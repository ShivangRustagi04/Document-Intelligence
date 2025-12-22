def evaluate(outputs):
    scores = []
    for o in outputs:
        for v in o["bureau_parameters"].values():
            scores.append(v.get("confidence", 0))
    return sum(scores)/len(scores)
