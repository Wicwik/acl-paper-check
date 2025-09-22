import torch

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


def apply_test_template(message, tokenizer):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that knows everything about research institutes in the world. When asked, reply only with the country.",
        },
        {"role": "user", "content": message},
    ]
    return tokenizer.apply_chat_template(
        [messages], tokenize=False, add_generation_prompt=True
    )


def predict(sentence, model, tokenizer):
    sentence = apply_test_template(sentence, tokenizer)

    # print(sentence)

    pipe = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=16,
        do_sample=False,
        top_p=None,
        temperature=None,
        use_cache=False,
        device="cuda",
    )

    result = pipe(sentence)[0]

    if "deepseek-llm" in model.config.name_or_path.lower():
        answer = result[0]["generated_text"].split("Assistant:")[-1].strip()
    else:
        answer = (
            result[0]["generated_text"]
            .split("label:<|eot_id|><|start_header_id|>assistant<|end_header_id|>")[-1]
            .strip()
        )

    return answer


def get_model():
    model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Meta-Llama-3.1-8B-Instruct",
        torch_dtype=torch.bfloat16,
    ).to("cuda")
    model.active_adapters = [
        "default"
    ]  # fix because llama has some active adapters for some reason

    tokenizer = AutoTokenizer.from_pretrained(
        "meta-llama/Meta-Llama-3.1-8B-Instruct",
        trust_remote_code=True,
        padding_side="right",
    )

    tokenizer.add_special_tokens({"pad_token": "<|reserved_special_token_0|>"})
    model.config.pad_token_id = tokenizer.pad_token_id
    model.generation_config.pad_token_id = tokenizer.pad_token_id

    return model, tokenizer
