import json
import time
from argparse import ArgumentParser

from data_gen import gen_arguments
from vllm.transformers_utils.tokenizer import get_tokenizer

import sglang as sgl
from sglang.test.test_utils import (
    add_common_sglang_args_and_parse,
    select_sglang_backend,
)
from sglang.utils import dump_state_text

import random

random.seed(42)


@sgl.function
def multi_turns(s, qas):
    for qa in qas:
        s += qa["prompt"]
        s += sgl.gen(max_tokens=qa["new_tokens"], ignore_eos=True)
    return s


def main(args):
    tokenizer = get_tokenizer(args.tokenizer, trust_remote_code=args.trust_remote_code)
    # Format of original multi-turn chat benchmark
    # multi_qas -> [{'qas':[{'prompt': '1st q', 'new_tokens':4}, ... # of turns]}, {'qas':...}, ... # of qas]
    # make qas as single turn and repeat run batch for # of turns
    # multi_qas -> [{'qas':[{'prompt': '1st q', 'new_tokens':4}]}, {'qas':...}, ... # of qas] # of turns
    # while doing this, suffle each qas order
    # this will make more randomness and realistic
    turns = args.turns
    args.turns = 1
    states = []
    tic = time.time()
    for _ in range(turns):    
        multi_qas = gen_arguments(args, tokenizer)
        for i, st in enumerate(states):
            # add previous state string
            # print(multi_qas[i]['qas'])
            multi_qas[i]['qas'][0]['prompt'] = st.text() + multi_qas[i]['qas'][0]['prompt']

        # shuffle for randomness
        random.shuffle(multi_qas)

        backend = select_sglang_backend(args)

        states = multi_turns.run_batch(
            multi_qas,
            temperature=0.7,
            backend=backend,
            num_threads=args.parallel,
            progress_bar=True,
        )
        input("Waiting for user response")
        # print(states)

    latency = time.time() - tic

    print(f"Latency: {latency:.3f}")

    dump_state_text(f"tmp_output_{args.backend}.txt", states)

    with open(args.result_file, "a") as fout:
        value = {
            "task": "multi_turn_chat",
            "backend": args.backend,
            "num_gpus": 1,
            "latency": round(latency, 3),
            "num_requests": args.num_qa,
            "num_turns": args.turns,
            "other": {
                "parallel": args.parallel,
                "output_mode": "long" if args.long else "short",
            },
        }
        fout.write(json.dumps(value) + "\n")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--turns", type=int, default=4)
    parser.add_argument("--num-qa", type=int, default=1)
    parser.add_argument("--min-len-q", type=int, default=256)
    parser.add_argument("--max-len-q", type=int, default=512)
    parser.add_argument("--min-len-a", type=int, default=4)
    parser.add_argument("--max-len-a", type=int, default=8)
    parser.add_argument("--tokenizer", type=str, required=True)
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--long", action="store_true")
    args = add_common_sglang_args_and_parse(parser)

    if args.long:
        args.min_len_a = 256
        args.max_len_a = 512
        args.num_qa = 10

    print(args)
    main(args)
