import random
def generate_option_line():
    stock_price = random.uniform(40, 110)
    strike_price = random.uniform(40, 110)
    risk_free_rate = random.uniform(0.05, 0.1)
    dividend_yield = 0.00  # Assuming a constant value
    volatility = random.uniform(0.1, 0.3)
    time_to_expiration = random.uniform(0.1, 1.0)
    option_type = random.choice(["C", "P"])
    additional_values = [0.00, random.uniform(0, 22)]  # Example of the additional values
    line = [stock_price, strike_price, risk_free_rate, dividend_yield, volatility, time_to_expiration, option_type] + additional_values
    return " ".join(f"{value:.10f}" if isinstance(value, float) else value for value in line)
def main():
    num_options = 21000000
    with open("blackscholes_input.data", "w") as file:
        file.write(str(num_options) + '\n')
        for _ in range(num_options):
            file.write(generate_option_line() + '\n')
    print(f"{num_options} lines written to blackscholes_input.data")
if __name__ == "__main__":
    main()