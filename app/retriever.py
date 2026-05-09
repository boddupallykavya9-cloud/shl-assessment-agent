import json


# LOAD DATA
with open("data/assessments.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)


def search_assessments(query, top_k=5):

    query = query.lower()

    scored_results = []

    for assessment in assessments:

        searchable_text = (
            assessment["name"] + " " +
            assessment["description"]
        ).lower()

        score = 0

        # BASIC WORD MATCHING
        for word in query.split():

            if word in searchable_text:
                score += 2

        # TECHNICAL KEYWORDS
        tech_keywords = [
            "java",
            ".net",
            "developer",
            "software",
            "programming",
            "sql",
            "python",
            "coding",
            "technical"
        ]

        for keyword in tech_keywords:

            if (
                keyword in query
                and keyword in searchable_text
            ):
                score += 5

        # LEADERSHIP / PERSONALITY KEYWORDS
        leadership_keywords = [
            "leadership",
            "stakeholder",
            "management",
            "communication",
            "personality",
            "manager",
            "executive",
            "teamwork",
            "collaboration"
        ]

        for keyword in leadership_keywords:

            if (
                keyword in query
                and keyword in searchable_text
            ):
                score += 5

        # BONUS FOR OPQ ASSESSMENTS
        if "opq" in searchable_text:

            if (
                "leadership" in query
                or "personality" in query
                or "manager" in query
            ):

                score += 8

        # BONUS FOR JAVA ASSESSMENTS
        if "java" in query and "java" in searchable_text:
            score += 10

        # ONLY KEEP RELEVANT RESULTS
        if score > 0:
            scored_results.append((score, assessment))

    # SORT BY HIGHEST SCORE
    scored_results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    # RETURN TOP RESULTS
    results = [
        item[1]
        for item in scored_results[:top_k]
    ]

    return results


# TESTING
if __name__ == "__main__":

    query = (
        "Hiring Java developer with leadership "
        "and stakeholder communication"
    )

    results = search_assessments(query)

    print("\nRESULTS:\n")

    for r in results:

        print(r["name"])
        print(r["url"])
        print(r["description"])
        print("-" * 60)