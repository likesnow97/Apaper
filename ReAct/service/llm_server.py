import os
import uvloop

from vllm.entrypoints.openai.api_server import run_server
from vllm.entrypoints.openai.cli_args import (
    make_arg_parser,
    validate_parsed_serve_args,
)
from vllm.entrypoints.serve.utils.api_utils import cli_env_setup
from vllm.utils.argparse_utils import FlexibleArgumentParser


MODEL_PATH = os.environ.get(
    "MODEL_PATH", "/data/snow/modlib/model/Qwen/Qwen3-VL-8B-Instruct"
)
SERVED_MODEL_NAME = os.environ.get("SERVED_MODEL_NAME", "qwen3-vl-8b")
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
GPU_DEVICES = os.environ.get("CUDA_VISIBLE_DEVICES", "1")

if not LLM_API_KEY:
    raise SystemExit("未设置环境变量 LLM_API_KEY，请先设置再运行。")

os.environ["CUDA_VISIBLE_DEVICES"] = GPU_DEVICES


def main():
    cli_env_setup()

    parser = FlexibleArgumentParser(
        description="vLLM OpenAI-Compatible API Server"
    )

    parser = make_arg_parser(parser)

    args = parser.parse_args([
        "--model", MODEL_PATH,
        "--served-model-name", SERVED_MODEL_NAME,
        "--host", "127.0.0.1",
        "--port", "8765",
        "--tensor-parallel-size", "1",
        "--gpu-memory-utilization", "0.90",
        "--max-model-len", "8192",
        "--dtype", "auto",
        "--api-key", LLM_API_KEY,
    ])

    validate_parsed_serve_args(args)

    uvloop.run(run_server(args))


if __name__ == "__main__":
    main()
