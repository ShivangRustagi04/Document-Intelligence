def test_example_1():
    prompt = "Extract bureau score and overdue amount from CRIF report"

    explanation = """
    Bureau score is extracted from the 'CRIF HM Score(S)' section.
    Total overdue amount is extracted from the Account Summary table.
    """

    key_mappings = {
        "bureau_score": "CRIF HM Score(S) Section",
        "total_overdue_amount": "Account Summary Table"
    }

    print("PROMPT:")
    print(prompt)
    print("\nEXPLANATION:")
    print(explanation.strip())
    print("\nKEY MAPPINGS:")
    print(key_mappings)


def test_example_2():
    prompt = "Extract monthly sales from GSTR-3B return"

    explanation = """
    Monthly sales correspond to Table 3.1(a) – Outward taxable supplies.
    The filing period determines the month.
    """

    key_mappings = {
        "month": "GSTR-3B Filing Period",
        "sales": "Table 3.1(a)"
    }

    print("\n-------------------------")
    print("PROMPT:")
    print(prompt)
    print("\nEXPLANATION:")
    print(explanation.strip())
    print("\nKEY MAPPINGS:")
    print(key_mappings)


if __name__ == "__main__":
    test_example_1()
    test_example_2()