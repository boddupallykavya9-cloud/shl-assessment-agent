from fastapi import FastAPI

from app.models import (
    ChatRequest,
    ChatResponse
)

from app.retriever import search_assessments

app = FastAPI()


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    # GET LATEST USER MESSAGE
    latest_message = request.messages[-1].content

    message_lower = latest_message.lower()

    # COMBINE ALL USER MESSAGES
    conversation_text = ""

    for message in request.messages:

        if message.role == "user":

            conversation_text += " " + message.content

    # OFF-TOPIC REFUSAL
    blocked_topics = [
        "salary",
        "salaries",
        "legal",
        "politics",
        "weather"
    ]

    for topic in blocked_topics:

        if topic in message_lower:

            return {
                "reply": (
                    "I can only help with SHL assessment "
                    "recommendations and comparisons."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

    # COMPARISON SUPPORT
    comparison_keywords = [
        "difference",
        "compare",
        "comparison"
    ]

    if any(word in message_lower for word in comparison_keywords):

        return {
            "reply": (
                "OPQ assessments focus on personality, leadership style, "
                "and workplace behavior, while technical assessments like "
                "Java assessments evaluate programming and technical skills. "
                "Managerial scenario assessments evaluate workplace "
                "decision-making and leadership capabilities."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # CLARIFICATION LOGIC
    vague_phrases = [
        "need a test",
        "need an assessment"
    ]

    is_vague = False

    # VERY SHORT QUERY
    if len(latest_message.split()) < 3:
        is_vague = True

    # CHECK VAGUE PHRASES
    for phrase in vague_phrases:

        if phrase in message_lower:
            is_vague = True

    # ASK FOR CLARIFICATION
    if is_vague:

        return {
            "reply": (
                "Could you share more details about the role, "
                "skills, or seniority level you are hiring for?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # SEARCH ASSESSMENTS
    results = search_assessments(conversation_text)

    recommendations = []

    for r in results:

        recommendations.append({
            "name": r["name"],
            "url": r["url"],
            "test_type": r["test_type"]
        })

    # FINAL RESPONSE
    reply = (
        f"I found {len(recommendations)} SHL assessments "
        f"relevant to your hiring requirements."
    )

    return {
        "reply": reply,
        "recommendations": recommendations,
        "end_of_conversation": False
    }