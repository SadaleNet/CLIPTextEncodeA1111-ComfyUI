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

def prompt_expander(text, cur_step, steps, handle_escape_character=True):
    ret = ''
    escaping = False
    depth = 0

    substitution_parameters = []
    substitution_str = ''
    for i, c in enumerate(text):
        if not escaping:
            if handle_escape_character and c == '\\':
                escaping = True
                continue
            elif c == '[':
                if depth == 0:
                    substitution_parameters = []
                    substitution_str = ''
                    depth += 1
                    continue
                depth += 1
            elif c == ']':
                depth -= 1
                if depth < 0:
                    raise Exception(f"Prompt Error: Extra closing bracket at index {i}")
                elif depth == 0:
                    substitution_parameters.append(substitution_str)
                    substitution_str = ''
                    if len(substitution_parameters) == 3 and substitution_parameters[2].replace('.','',1).isdigit():
                        threshold = round(float(substitution_parameters[2])*steps)
                        ret += prompt_expander(substitution_parameters[0] if cur_step < threshold else substitution_parameters[1], cur_step, steps, False)
                    else:
                        ret += prompt_expander(substitution_parameters[cur_step%len(substitution_parameters)], cur_step, steps, False)
                    continue
            elif depth == 1 and c == '|':
                substitution_parameters.append(substitution_str)
                substitution_str = ''
                continue

        if depth == 0:
            ret += c
        else:
            substitution_str += c
        escaping = False
    if depth != 0:
        raise Exception("Prompt Error: Missing closing bracket at the end of prompt")
    return ret

class CLIPTextEncodeA1111:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"text": ("STRING", {"multiline": True}), "clip": ("CLIP", ), "cur_step": ("INT", {"default": 0, "min": 0, "max": 10000}), "steps": ("INT", {"default": 20, "min": 1, "max": 10000}) }}
    RETURN_TYPES = ("CONDITIONING", )
    FUNCTION = "encode"

    CATEGORY = "conditioning"

    def encode(self, clip, text, cur_step, steps):
        tokens = clip.tokenize(prompt_expander(text,cur_step,steps))
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return ([[cond, {"pooled_output": pooled}]],)

class RerouteText:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"text": ("STRING", {"multiline": True}), }}
    RETURN_TYPES = ("STRING", )
    FUNCTION = "reroute"

    CATEGORY = "utils"

    def reroute(self, text):
        return (text, )

NODE_CLASS_MAPPINGS = {
    "CLIPTextEncodeA1111": CLIPTextEncodeA1111,
    "RerouteTextForCLIPTextEncodeA1111": RerouteText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CLIPTextEncodeA1111": "CLIP Text Encode A1111 (Prompt)",
    "RerouteTextForCLIPTextEncodeA1111": "Reroute Text",
}
