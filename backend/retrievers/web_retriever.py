from ddgs import DDGS

def retrieve_web_context(question):

    context = ""

    with DDGS() as ddgs:
        results = ddgs.text(question, max_results=5)

        for r in results:
            context += f"""
		Title: {r['title']}

		Body:
		{r['body']}

		URL:
		{r['href']}

		"""

    return context