from workflow.graph import graph


question = "O que é educação híbrida?"


result = graph.invoke({
    "question": question,
    "attempts": 0
})


print("\n===== DECISÃO =====\n")
print(result["decision"])

print("\n===== TENTATIVAS =====\n")
print(result["attempts"])

print("\n===== RESPOSTA FINAL =====\n")
print(result["final_answer"])