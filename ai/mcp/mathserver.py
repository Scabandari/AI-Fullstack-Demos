"""
Math Server using FastMCP

A simple MCP server that provides basic mathematical operations.
"""

from fastmcp import FastMCP
import math

# Create the MCP server instance
mcp = FastMCP("Math Server")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract second number from first number."""
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide first number by second number."""
    if b == 0:
        raise ValueError("Cannot divide by zero")

    return a / b


if __name__ == "__main__":
    # Run the server
    mcp.run()
