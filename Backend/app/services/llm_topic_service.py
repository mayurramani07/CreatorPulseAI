import json
import os

from groq import Groq


MODEL_NAME = "openai/gpt-oss-20b"

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def group_request_comments(
    comments: list[dict],
) -> dict[str, list[dict]]:
    """
    Use GPT-OSS 20B to semantically assign
    each content-request comment to a topic.

    LLM:
        Understands comment meaning
        and determines the topic.

    Python:
        Only converts assignments into groups.

    No keyword matching.
    No stop-word rules.
    No topic-specific if/else logic.
    """

    if not comments:
        return {}

    valid_comments = [
        comment
        for comment in comments
        if comment.get("text", "").strip()
    ]

    if not valid_comments:
        return {}

    # ---------------------------------------------------------
    # 1. Prepare comments
    # ---------------------------------------------------------

    comment_data = []

    for comment in valid_comments:

        comment_data.append(
            {
                "comment_id": str(
                    comment.get(
                        "comment_id",
                        "",
                    )
                ),
                "text": comment.get(
                    "text",
                    "",
                ).strip(),
            }
        )

    comments_json = json.dumps(
        comment_data,
        ensure_ascii=False,
    )

    # ---------------------------------------------------------
    # 2. Prompt
    # ---------------------------------------------------------

    prompt = f"""
You are the semantic topic classification engine
for CreatorPulse AI.

You will receive YouTube comments that have already
been detected as potential content requests.

Your job is to understand the MEANING of each comment
and assign it to the most appropriate topic.

Do NOT classify based on individual keywords alone.

Understand the complete meaning of the comment.

Do NOT use predefined topic categories.

Create the topic dynamically from the meaning of
the comments.

Similar requests must receive the same topic.

Different subjects must receive different topics.

Every comment must receive exactly ONE topic.

Topic names should be short and meaningful,
normally between 1 and 4 words.

Do NOT use generic topics such as:

Other
General
Misc
Unknown
Random

Do NOT use request words as topics:

course
video
tutorial
playlist
series
learn
learning
teach
teaching
please
make
want
need
full
complete

Instead identify WHAT the creator is being asked
to create content about.

Examples:

Comment:
"please make full playlist for ai/ml"

Topic:
"AI/ML"

Comment:
"please make a complete playlist on rag implementation"

Topic:
"RAG"

Comment:
"continue the c++ dsa series"

Topic:
"DSA"

Comment:
"aws full complete course"

Topic:
"AWS"

Comment:
"bring a web development series"

Topic:
"Web Development"

Comment:
"waiting for sigma 12 prime"

Topic:
"Sigma 12 / Sigma Prime"

Comment:
"vote for mcp and n8n"

Topic:
"MCP / n8n"

Comment:
"please make backend deployment course"

Topic:
"Backend / Deployment"

IMPORTANT:

Preserve every comment_id exactly.

comment_id MUST be returned as a STRING.

Do not modify comment IDs.

Return ONLY valid JSON.

Required JSON structure:

{{
    "assignments": [
        {{
            "comment_id": "123",
            "topic": "AI/ML"
        }}
    ]
}}

COMMENTS:

{comments_json}
"""

    # ---------------------------------------------------------
    # 3. GPT-OSS call
    # ---------------------------------------------------------

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],

        # JSON Object Mode
        response_format={
            "type": "json_object"
        },

        # IMPORTANT FOR GPT-OSS + JSON
        reasoning_format="hidden",

        # Keep reasoning low for classification.
        reasoning_effort="low",

        temperature=0,

        max_completion_tokens=4096,
    )

    # ---------------------------------------------------------
    # 4. Extract response
    # ---------------------------------------------------------

    content = (
        response
        .choices[0]
        .message
        .content
    )

    if not content:
        return {}

    # ---------------------------------------------------------
    # 5. Parse JSON
    # ---------------------------------------------------------

    try:

        result = json.loads(
            content
        )

    except json.JSONDecodeError:

        print(
            "LLM returned invalid JSON:"
        )

        print(content)

        return {}

    # ---------------------------------------------------------
    # 6. Build comment lookup
    # ---------------------------------------------------------

    comments_by_id = {
        str(
            comment.get(
                "comment_id",
                "",
            )
        ): comment
        for comment in valid_comments
    }

    # ---------------------------------------------------------
    # 7. Convert assignments → topic groups
    # ---------------------------------------------------------

    grouped_comments: dict[
        str,
        list[dict],
    ] = {}

    assignments = result.get(
        "assignments",
        [],
    )

    if not isinstance(
        assignments,
        list,
    ):
        return {}

    for assignment in assignments:

        if not isinstance(
            assignment,
            dict,
        ):
            continue

        comment_id = str(
            assignment.get(
                "comment_id",
                "",
            )
        )

        topic = assignment.get(
            "topic",
            "",
        )

        if not isinstance(
            topic,
            str,
        ):
            continue

        topic = topic.strip()

        if not topic:
            continue

        comment = comments_by_id.get(
            comment_id
        )

        if comment is None:
            continue

        grouped_comments.setdefault(
            topic,
            [],
        ).append(
            comment
        )

    return grouped_comments