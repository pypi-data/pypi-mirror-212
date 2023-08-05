# bettertest 📝🔍

⚡ A Python testing library for automatically evaluating and tracing LLM applications ⚡

Our goal with bettertest is to simplify the process of testing and debugging LLM applications. It automatically evaluates your model's responses against your solution answers (auto-eval) and provides tracing features out-of-the-box.

With bettertest, you can automatically test your LLM applications and view print statements for each run just by adding 'bettertest' to any print statement in your code.

## Getting Started

Before using BetterTest, you need to install it via pip:

```
pip install bettertest
```

After installation, import the BetterTest library in your Python project:

```python
from bettertest import BetterTest
```
## Using BetterTest

### Initialize BetterTest

Create an instance of the BetterTest class with the user's email:

```python
bt = BetterTest("your_email@example.com")
```

Replace `"your_email@example.com"` with the appropriate email address.

### Evaluate Model Responses

The `eval()` function takes in a list of questions, a list of answers, an LLM function, and an optional `num_runs` argument. It automatically evaluates the model's response against the solution answer and provides tracing for each run. Use it as follows:

```python
questions = [...]  # List of questions
answers = [...]    # List of corresponding solution answers

def llm_function(question):
    # Your custom LLM function implementation goes here
    pass

bt = BetterTest("your_email@example.com")
bt.eval(questions, answers, llm_function)
```

Replace the `llm_function` with your LLM function, and customize `num_runs` if necessary. By default, `num_runs` is set to 1.


## Contributing

We welcome contributions to InstructPrompt! Feel free to create issues/PR's/or DM us (👋 Hi I'm Krrish - +17708783106)

## Changelog

The current version of BetterTest is `0.1.9`.

## License

BetterTest is released under the [MIT License](https://github.com/bettertest/readme/blob/master/LICENSE).
