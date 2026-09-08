# LangChain LCEL — Hands-On Assessment

## Overview

This project implements **LangChain Expression Language (LCEL)** concepts through a series of hands-on tasks.

The goal of the assessment is to build orchestration declaratively using LangChain Runnables instead of manually connecting each step with imperative code.

---

# Task 1 — Pipe Chain

## Objective

The objective of Task 1 is to compose at least four LangChain Runnables into a single LCEL chain and display the resulting execution graph.

Instead of manually invoking each component, the components are connected declaratively using the LCEL pipe operator (`|`).

---

## Implementation

The chain consists of the following components:

```text
Input
  ↓
Input Validation
  ↓
Prompt Template
  ↓
Chat Model
  ↓
String Output Parser
  ↓
Output Validation
```

The LCEL chain is defined as:

```python
chain = (
    validate_input_runnable
    | prompt
    | model
    | parser
    | validate_output_runnable
).with_retry(stop_after_attempt=3)
```

This gives the chain five composed Runnables:

1. `RunnableLambda(validate_input)`
2. `ChatPromptTemplate`
3. `ChatOpenRouter`
4. `StrOutputParser`
5. `RunnableLambda(validate_output)`

The output of each Runnable automatically becomes the input to the next Runnable.

---

## Dynamic Input

The query is collected from the user at runtime:

```python
user_input = input("Enter your query: ")

data = {"q": user_input}
```

The prompt uses the LCEL input variable:

```python
("human", "{q}")
```

This allows the input dictionary to flow through the chain rather than inserting a fixed query while constructing the prompt.

---

## Chain Graph

The LCEL execution graph is printed using:

```python
print(chain.get_graph().draw_ascii())
```

This provides visual evidence that the components are connected as a single Runnable pipeline.

---

## Run Task 1

From the project root:

```bash
uv run python -m pipe_chain.pipe_chain
```

The program asks for a query, invokes the LCEL chain, prints the generated response, and displays the chain graph.

To save the execution evidence:

```bash
uv run python -m pipe_chain.pipe_chain > outputs/task1_output.txt 2>&1
```

---

## Testing

Task 1 includes automated tests for both successful and invalid inputs/outputs.

The tests cover:

* Valid input acceptance
* Missing input rejection
* Valid output acceptance
* Invalid/empty output rejection

Run the tests with:

```bash
uv run python -m pytest tests/test_pipe_chain.py -v
```

Save the test evidence with:

```bash
uv run python -m pytest tests/test_pipe_chain.py -v > outputs/task1_tests.txt 2>&1
```

---

## Guardrails

The project includes reusable guardrails in `guards.py`.

### Input Validation

Input is validated before it is passed further through the chain. Invalid or missing input is rejected instead of reaching the model.

### Output Validation

Model output is validated before being returned to the caller. Empty or invalid output is rejected.

### Token Budget

A token/input budget guard is available in `guards.py` to reject requests that exceed the configured budget.

The model also uses:

```python
max_tokens=100
```

to place a limit on generated output.

### Timeout

Each model request has a configured timeout:

```python
timeout=20_000
```

This prevents a model request from waiting indefinitely.

### Retry

Retry behaviour is bounded using:

```python
.with_retry(stop_after_attempt=3)
```

The model configuration also contains a capped retry setting for provider requests.

### Secret Hygiene

Secrets and provider configuration are read from environment variables:

```python
os.environ["OPENROUTER_API_KEY"]
os.environ["MODEL_NAME"]
os.environ["BASE_URL"]
```

No API key is hardcoded in the source files.

The `.env` file containing actual credentials is excluded from version control, while `.env.example` documents the required variables without exposing their values.

---

## Task 2 — Passthrough

### Objective

Use `RunnablePassthrough.assign` to preserve the original input while adding a derived value to the same data.

### Implementation

The chain validates the input and then uses `RunnablePassthrough.assign` to calculate and add the query's word count:

```python id="0dh3sp"
chain = (
    validate_input_runnable
    | RunnablePassthrough.assign(
        word_count=RunnableLambda(count_words)
    )
)
```

For example:

```text id="0c7ebh"
Input:
{"q": "What is LCEL in LangChain?"}

Output:
{"q": "What is LCEL in LangChain?", "word_count": 5}
```

This shows that the original `q` is carried forward while `word_count` is added as a derived value.

### Run

```bash id="s9pf41"
uv run python -m passthrough.passthrough
```

Save the output:

```bash id="hlh8cc"
uv run python -m passthrough.passthrough > outputs/passthrough_output.txt 2>&1
```

### Testing

The tests verify:

* The original query is preserved and the correct word count is added.
* Invalid input is rejected.

Run:

```bash id="17s5jq"
uv run python -m pytest tests/test_passthrough.py -v
```

Save the test output:

```bash id="uvst4e"
uv run python -m pytest tests/test_passthrough.py -v > outputs/passthrough_test_output.txt 2>&1
```

### Guardrails

Input validation is applied before the passthrough operation. Invalid or missing input is rejected through the reusable validation guard.

Task 2 does not make a model/API call, so model-specific controls such as timeout and output token limits are not part of this execution path. Secrets used elsewhere in the project remain environment-based through `.env`.

