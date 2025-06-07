#!/usr/bin/env python3
"""
DeepSeek Coder Generator MCP Server

This MCP server provides code generation capabilities using OpenAI compatible APIs,
specifically optimized for DeepSeek Coder and other coding-focused models.
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import FastMCP
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration from environment variables
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "deepseek-reasoner")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "8000"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))

if not API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

# Initialize OpenAI client with custom base URL for DeepSeek or other compatible APIs
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# Create FastMCP server
mcp = FastMCP(
    name="DeepSeekCoderGenerator",
    instructions="""
    This is a code generation server that uses OpenAI compatible APIs (DeepSeek Coder, etc.) to generate code.
    
    Available tools:
    - generate_code: Generate code based on requirements and programming language
    - explain_code: Explain existing code and provide documentation
    - refactor_code: Refactor and improve existing code
    - debug_code: Help debug code and suggest fixes
    - generate_tests: Generate unit tests for given code
    - code_review: Perform code review and suggest improvements
    
    The server supports various programming languages including Python, JavaScript, TypeScript, 
    Java, C++, Go, Rust, and more.
    """,
)

class CodeGenerationRequest(BaseModel):
    """Request model for code generation"""
    requirements: str = Field(description="Description of what the code should do")
    language: str = Field(description="Programming language (e.g., python, javascript, java)")
    style: Optional[str] = Field(default="clean", description="Code style preference (clean, functional, oop)")
    include_comments: bool = Field(default=True, description="Whether to include comments")
    include_tests: bool = Field(default=False, description="Whether to include basic tests")

class CodeExplanationRequest(BaseModel):
    """Request model for code explanation"""
    code: str = Field(description="The code to explain")
    language: Optional[str] = Field(default=None, description="Programming language if not auto-detectable")
    detail_level: str = Field(default="medium", description="Detail level: basic, medium, detailed")

class CodeRefactorRequest(BaseModel):
    """Request model for code refactoring"""
    code: str = Field(description="The code to refactor")
    language: Optional[str] = Field(default=None, description="Programming language if not auto-detectable")
    goals: List[str] = Field(default=["readability", "performance"], description="Refactoring goals")

def create_system_prompt(task_type: str, language: str = None) -> str:
    """Create system prompt based on task type"""
    base_prompt = "You are an expert software engineer and code generator."
    
    prompts = {
        "generate": f"""
{base_prompt}
Generate clean, efficient, and well-documented code based on the given requirements.
Follow best practices for the specified programming language.
Include appropriate error handling and edge case considerations.
Make the code production-ready and maintainable.
""",
        "explain": f"""
{base_prompt}
Analyze and explain the provided code clearly and comprehensively.
Break down complex logic into understandable parts.
Explain the purpose, functionality, and any notable patterns or techniques used.
""",
        "refactor": f"""
{base_prompt}
Refactor the provided code to improve its quality while maintaining functionality.
Focus on readability, performance, maintainability, and following best practices.
Explain the changes made and why they improve the code.
""",
        "debug": f"""
{base_prompt}
Analyze the provided code for potential bugs, issues, or improvements.
Identify syntax errors, logical errors, performance issues, and security concerns.
Provide specific suggestions and corrected code where applicable.
""",
        "test": f"""
{base_prompt}
Generate comprehensive unit tests for the provided code.
Include edge cases, error conditions, and various input scenarios.
Use appropriate testing frameworks for the specified language.
""",
        "review": f"""
{base_prompt}
Perform a thorough code review of the provided code.
Check for code quality, best practices, potential issues, and improvements.
Provide constructive feedback and specific recommendations.
"""
    }
    
    return prompts.get(task_type, prompts["generate"])

async def call_openai_api(messages: List[Dict[str, str]], model: str = None) -> str:
    """Call OpenAI compatible API and return response"""
    try:
        response = client.chat.completions.create(
            model=model or DEFAULT_MODEL,
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"API call failed: {e}")
        raise Exception(f"Code generation failed: {str(e)}")

@mcp.tool()
async def generate_code(
    requirements: str,
    language: str,
    style: str = "clean",
    include_comments: bool = True,
    include_tests: bool = False
) -> str:
    """
    Generate code based on requirements and specifications.
    
    Args:
        requirements: Description of what the code should do
        language: Programming language (e.g., python, javascript, java, cpp, go, rust)
        style: Code style preference (clean, functional, oop)
        include_comments: Whether to include explanatory comments
        include_tests: Whether to include basic tests
    
    Returns:
        Generated code as a string
    """
    
    system_prompt = create_system_prompt("generate", language)
    
    user_prompt = f"""
Generate {language} code with the following requirements:

Requirements: {requirements}

Style preference: {style}
Include comments: {include_comments}
Include tests: {include_tests}

Please provide clean, efficient, and well-structured code that follows best practices for {language}.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        result = await call_openai_api(messages)
        return result
    except Exception as e:
        return f"Error generating code: {str(e)}"

@mcp.tool()
async def explain_code(
    code: str,
    language: str = None,
    detail_level: str = "medium"
) -> str:
    """
    Explain existing code and provide documentation.
    
    Args:
        code: The code to explain
        language: Programming language (auto-detected if not specified)
        detail_level: Level of detail (basic, medium, detailed)
    
    Returns:
        Detailed explanation of the code
    """
    
    system_prompt = create_system_prompt("explain", language)
    
    user_prompt = f"""
Please explain the following code with {detail_level} level of detail:

```{language or ''}
{code}
```

Provide a clear explanation of:
1. What the code does
2. How it works
3. Key components and their purposes
4. Any notable patterns or techniques used
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        result = await call_openai_api(messages)
        return result
    except Exception as e:
        return f"Error explaining code: {str(e)}"

@mcp.tool()
async def refactor_code(
    code: str,
    language: str = None,
    goals: List[str] = None
) -> str:
    """
    Refactor and improve existing code.
    
    Args:
        code: The code to refactor
        language: Programming language (auto-detected if not specified)
        goals: List of refactoring goals (e.g., readability, performance, maintainability)
    
    Returns:
        Refactored code with explanations
    """
    
    if goals is None:
        goals = ["readability", "performance", "maintainability"]
    
    system_prompt = create_system_prompt("refactor", language)
    
    user_prompt = f"""
Please refactor the following code focusing on: {', '.join(goals)}

```{language or ''}
{code}
```

Provide:
1. The refactored code
2. Explanation of changes made
3. Benefits of the refactoring
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        result = await call_openai_api(messages)
        return result
    except Exception as e:
        return f"Error refactoring code: {str(e)}"

@mcp.tool()
async def debug_code(
    code: str,
    language: str = None,
    error_message: str = None
) -> str:
    """
    Help debug code and suggest fixes.
    
    Args:
        code: The code to debug
        language: Programming language (auto-detected if not specified)
        error_message: Any error message encountered (optional)
    
    Returns:
        Debug analysis and suggested fixes
    """
    
    system_prompt = create_system_prompt("debug", language)
    
    user_prompt = f"""
Please analyze the following code for bugs and issues:

```{language or ''}
{code}
```

{f"Error message: {error_message}" if error_message else ""}

Please provide:
1. Identified issues or potential bugs
2. Suggested fixes
3. Corrected code if applicable
4. Prevention tips
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        result = await call_openai_api(messages)
        return result
    except Exception as e:
        return f"Error debugging code: {str(e)}"

@mcp.tool()
async def generate_tests(
    code: str,
    language: str = None,
    test_framework: str = None
) -> str:
    """
    Generate unit tests for given code.
    
    Args:
        code: The code to generate tests for
        language: Programming language (auto-detected if not specified)
        test_framework: Preferred testing framework (auto-selected if not specified)
    
    Returns:
        Generated unit tests
    """
    
    system_prompt = create_system_prompt("test", language)
    
    user_prompt = f"""
Generate comprehensive unit tests for the following code:

```{language or ''}
{code}
```

{f"Use {test_framework} testing framework." if test_framework else "Use the most appropriate testing framework for this language."}

Include:
1. Basic functionality tests
2. Edge cases
3. Error condition tests
4. Mock data where appropriate
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        result = await call_openai_api(messages)
        return result
    except Exception as e:
        return f"Error generating tests: {str(e)}"

@mcp.tool()
async def code_review(
    code: str,
    language: str = None,
    focus_areas: List[str] = None
) -> str:
    """
    Perform code review and suggest improvements.
    
    Args:
        code: The code to review
        language: Programming language (auto-detected if not specified)
        focus_areas: Specific areas to focus on (e.g., security, performance, style)
    
    Returns:
        Code review with suggestions and improvements
    """
    
    if focus_areas is None:
        focus_areas = ["code quality", "best practices", "security", "performance"]
    
    system_prompt = create_system_prompt("review", language)
    
    user_prompt = f"""
Please perform a code review focusing on: {', '.join(focus_areas)}

```{language or ''}
{code}
```

Provide:
1. Overall assessment
2. Specific issues found
3. Improvement suggestions
4. Best practice recommendations
5. Security considerations (if applicable)
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        result = await call_openai_api(messages)
        return result
    except Exception as e:
        return f"Error performing code review: {str(e)}"

def main():
    """Main entry point for the MCP server"""
    logger.info("Starting DeepSeek Coder Generator MCP Server...")
    logger.info(f"Using base URL: {BASE_URL}")
    logger.info(f"Default model: {DEFAULT_MODEL}")
    
    # Run the MCP server
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()