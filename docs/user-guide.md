# User Guide

Status: **Planned**. The Chainlit UI is not implemented; this describes the intended experience.

## Typical journey

1. **Start a session.** Open the app and begin a conversation; the UI creates a session via the API.
2. **Ask a question** in plain language, or by reference (for example, a section number).
3. **Read the answer.** It is based on retrieved passages and carries citation markers.
4. **Open citations.** Each marker opens the source passage with document title, section path, version or effective date and a link to the original.
5. **Check uncertainty.** If evidence is partial, the answer says what is and is not supported.
6. **Continue the conversation.** Follow-up questions stay in the same session; history is private to you.

## Reading abstentions

When the system says it cannot answer, it means the available sources did not support an answer, not that the answer is "no". Try rephrasing, naming a section or specifying a period. If the topic is outside the collected documents, it will not be covered.

## Temporal questions

State the period you care about. Answers name the version relied on; older provisions are available for historical questions only.

## What to remember

The system covers a small curated set of documents and may be incomplete or out of date. It is not legal or tax advice; consult a qualified professional ([limitations](limitations.md)).

Related: [Generation and citations](generation-and-citations.md) · [API](api.md)
