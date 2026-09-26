# -*- coding: utf-8 -*-
"""本地 ComfyUI 提交/监控通用脚本（local-miora-canvas skill）。

用法：
    import sys; sys.path.insert(0, r"<skill_dir>/scripts")
    from comfy_submit import load_template, upload, submit, wait_for, queue_free

    wf = load_template(r"C:/Users/luo/Downloads/comfyuiapi/video_minimax_h3_r2v_turbo_8_step.json")
    wf["138"]["inputs"]["value"] = PROMPT          # 按节点映射填参数
    wf["129"]["inputs"]["noise_seed"] = 20260816
    pid = submit(wf)
    fname = wait_for(pid, timeout=2700)

规则（勿破坏）：
- submit 内置 node_errors 检查：ComfyUI 0.36+ 部分执行会假成功，必须拦截。
- wait_for 只按 prompt_id 走 /history/{pid}，禁止按文件名前缀找文件。
"""
import json
import os
import time
import urllib.request

COMFY = "http://127.0.0.1:8818"


def load_template(path):
    """读取 workflow 模板并深拷贝，防污染模板文件。"""
    with open(path, encoding="utf-8") as f:
        return json.loads(json.dumps(json.load(f)))


def _post(path, payload, timeout=30):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{COMFY}{path}", data=body,
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode())


def upload(img_path):
    """POST /upload/image，返回 ComfyUI 侧文件名（供 LoadImage 使用）。"""
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
        f"{COMFY}/upload/image", data=payload,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    resp = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())
    print(f"[upload] {fname} -> {resp.get('name', fname)}", flush=True)
    return resp.get("name", fname)


def queue_free():
    """返回 (running, pending) 数量；进队前检查，用户可能在 GUI 手动跑 job。"""
    d = json.loads(urllib.request.urlopen(f"{COMFY}/queue", timeout=30).read().decode())
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
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(poll)
        try:
            h = json.loads(urllib.request.urlopen(f"{COMFY}/history/{pid}",
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


def output_path(filename,
                out_dir=r"C:/Users/luo/AI/Comfyui/ComfyUI/ComfyUI/output"):
    return os.path.join(out_dir, filename)
