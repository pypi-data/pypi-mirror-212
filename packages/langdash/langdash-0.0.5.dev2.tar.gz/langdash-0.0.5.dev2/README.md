# langdash

A simple library for interfacing with language models.

**Currently in alpha!**

Features:
  
  * Support for text generation, text classification (through prompting) and vector-based document searching.
  * Lightweight, build-it-yourself-style prompt wrappers.
  * Token healing and transformers/RNN state reuse for fast inference, like in [Microsoft's guidance](https://github.com/microsoft/guidance).
  * First-class support for ggml backends (currently rwkv.cpp is supported).

Documentation: [Read on readthedocs.io](https://langdash.readthedocs.io/en/latest/)

## Installation

Use [pip](https://pip.pypa.io/en/stable/) to install. By default, langdash does not come preinstalled with any additional modules, so you'll have to specify what you need like in the following command:

```
pip install --user langdash[embeddings,sentence_transformers]
```

List of modules:
  
  * **core:**
    * *embeddings:* required for running searching through embeddings
  * **backends:**
    * Supported backends include: *rwkvcpp*, *transformers*

**Note:** If you're running this from source, initialize the git submodules in the `langdash/extern` folder to compile foreign backends.
    
## Usage

See [examples folder](https://git.mysymphony.jp.net/nana/langdash/src/branch/master/examples) for full examples.

### Load a model template

```python
ld = Langdash()
ld.register_model(
  name="raven",
  model=RWKVCppModel("/path/to/ggml-raven.bin"),
)
```

### Create a prompt template, and specialize it for a model

```python
instruct_chain = ld.chain(
  args={"instruction": str},
  returns={"response": str},
  nodes=[
    ld.format_args("""\
Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Response:
"""),
    ld.returns("response", "", inference_args=InferArgs(
      typical_mass=0.8,
      # more inference arguments
    )),
  ],
)

raven_instruct_chain = instruct_chain.cached("raven")
```

### Run inference

```python
instruction = "Explain what a raven is."
raven_instruct_chain.call(args={"instruction": instruction})
```

Example output (on `ggml-RWKV-4-Raven-1B5-v11-Eng99%-Other1%-20230425-ctx4096-f16.bin` model):

```python
LDResult(returns={'response': 'A raven is a type of wild bird known for its piercing cry of \"Rra-ra-ra-ra.\" These birds are also known for their incredible agility and speed, often catching fish from waterways with ease. Rra-ra-ra-ra can be seen in the natural world and is commonly seen in the parklands and forests of Canada, the United States, Australia, and New Zealand.'}, prompt_tokens=32, completion_tokens=87)
```

## License

Apache 2.0