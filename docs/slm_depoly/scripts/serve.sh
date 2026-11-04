#!/usr/bin/env bash
# Run on DGX Spark. This starts inference only; no KG or agent tools are mounted.
set -euo pipefail
: "${SLM_STATE:?Set SLM_STATE to the absolute deployment-state directory}"
: "${SPARK_BIND_IP:?Set SPARK_BIND_IP to the Spark LAN address or 127.0.0.1}"
SLM_STATE="$(cd -- "$SLM_STATE" && pwd)"
SLM_IMAGE_DIGEST="$(cat "$SLM_STATE/image.digest")"
[[ "$SLM_IMAGE_DIGEST" == *@sha256:* ]] || { echo 'Pin the image digest first' >&2; exit 1; }
[[ -f "$SLM_STATE/runtime.secrets.env" ]] || { echo 'Missing API key env file' >&2; exit 1; }
[[ -f "$SLM_STATE/weights/model.lock.json" ]] || { echo 'Complete the model download first' >&2; exit 1; }
python3 - "$SLM_STATE" "$SPARK_BIND_IP" <<'PY'
import ipaddress, json, sys
from pathlib import Path
root = Path(sys.argv[1])
address = ipaddress.ip_address(sys.argv[2])
allowed = [ipaddress.ip_network(n) for n in ('10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16')]
if address.version != 4 or not (address.is_loopback or any(address in n for n in allowed)):
    raise SystemExit('Use a loopback or private IPv4 bind address')
lock = json.loads((root / 'weights/model.lock.json').read_text())
if Path(lock['model_dir']).resolve() != (root / 'weights/model').resolve():
    raise SystemExit('Model lock points to another deployment directory')
config = json.loads((root / 'weights/model/config.json').read_text())
if config.get('quantization_config'):
    raise SystemExit('This launcher is for BF16 checkpoints; use a separate quantized recipe')
if not any(line.startswith('VLLM_API_KEY=') and len(line.split('=', 1)[1]) >= 32
           for line in (root / 'runtime.secrets.env').read_text().splitlines()):
    raise SystemExit('Missing or too-short VLLM_API_KEY')
PY
extra=()
case "${SLM_MODEL_FAMILY:-qwen35}" in
    qwen35) extra+=(--language-model-only) ;;
    qwen3) ;;
    *) echo 'SLM_MODEL_FAMILY must be qwen35 or qwen3' >&2; exit 1 ;;
esac
command=(docker run -d --name "${SLM_CONTAINER_NAME:-ants-registry-slm}"
    --platform linux/arm64 --gpus all --network host --ipc=host
    --restart no --env-file "$SLM_STATE/runtime.secrets.env"
    -e HF_HUB_OFFLINE=1 -e TRANSFORMERS_OFFLINE=1
    -e HF_HUB_DISABLE_TELEMETRY=1 -e VLLM_NO_USAGE_STATS=1 -e DO_NOT_TRACK=1
    --mount "type=bind,src=$SLM_STATE/weights/model,dst=/model,readonly"
    --entrypoint vllm "$SLM_IMAGE_DIGEST" serve /model
    --host "$SPARK_BIND_IP" --port "${SLM_PORT:-8000}"
    --served-model-name registry-slm --dtype bfloat16 --tensor-parallel-size 1
    --max-model-len 8192 --max-num-seqs "${SLM_MAX_NUM_SEQS:-2}"
    --max-num-batched-tokens 8192 --gpu-memory-utilization "${SLM_MEMORY_FRACTION:-0.70}"
    --generation-config vllm --seed 20261026
    --reasoning-parser qwen3 --enforce-eager --no-enable-prefix-caching
    "${extra[@]}")
if [[ "${1:-}" == --dry-run ]]; then
    printf '%q ' "${command[@]}"
    printf '\n'
elif [[ $# -eq 0 ]]; then
    "${command[@]}"
else
    echo 'Usage: bash serve.sh [--dry-run]' >&2
    exit 1
fi
