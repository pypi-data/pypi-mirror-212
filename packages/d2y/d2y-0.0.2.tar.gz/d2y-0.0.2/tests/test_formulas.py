# tests/test_formulas.py
import unittest
from datetime import datetime
from d2y.formulas import *
from d2y.enums import *
import pytz


class TestFormulas(unittest.TestCase):
    def setUp(self):
        self.S = 100  # Current stock price
        self.K = 100  # Strike price of the option
        self.T = datetime(2023, 12, 29, 8, 0, 0, tzinfo=pytz.UTC)  # Expiration date
        self.r = 0.05  # Annual risk-free interest rate
        self.sigma = 0.2  # Annual volatility of the stock price
        self.C = 10  # Option price

    def test_calculate_option_price(self):
        print("\n****** GETTING CALL/PUT price ******\n")
        call_price = calculate_option_price(
            self.S, self.K, self.T, self.r, self.sigma, OptionType.CALL
        )
        put_price = calculate_option_price(
            self.S, self.K, self.T, self.r, self.sigma, OptionType.PUT
        )
        print("Call price:", call_price)
        print("Put price:", put_price)

    def test_newton_raphson_volatility(self):
        print("\n****** GETTING VOLATILITY ******\n")
        vol = newton_raphson_volatility(
            self.S, self.K, self.T, self.r, self.C, OptionType.CALL
        )
        print("Volatility:", vol)

    def test_brenner_subrahmanyam_approximation(self):
        print("\n****** GETTING APPROXIMATION ******\n")
        approx = brenner_subrahmanyam_approximation(
            self.S, self.K, self.T, self.r, self.C, OptionType.CALL
        )
        print("Approximation:", approx)

    def test_black_scholes_delta(self):
        print("\n****** GETTING DELTA ******\n")
        delta = black_scholes_delta(
            self.S, self.K, self.T, self.r, self.sigma, OptionType.CALL
        )
        print("Delta:", delta)

    def test_black_scholes_vega(self):
        print("\n****** GETTING VEGA ******\n")
        vega = black_scholes_vega(self.S, self.K, self.T, self.r, self.sigma)
        print("Vega:", vega)

    def test_black_scholes_gamma(self):
        print("\n****** GETTING GAMMA ******\n")
        gamma = black_scholes_gamma(self.S, self.K, self.T, self.r, self.sigma)
        print("Gamma:", gamma)

    def test_black_scholes_rho(self):
        print("\n****** GETTING RHO ******\n")
        rho = black_scholes_rho(
            self.S, self.K, self.T, self.r, self.sigma, OptionType.CALL
        )
        print("Rho:", rho)

    def test_black_scholes_theta(self):
        print("\n****** GETTING THETA ******\n")
        theta = black_scholes_theta(
            self.S, self.K, self.T, self.r, self.sigma, OptionType.CALL
        )
        print("Theta:", theta)


if __name__ == "__main__":
    unittest.main()
