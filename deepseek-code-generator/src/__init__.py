"""
DeepSeek Coder Generator MCP Server

A Model Context Protocol (MCP) server that provides code generation capabilities
using OpenAI compatible APIs, specifically optimized for DeepSeek Coder and other
coding-focused language models.
"""

__version__ = "0.1.0"
__author__ = "MCP Server Developer"
__description__ = "MCP server for generating code using OpenAI compatible APIs"

from .server import main

__all__ = ["main"]