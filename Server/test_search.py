from ai.llm_client import ask_llm

# Test query 1
query1 = "pics in blue shirt"
keywords1 = ask_llm(f"Extract important visual keywords from this query: {query1}")
print(f"Query: '{query1}'")
print(f"Keywords: {keywords1}\n")

# Test query 2
query2 = "me and my dog in the beach"
keywords2 = ask_llm(f"Extract important visual keywords from this query: {query2}")
print(f"Query: '{query2}'")
print(f"Keywords: {keywords2}\n")
