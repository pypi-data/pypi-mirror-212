import os
import shutil
import sys
from collections import OrderedDict

import danling as dl
import torch
from chanfig import NestedDict

from .config import build_config


def convert_ckpt(ckpt):
    if isinstance(ckpt, str):
        ckpt = dl.load(ckpt)
    ckpt = NestedDict(ckpt)
    weights = OrderedDict()
    weights["embeddings.word_embeddings.weight"] = ckpt.pop("embed_tokens.weight")
    if "embeddings.position_ids" in ckpt:
        weights["embeddings.position_ids"] = ckpt.pop("embeddings.position_ids")
    if "embeddings.position_embeddings.weight" in ckpt:
        weights["embeddings.position_embeddings.weight"] = ckpt.pop("embeddings.position_embeddings.weight")
    weights["embeddings.layer_norm.weight"] = ckpt.pop("emb_layer_norm_before.weight")
    weights["embeddings.layer_norm.bias"] = ckpt.pop("emb_layer_norm_before.bias")
    for key, value in ckpt.layers.items():
        qw, kw, vw = value.pop("self_attn.in_proj.weight").chunk(3, dim=0)
        qb, kb, vb = value.pop("self_attn.in_proj.bias").chunk(3, dim=0)
        weights[f"encoder.layer.{key}.attention.self.query.weight"] = qw
        weights[f"encoder.layer.{key}.attention.self.query.bias"] = qb
        weights[f"encoder.layer.{key}.attention.self.key.weight"] = kw
        weights[f"encoder.layer.{key}.attention.self.key.bias"] = kb
        weights[f"encoder.layer.{key}.attention.self.value.weight"] = vw
        weights[f"encoder.layer.{key}.attention.self.value.bias"] = vb
        weights[f"encoder.layer.{key}.attention.self.rotary_embeddings.inv_freq"] = value.pop(
            "self_attn.rot_emb.inv_freq"
        )
        weights[f"encoder.layer.{key}.attention.output.dense.weight"] = value.pop("self_attn.out_proj.weight")
        weights[f"encoder.layer.{key}.attention.output.dense.bias"] = value.pop("self_attn.out_proj.bias")
        weights[f"encoder.layer.{key}.attention.LayerNorm.weight"] = value.pop("self_attn_layer_norm.weight")
        weights[f"encoder.layer.{key}.attention.LayerNorm.bias"] = value.pop("self_attn_layer_norm.bias")
        weights[f"encoder.layer.{key}.intermediate.dense.weight"] = value.pop("fc1.weight")
        weights[f"encoder.layer.{key}.intermediate.dense.bias"] = value.pop("fc1.bias")
        weights[f"encoder.layer.{key}.output.dense.weight"] = value.pop("fc2.weight")
        weights[f"encoder.layer.{key}.output.dense.bias"] = value.pop("fc2.bias")
        weights[f"encoder.layer.{key}.LayerNorm.weight"] = value.pop("final_layer_norm.weight")
        weights[f"encoder.layer.{key}.LayerNorm.bias"] = value.pop("final_layer_norm.bias")
    weights["encoder.emb_layer_norm_after.weight"] = ckpt.pop("emb_layer_norm_after.weight")
    weights["encoder.emb_layer_norm_after.bias"] = ckpt.pop("emb_layer_norm_after.bias")
    weights["lm_head.dense.weight"] = ckpt.pop("lm_head.dense.weight")
    weights["lm_head.dense.bias"] = ckpt.pop("lm_head.dense.bias")
    weights["lm_head.layer_norm.weight"] = ckpt.pop("lm_head.layer_norm.weight")
    weights["lm_head.layer_norm.bias"] = ckpt.pop("lm_head.layer_norm.bias")
    weights["lm_head.decoder.weight"] = ckpt.pop("lm_head.out_proj.weight")
    weights["lm_head.decoder.bias"] = ckpt.pop("lm_head.out_proj.bias")
    return weights


def convert(path):
    ckpt = dl.load(path)
    config = build_config(path)
    if os.path.exists(config._name_or_path):
        shutil.rmtree(config._name_or_path)
    shutil.copytree(os.path.join(os.path.dirname(__file__), "template"), config._name_or_path)
    config.save_pretrained(config._name_or_path)
    ckpt = dl.load(path)
    weights = convert_ckpt(ckpt["model"])
    torch.save(weights, os.path.join(config._name_or_path, "pytorch_model.bin"))


if __name__ == "__main__":
    convert(sys.argv[1])
