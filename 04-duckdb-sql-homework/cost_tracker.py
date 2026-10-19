from collections import defaultdict

PRICES = {
    "openai:gpt-4o-mini": (0.15, 0.60),
}

usage_totals = defaultdict(lambda: [0, 0])


def capture_usage(model, result):
    usage = result.usage
    usage_totals[model][0] += usage.input_tokens
    usage_totals[model][1] += usage.output_tokens


def display_total_usage():
    total = 0.0
    for model, (input_tokens, output_tokens) in usage_totals.items():
        input_price, output_price = PRICES[model]
        cost = (input_tokens * input_price + output_tokens * output_price) / 1_000_000
        print(f"{model}: ${cost:.6f}")
        total += cost

    print(f"Total cost: ${total:.6f}")
