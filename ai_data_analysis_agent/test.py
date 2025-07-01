if __name__ == "__main__":
    from utils.gorq_client import call_gorq
    prompt = "Write Python code to calculate the average temperature from a DataFrame."
    print(call_gorq(prompt))
