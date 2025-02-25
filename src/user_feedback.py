def get_user_feedback(search_results):
    """
    Let users choose which search results are relevant and return relevant results marked by users
    """
    relevant_results = []

    print("\nPlease mark relevant results (Y/N):")
    for idx, result in enumerate(search_results):
        print(f"\nResult {idx+1} \n[\nURL: {result['url']}\nTitle: {result['title']}\nSummary: {result['snippet']}]")
        user_input = input("Is this relevant? (Y/N): ").strip().lower()

        if user_input == "y":
            relevant_results.append(result)

    return relevant_results