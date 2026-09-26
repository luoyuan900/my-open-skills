# -*- coding: utf-8 -*-
"""本地 ComfyUI 提交/监控通用脚本（local-miora-canvas skill）。

路径 / URL 一律不写死，运行时按以下优先级解析（详见 SKILL.md「环境配置」）：
  1. 环境变量（COMFYUI_URL / KREA2_TEMPLATE / H3_R2V_TEMPLATE /
     H3_FL2V_TEMPLATE / COMFYUI_OUTPUT）
  2. 同目录 config.json（首次安装时由 agent 询问用户后写入，已加入 .gitignore）
  3. ComfyUI 服务地址尝试自动探测本机端口（8818 / 8188）
  4. 模板 / 输出目录按文件名在常见目录（Downloads / Documents / AI 等）自动查找
  5. 仍找不到 → 抛出清晰错误，提示 agent 询问用户并写入 config.json

用法：
    import sys; sys.path.insert(0, r"<skill_dir>/scripts")
    from comfy_submit import (load_template, upload, submit, wait_for, queue_free,
                             comfy_url, krea2_template, h3_r2v_template,
                             h3_fl2v_template, output_dir, save_config)

    wf = load_template(krea2_template())        # 解析 krea2 模板路径
    wf["138"]["inputs"]["value"] = PROMPT         # 按节点映射填参数
    wf["129"]["inputs"]["noise_seed"] = 20260816
    pid = submit(wf)
    fname = wait_for(pid, timeout=2700)
    local = os.path.join(output_dir(), fname)    # 产出落盘目录（同机）

规则（勿破坏）：
- submit 内置 node_errors 检查：ComfyUI 0.36+ 部分执行会假成功，必须拦截。
- wait_for 只按 prompt_id 走 /history/{pid}，禁止按文件名前缀找文件。
"""
import json
import os
import time
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")

# 本机常见 ComfyUI 端口与探测主机
_DEFAULT_HOST = "127.0.0.1"
_DEFAULT_PORTS = (8818, 8188)

# 模板 / 输出目录自动查找的根目录（最佳努力；找不到则交由用户配置）
_SEARCH_ROOTS = [
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/AI"),
    os.path.expanduser("~/ComfyUI"),
    "C:/ComfyUI", "D:/ComfyUI", "E:/ComfyUI",
]


def load_config():
    """读取同目录 config.json；不存在返回空 dict。"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(cfg):
    """把配置写回 config.json（agent 在首次安装时调用）。"""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def _reachable(url):
    try:
        urllib.request.urlopen(f"{url}/", timeout=2)
        return True
    except Exception:
        return False


def comfy_url():
    """解析 ComfyUI 服务地址：env > config > 自动探测 > 报错。"""
    if os.environ.get("COMFYUI_URL"):
        return os.environ["COMFYUI_URL"].rstrip("/")
    cfg = load_config()
    if cfg.get("comfyui_url"):
        return str(cfg["comfyui_url"]).rstrip("/")
    for port in _DEFAULT_PORTS:
        url = f"http://{_DEFAULT_HOST}:{port}"
        if _reachable(url):
            return url
    raise RuntimeError(
        "无法自动检测到 ComfyUI 服务。请设置环境变量 COMFYUI_URL，"
        "或在 config.json 写入 comfyui_url（例如 http://127.0.0.1:8818）。"
    )


def _search_file(name, max_depth=3):
    """在常见根目录按文件名做深度受限查找，找不到返回 None。"""
    for root in _SEARCH_ROOTS:
        if not os.path.isdir(root):
            continue
        for dp, dirs, fns in os.walk(root):
            if name in fns:
                return os.path.join(dp, name)
            depth = dp[len(root.rstrip(os.sep)):].count(os.sep)
            if depth >= max_depth:
                dirs[:] = []  # 不再下探，避免扫爆大目录
    return None


def _require(key, filename_hint=None):
    """解析一个必填路径：env > config > 文件名自动查找 > 报错提示。"""
    env_val = os.environ.get(key.upper())
    if env_val:
        return env_val
    cfg = load_config()
    if cfg.get(key):
        return str(cfg[key])
    if filename_hint:
        found = _search_file(filename_hint)
        if found:
            return found
    raise FileNotFoundError(
        f"未找到必需的 '{key}'。请三选一：\n"
        f"  1) 设置环境变量 {key.upper()}\n"
        f"  2) 在 config.json 写入 '{key}'\n"
        + (f"  3) 或将 '{filename_hint}' 放到常见目录（Downloads/Documents/AI）后自动发现"
           if filename_hint else "")
    )


def krea2_template():
    """krea2 图像 workflow 模板路径。"""
    return _require("krea2_template", "Krea2_samll_then_large.json")


def h3_r2v_template():
    """H3 r2v 视频 workflow 模板路径。"""
    return _require("h3_r2v_template", "video_minimax_h3_r2v_turbo_8_step.json")


def h3_fl2v_template():
    """H3 fl2v 视频 workflow 模板路径。"""
    return _require("h3_fl2v_template", "video_minimax_h3_fl2v_turbo_8_step.json")


def output_dir():
    """ComfyUI 产出落盘目录（与 ComfyUI 同机的本地路径）。"""
    return _require("output_dir")


def output_path(filename):
    """拼接产出的本地绝对路径。"""
    return os.path.join(output_dir(), filename)


def load_template(path):
    """读取 workflow 模板并深拷贝，防污染模板文件。"""
    with open(path, encoding="utf-8") as f:
        return json.loads(json.dumps(json.load(f)))


def _post(path, payload, timeout=30):
    url = comfy_url()
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{url}{path}", data=body,
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode())


def upload(img_path):
    """POST /upload/image，返回 ComfyUI 侧文件名（供 LoadImage 使用）。"""
    url = comfy_url()
    boundary = "----comfybound7d2f"
    fname = os.path.basename(img_path)
    with open(img_path, "rb") as f:
        data = f.read()
    payload = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="image"; filename="{fname}"\r\n'
        f"Content-Type: image/png\r\n\r\n"
    ).encode("utf-8") + data + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(
        f"{url}/upload/image", data=payload,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    resp = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())
    print(f"[upload] {fname} -> {resp.get('name', fname)}", flush=True)
    return resp.get("name", fname)


def queue_free():
    """返回 (running, pending) 数量；进队前检查，用户可能在 GUI 手动跑 job。"""
    url = comfy_url()
    d = json.loads(urllib.request.urlopen(f"{url}/queue", timeout=30).read().decode())
    return len(d.get("queue_running", [])), len(d.get("queue_pending", []))


def submit(wf, client_id="local_miora_canvas"):
    """POST /prompt，校验 node_errors，返回 prompt_id。有错误直接抛异常。"""
    resp = _post("/prompt", {"prompt": wf, "client_id": client_id})
    if resp.get("node_errors"):
        raise RuntimeError("[FAIL] node_errors: "
                           + json.dumps(resp["node_errors"], ensure_ascii=False)[:600])
    pid = resp["prompt_id"]
    print(f"[queue] submitted -> {pid}", flush=True)
    return pid


def wait_for(pid, timeout=2700, poll=30):
    """按 prompt_id 轮询 /history/{pid}，返回产物文件名列表（mp4/png）。

    status_str=error 时打印摘要并抛异常；超时抛 TimeoutError。
    """
    url = comfy_url()
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(poll)
        try:
            h = json.loads(urllib.request.urlopen(f"{url}/history/{pid}",
                                                  timeout=30).read().decode())
            if pid not in h:
                print("[monitor] queued/running...", flush=True)
                continue
            entry = h[pid]
            st = entry.get("status", {})
            if st.get("status_str") == "error":
                raise RuntimeError("[monitor] FAILED: "
                                   + json.dumps(st, ensure_ascii=False)[:500])
            vids = []
            for _, o in entry.get("outputs", {}).items():
                for key in ("images", "gifs"):
                    for g in o.get(key, []) or []:
                        fn = g.get("filename", "")
                        if fn.endswith((".mp4", ".png")):
                            vids.append(fn)
            if vids:
                print(f"[monitor] DONE: {vids[0]}", flush=True)
                return vids
        except RuntimeError:
            raise
        except Exception as e:  # 网络抖动重试
            print(f"[monitor] poll err {e}", flush=True)
    raise TimeoutError(f"[monitor] TIMEOUT after {timeout}s: {pid}")
