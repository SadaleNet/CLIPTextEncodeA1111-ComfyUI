#!/usr/bin/python3
# BSD 2-Clause License
# 
# Copyright (c) 2023, Wong "Sadale" Cho Ching <https://sadale.net>
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import copy
import json
import sys

node_template = {
    "PrimitiveNode": {
      "id": 9999, "type": "PrimitiveNode", "pos": [9999,9999], "size": {"0": 210,"1": 82}, "flags": {}, "order": 9999, "mode": 0,
      "outputs": [
        {"name": "FLOAT","type": "FLOAT","links": None,"slot_index": 0,"widget": {"name": "cfg","config": ["FLOAT",{"default": 8,"min": 0,"max": 100}]}}
      ],
      "title": "DUMMY", "properties": {}, "widgets_values": None
    },
    "Reroute": { "id": 9999, "type": "Reroute", "pos": [9999, 9999], "size": [90.4, 26], "flags": {}, "order": 9999, "mode": 0,
      "inputs": [ { "name": "", "type": "*", "link": None, "slot_index": 0 } ],
      "outputs": [ { "name": "LATENT", "type": "LATENT", "links": None, "slot_index": 0 } ],
      "properties": { "showOutputText": True, "horizontal": False }
    },
    "RerouteTextForCLIPTextEncodeA1111": {
        "id": 9999, "type": "RerouteTextForCLIPTextEncodeA1111", "pos": [9999,9999],"size": [210,46],"flags": {"collapsed": True},"order": 9999,"mode": 0,
        "inputs": [{"name": "text","type": "STRING","link": None,"widget": {"name": "text","config": ["STRING",{"multiline": True}]}}],
        "outputs": [{"name": "STRING","type": "STRING","links": None,"shape": 3}],"title": "DUMMY","properties": {"Node name for S&R": "RerouteTextForCLIPTextEncodeA1111"},
        "widgets_values": [""]
    },
    "CLIPTextEncode": { "id": 9999, "type": "CLIPTextEncode", "pos": [9999, 9999], "size": {"0": 425, "1": 180 }, "flags": { "collapsed": True },
      "order": 9999, "mode": 0, "inputs": [ { "name": "clip", "type": "CLIP", "link": 9999 } ],
      "outputs": [ {"name": "CONDITIONING", "type": "CONDITIONING", "links": None, "slot_index": 0 } ],
      "title": "DUMMY", "properties": { "Node name for S&R": "CLIPTextEncode" }, "widgets_values": [ "DUMMY" ]
    },
    "CLIPTextEncodeA1111": {"id": 9999,"type": "CLIPTextEncodeA1111","pos": [9999,9999],"size": [261,124],"flags":{"collapsed": True},"order": 9999,"mode": 0,
        "inputs": [{"name": "clip","type": "CLIP","link": None,"slot_index": 0},
            {"name": "text","type": "STRING","link": None,"widget": {"name": "text","config": ["STRING",{"multiline": True}]}}],
        "outputs": [{"name": "CONDITIONING","type": "CONDITIONING","links": None,"shape": 3,"slot_index": 0}],
        "properties": {"Node name for S&R": "CLIPTextEncodeA1111"},
        "widgets_values": ["DUMMY",9999,9999]
    },
    "KSamplerAdvanced": { "id": 9999, "type": "KSamplerAdvanced", "pos": [9999, 9999], "size": [315, 334], "flags": {"collapsed": True}, "order": 9999, "mode": 0,
      "inputs": [{ "name": "model", "type": "MODEL", "link": 9999, "slot_index": 0 },
            {"name": "positive", "type": "CONDITIONING", "link": 9999, "slot_index": 1 },
            {"name": "negative", "type": "CONDITIONING", "link": 9999, "slot_index": 2 },
            {"name": "latent_image", "type": "LATENT", "link": 9999, "slot_index": 3 },
            {"name": "sampler_name", "type": "euler,euler_ancestral,heun,dpm_2,dpm_2_ancestral,lms,dpm_fast,dpm_adaptive,dpmpp_2s_ancestral,dpmpp_sde,dpmpp_sde_gpu,dpmpp_2m,dpmpp_2m_sde,dpmpp_2m_sde_gpu,ddim,uni_pc,uni_pc_bh2", "link": 9999, "widget": { "name": "sampler_name", "config": [["euler","euler_ancestral","heun","dpm_2","dpm_2_ancestral","lms","dpm_fast","dpm_adaptive","dpmpp_2s_ancestral","dpmpp_sde","dpmpp_sde_gpu","dpmpp_2m","dpmpp_2m_sde","dpmpp_2m_sde_gpu","ddim","uni_pc","uni_pc_bh2"]] } },
            {"name": "scheduler","type": "normal,karras,exponential,simple,ddim_uniform","link": 9999,"widget": {"name": "scheduler","config": [["normal","karras","exponential","simple","ddim_uniform"]]}},
            {"name": "cfg","type": "FLOAT","link": 9999,"widget": {"name": "cfg","config": ["FLOAT",{"default": 8,"min": 0,"max": 100}]}},
            {"name": "noise_seed","type": "INT","link": 9999,"widget": {"name": "noise_seed","config": ["INT",{"default": 0,"min": 0,"max": 18446744073709552000}]}}
        ],
      "outputs": [{"name": "LATENT","type": "LATENT","links": None,"shape": 3,"slot_index": 0}],
      "title": "DUMMY",
      "properties": {"Node name for S&R": "KSamplerAdvanced"},
      "widgets_values": ["disable",605756652843224,"randomize",20,8,"euler","normal",0,1,"enable"]
    }
}

json_result = {
    "last_node_id": 9999,
    "last_link_id": 9999,
    "nodes": [],
    "links": [],
    "groups": [ { "title": "Generator", "bounding": [ 9999, 9999, 9999, 9999 ], "color": "#3f789e"}],
    "config": {},
    "extra": {},
    "version": 0.4
 }

data_types = ["LATENT", "CLIP", "MODEL"]

def create_node(node_type, node_id, title, x, y):
    ret = copy.deepcopy(node_template[node_type])
    ret["id"] = node_id
    ret["order"] = node_id
    if title is not None:
        ret["title"] = title
    ret["pos"][0] = x
    ret["pos"][1] = y
    return ret

def link_node(link_id, src, src_index, dst, dst_index=0):
    if src["outputs"][src_index]["links"] is None:
        src["outputs"][src_index]["links"] = []
    src["outputs"][src_index]["links"].append(link_id)

    if src["type"] in ["PrimitiveNode", "Reroute", "RerouteTextForCLIPTextEncodeA1111"]:
        src["outputs"][src_index]["name"] = dst["inputs"][dst_index]["name"]
        src["outputs"][src_index]["type"] = dst["inputs"][dst_index]["type"]
        if "widget" in src["outputs"][src_index]:
            src["outputs"][src_index]["widget"]["name"] = dst["inputs"][dst_index]["name"]
            src["outputs"][src_index]["widget"]["config"] = dst["inputs"][dst_index]["widget"]["config"]
        
        # Special handling if we're linking to KSamplerAdvanced or CLIPTextEncode or CLIPTextEncodeA1111: Need to copy content based on the mapping of the dst node itself.
        if dst["type"] == "KSamplerAdvanced":
            mapping = {"cfg": 4, "sampler_name": 5, "scheduler": 6}
            if dst["inputs"][dst_index]["name"] == "noise_seed":
                src["widgets_values"] = [
                    dst["widgets_values"][1], # seed
                    dst["widgets_values"][2] # seed policy
                ]
            elif dst["inputs"][dst_index]["name"] in mapping:
                src["widgets_values"] = [
                    dst["widgets_values"][ mapping[dst["inputs"][dst_index]["name"]] ],
                    "fixed"
                ]
        elif dst["type"] in ["CLIPTextEncode", "CLIPTextEncodeA1111"]:
            mapping = {"text": 0}
            if dst["inputs"][dst_index]["name"] in mapping:
                src["widgets_values"] = [
                    dst["widgets_values"][ mapping[dst["inputs"][dst_index]["name"]] ]
                ]

    dst["inputs"][dst_index]["link"] = link_id

    return [link_id, src["id"], src_index, dst["id"], dst_index]
    

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <steps> [step_start inclusive (default:0)] [step_end exclusive (default:max)]")
    exit(1)

steps = int(sys.argv[1])
step_start = 0
step_end = steps
if len(sys.argv) > 2:
    step_start = int(sys.argv[2])
if len(sys.argv) > 3:
    step_end = int(sys.argv[3])

GROUP_X = 100
GROUP_Y = 100

INPUT_X = GROUP_X
INPUT_Y = GROUP_Y
model_input = create_node("Reroute", 1, None, INPUT_X, INPUT_Y+26*0)
clip_input = create_node("Reroute", 2, None, INPUT_X, INPUT_Y+26*1)
latent_input = create_node("Reroute", 3, None, INPUT_X, INPUT_Y+26*2)
positive_input = create_node("RerouteTextForCLIPTextEncodeA1111", 4, "+ve", INPUT_X, INPUT_Y+32+26*3)
negative_input = create_node("RerouteTextForCLIPTextEncodeA1111", 5, "-ve", INPUT_X, INPUT_Y+32+26*4)
latent_output = create_node("Reroute", 6, None, INPUT_X+325, INPUT_Y+26*0)

CONFIG_X = INPUT_X
CONFIG_Y = INPUT_Y+26*5+32
seed = create_node("PrimitiveNode", 7, "Seed", CONFIG_X, CONFIG_Y+(82+32)*0)
sampler = create_node("PrimitiveNode", 8, "Sampler", CONFIG_X+210, CONFIG_Y+(82+32)*0)
scheduler = create_node("PrimitiveNode", 9, "Scheduler", CONFIG_X, CONFIG_Y+(82+32)*1)
cfg = create_node("PrimitiveNode", 10, "Cfg", CONFIG_X+210, CONFIG_Y+(82+32)*1)


GENERATOR_X = GROUP_X
GENERATOR_Y = CONFIG_Y+(82+32)*2

NODE_START_INDEX = 11

link_table = []
generator_nodes = []
k_prev = None
for i in range(step_start, step_end):
    p = create_node("CLIPTextEncodeA1111", NODE_START_INDEX+i*3+0, f"P{i}", GENERATOR_X, GENERATOR_Y+(0 if i==step_start else 32)+(i-step_start)*2)
    n = create_node("CLIPTextEncodeA1111", NODE_START_INDEX+i*3+1, f"N{i}", GENERATOR_X+100, GENERATOR_Y+(0 if i==step_start else 32)+(i-step_start)*2)
    
    p["widgets_values"][0] = "beautiful scenery nature glass bottle landscape, , purple galaxy bottle,"
    n["widgets_values"][0] = "text, watermark"
    p["widgets_values"][1] = i
    n["widgets_values"][1] = i
    p["widgets_values"][2] = step_end-step_start
    n["widgets_values"][2] = step_end-step_start
    
    link_table.append(link_node(len(link_table)+1, clip_input, 0, p, 0))
    link_table.append(link_node(len(link_table)+1, clip_input, 0, n, 0))
    link_table.append(link_node(len(link_table)+1, positive_input, 0, p, 1))
    link_table.append(link_node(len(link_table)+1, negative_input, 0, n, 1))
    k = create_node("KSamplerAdvanced", NODE_START_INDEX+i*3+2, f"K{i}", GENERATOR_X+200, GENERATOR_Y+(0 if i==step_start else 32)+(i-step_start)*2)
    k["widgets_values"] = [
        "enable" if i==0 else "disable", # add_noise
        156680208700286 if i==0 else 0, # seed
        "randomize" if i==0 else "fixed", # seed policy
        steps, # steps
        8.0, # cfg
        "euler", # sampler
        "normal", # schedule
        i, # start at step
        i+1, # end at step
        "disable" if i==steps-1 else "enable" # return with noise
    ]
    link_table.append(link_node(len(link_table)+1, model_input, 0, k, 0))
    link_table.append(link_node(len(link_table)+1, p, 0, k, 1))
    link_table.append(link_node(len(link_table)+1, n, 0, k, 2))
    link_table.append(link_node(len(link_table)+1, sampler, 0, k, 4))
    link_table.append(link_node(len(link_table)+1, scheduler, 0, k, 5))
    link_table.append(link_node(len(link_table)+1, cfg, 0, k, 6))
    
    if i == 0:
        link_table.append(link_node(len(link_table)+1, seed, 0, k, 7))
    else:
        k["inputs"] = k["inputs"][:-1] # No noise seed input for the remaining nodes
    if k_prev is None:
        link_table.append(link_node(len(link_table)+1, latent_input, 0, k, 3))
    else:
        link_table.append(link_node(len(link_table)+1, k_prev, 0, k, 3)) # link the previous latent output to the current latent input
    k_prev = k
    generator_nodes += [p, n, k]
    if i == step_end-1:
        link_table.append(link_node(len(link_table)+1, k, 0, latent_output))

json_result["groups"][0]["bounding"] = [GROUP_X, GROUP_Y-40, 420, (GENERATOR_Y-GROUP_Y)+80+(step_end-step_start)*2]
json_result["groups"][0]["title"] = f"Step {step_start}-{step_end-1}"
json_result["nodes"] = [seed, sampler, scheduler, cfg, model_input, clip_input, latent_input, positive_input, negative_input, latent_output] + generator_nodes
json_result["links"] = link_table
json_result["last_node_id"] = len(json_result["nodes"])
json_result["last_link_id"] = len(json_result["links"])

print(json.dumps(json_result, indent=4))
