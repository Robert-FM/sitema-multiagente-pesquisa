from workflow.graph import graph


question = "Quais são as principais aplicações de Machine Learning na área ambiental?"


result = graph.invoke({
    "question": question
})


print("\n===== RESPOSTA FINAL =====\n")

print(result["final_answer"])