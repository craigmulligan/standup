from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""Summarize the log of git commit messages and diffs into a detailed message in markdown, appropriate for daily standup report and intended for a non-technical audience. The summary should be focused on user-facing changes ignore minor edits and grouped by author. It should be title "Daily standup".
    The git log:
```{text}```""", input_variables=['text'])
