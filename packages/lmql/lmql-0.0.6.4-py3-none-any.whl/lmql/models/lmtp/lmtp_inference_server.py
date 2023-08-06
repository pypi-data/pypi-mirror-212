"""
HuggingFace Transformers LMTP inference server implementation.

To run an instance of this LMTP server, run e.g. the following command:

lmql serve-model --cuda gpt2-medium

See lmtp_client for an example how to connect to this server via 'websocket'.
"""

import sys
import aiohttp
from aiohttp import web
import asyncio
import json
import pickle
from dataclasses import dataclass
from queue import Queue, Empty as QueueEmpty
import threading
import time
import torch
import atexit
from typing import Optional, Tuple

from transformers import AutoModelForCausalLM

class LMTPCannotLoadModelByPolicy(Exception):
    pass

@dataclass
class GenerateCall:
    prompt: str
    logit_bias: dict
    kwargs: dict
    stream_id: int
    result_queue: Queue

    def put(self, token):
        self.result_queue.put(token)

    def error(self, msg):
        self.result_queue.put({
            "stream_id": self.stream_id,
            "error": msg
        })

    def generation_mode(self):
        is_score = self.kwargs.get("score", False)
        if is_score: return "score"
        # string that describes the generation mode for this call (same string = can run in batch)
        return f"{self.kwargs.get('temperature', 0.0)}"

@dataclass
class GenerateBatch:
    input_ids: list
    attention_mask: list
    
    temperature: float
    max_tokens: int
    logit_biases: list

    calls: list

    is_score: bool = False
    scoring_offsets: list = None
    
    @classmethod
    def from_calls(cls, calls):
        input_ids = [c.prompt for c in calls]
        max_len = max(len(ids) for ids in input_ids)
        input_ids = [[0] * (max_len - len(ids)) + ids for ids in input_ids]
        attention_mask = [[0] * (max_len - len(ids)) + [1] * len(ids) for ids in input_ids]
        
        temperature = calls[0].kwargs.get("temperature", 0.0)
        max_tokens = max(c.kwargs.get("max_tokens", 32) for c in calls)
        logit_biases = [c.logit_bias or {} for c in calls]
        
        is_score = any(c.kwargs.get("score", False) for c in calls)
        assert not is_score or all(c.kwargs.get("score", False) for c in calls), "cannot mix score and non-score calls in batch"
        
        if is_score:
            scoring_offsets = []
            for i, c in enumerate(calls):
                padding = max_len - len(c.prompt)
                scoring_offsets.append(c.kwargs.get("scoring_offset", 0) + padding)
        else:
            scoring_offsets = None

        return cls(input_ids, attention_mask, temperature, max_tokens, logit_biases, calls, is_score, scoring_offsets)

    def logits_processors(self):
        bias_tensors = None
        logit_biases = self.logit_biases
        
        if len(logit_biases) == 0:
            return []

        class BatchLogitsProcessor:
            def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
                nonlocal bias_tensors

                vocab_size = scores.shape[-1]
                if bias_tensors is None:
                    bias_tensors = [torch.zeros(vocab_size) for _ in logit_biases]
                    for i, bias in enumerate(logit_biases):
                        if len(bias) > 0:
                            indices = torch.tensor(list(bias.keys()), dtype=torch.long)
                            values = torch.tensor(list(bias.values()), dtype=torch.float32)
                            bias_tensors[i][indices] = values
                    bias_tensors = torch.stack(bias_tensors).to(scores.device)

                return scores + bias_tensors

        return [BatchLogitsProcessor()]

    def generate_args(self):
        return {
            "input_ids": torch.tensor(self.input_ids),
            "do_sample": self.temperature > 0.0,
            "attention_mask": torch.tensor(self.attention_mask),
            "temperature": self.temperature,
            "max_new_tokens": self.max_tokens,
            "logits_processor": self.logits_processors(),
            "output_scores": True,
            "return_dict_in_generate": True,
            **({"scoring_offsets": self.scoring_offsets} if self.is_score else {})
        }

class ScoreStreamer:
    def log_token(self, batch: GenerateBatch, all_scores: torch.FloatTensor, **kwargs):
        batch_size = all_scores.shape[0]
        
        for i in range(batch_size):
            offset = batch.scoring_offsets[i]
            scores = all_scores[i][offset:]
            scored_ids = batch.input_ids[i][offset:]
            call = batch.calls[i]

            for i, (score, token) in enumerate(zip(scores, scored_ids)):
                token_payload = {
                    "token": int(token),
                    "stream_id": call.stream_id,
                    "logprob": float(score),
                    "finish_reason": "stop" if i == len(scores) - 1 else None
                }
                call.put(token_payload)

class TokenStreamer:
    def __init__(self, batch: GenerateBatch, eos_token_id):
        self.batch = batch
        self.eos_token_id = eos_token_id

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        self.log_token(input_ids, scores, **kwargs)
        return False

    def log_token(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, last=False, **kwargs):
        batch_size = input_ids.shape[0]
        
        last_tokens = input_ids[:, -1]
        last_scores = scores[-1]
        
        max_num_top_logprobs = max([c.kwargs.get("top_logprobs", 1) for c in self.batch.calls])

        # for each sample get top logprobs
        top_logprobs = torch.topk(last_scores, max_num_top_logprobs, dim=-1, largest=True, sorted=True)
        for i in range(batch_size):
            logprobs = top_logprobs.values[i]
            tokens = top_logprobs.indices[i]
            token_score = last_scores[i][last_tokens[i]]

            num_top_logprobs = self.batch.calls[i].kwargs.get("top_logprobs", 1)
            logprobs = logprobs[:num_top_logprobs]
            tokens = tokens[:num_top_logprobs]

            token_payload = {
                "token": int(last_tokens[i].item()),
                "stream_id": self.batch.calls[i].stream_id,
                "logprob": float(token_score.item()),
                "finish_reason": ("stop" if last_tokens[i].item() == self.eos_token_id else "length" if last else None),
                "top_logprobs": {
                    int(token.item()): float(logprob.item()) for logprob, token in zip(logprobs, tokens)
                }
            }

            self.batch.calls[i].put(token_payload)

class Scheduler:
    """
    A scheduler that takes calls to generate and batches them together. 

    Can be shared between multiple clients, make sure to call unregister(<user>) when done,
    to allow the scheduler to shut down when no longer needed by anyone.
    """
    def __init__(self, model_identifier, model_args = None):
        self.model_identifier = model_identifier
        if model_args is None: self.model_args = {}
        else: self.model_args = model_args
        
        self.queue = Queue()
        self.kill_event = threading.Event()
        
        self.worker_thread = threading.Thread(target=self.worker, daemon=True)
        self.worker_thread.start()

        self.users = set()
        self.last_use = time.time()

    def put(self, call: GenerateCall):
        self.queue.put(call)

    def batches(self):
        start = time.time()
        calls = []
        # get as many calls from the queue as possible within 0.1 seconds
        while time.time() - start < 0.1:
            try:
                calls.append(self.queue.get_nowait())
            except QueueEmpty:
                break
        # group calls into batches
        batches_by_mode = {}
        for c in calls:
            mode = c.generation_mode()
            batches_by_mode.setdefault(mode, []).append(c)
        return batches_by_mode.values()

    def score(
        self,
        model,
        input_ids: torch.LongTensor,
        attention_mask: torch.LongTensor,
        eos_token_id: Optional[int] = None,
        **model_kwargs,
    ) -> Tuple[torch.FloatTensor, torch.FloatTensor]:
        # prepare model inputs
        model_inputs = model.prepare_inputs_for_generation(input_ids, **model_kwargs, eos_token_id=eos_token_id)
        model_inputs["attention_mask"] = attention_mask

        token_scores = []
        
        outputs = model(
            **model_inputs,
            return_dict=True,
            output_attentions=False,
            output_hidden_states=False,
        )

        next_token_logits = outputs.logits[:, -len(input_ids), :]
        next_token_logits = torch.log_softmax(next_token_logits, dim=-1)
        token_scores = next_token_logits.gather(-1, input_ids)

        return token_scores

    def worker(self):
        print("[Loading", self.model_identifier, "with", f"AutoModelForCausalLM.from_pretrained({self.model_identifier}, {str(self.model_args)[1:-1]})]", flush=True)
        model = AutoModelForCausalLM.from_pretrained(self.model_identifier, **self.model_args)

        print("[", self.model_identifier, " ready on device ", model.device, flush=True, sep="", end="]\n")

        while True:
            if self.kill_event.is_set():
                break

            for batch in self.batches():
                eos_token = model.config.eos_token_id

                try:
                    b = GenerateBatch.from_calls(batch)
                    
                    if b.is_score:
                        kwargs = b.generate_args()
                        input_ids = kwargs["input_ids"].to(model.device)
                        attention_mask = kwargs["attention_mask"].to(model.device)
                        
                        scores = self.score(model, input_ids, attention_mask, eos_token_id=eos_token)
                        ScoreStreamer().log_token(b, scores)
                    else:
                        streamer = TokenStreamer(b, model.config.eos_token_id)
                        kwargs = b.generate_args()
                        kwargs["input_ids"] = kwargs["input_ids"].to(model.device)
                        kwargs["attention_mask"] = kwargs["attention_mask"].to(model.device)
                        result = model.generate(**kwargs, stopping_criteria=[streamer], eos_token_id=eos_token, pad_token_id=eos_token)
                        streamer.log_token(result.sequences, result.scores, last=True)
                except Exception as e:
                    print("[Error during generate()]", e, flush=True)
                    for c in batch:
                        c.error("failed to generate tokens '" + str(e) + "'")
                    raise e

    @staticmethod
    def instance(model_identifier, model_args, user, only_existing=False):
        identifier = (model_identifier, pickle.dumps(model_args).hex())

        if identifier not in Scheduler._instances:
            if only_existing:
                raise LMTPCannotLoadModelByPolicy("Model '" + model_identifier + "' is not loaded and server is not configured to load it on demand.")
            Scheduler._instances[identifier] = Scheduler(model_identifier, model_args)

        s = Scheduler._instances[identifier]
        s.last_use = time.time()
        
        if user is not None:
            s.users.add(user)

        Scheduler.gc() # unload any unused models
    
        return s
    
    def unregister(self, user):
        if user in self.users:
            self.users.remove(user)
            self.last_use = time.time()

    def dealloc(self):
        print("[Unloading ", self.model_identifier, "]", flush=True, sep="")
        identifier = (self.model_identifier, pickle.dumps(self.model_args).hex())
        
        Scheduler._instances.pop(identifier)
        
        self.kill_event.set()
        self.worker_thread.join()

    @staticmethod
    def gc(n: int = 2, timeout: int = 10):
        total = len(Scheduler._instances)
        not_needed = [k for k, v in Scheduler._instances.items() if len(v.users) == 0]

        if total >= n:
            for k in not_needed:
                s = Scheduler._instances[k]
                Scheduler._instances[k].dealloc()
        
        # total = len(Scheduler._instances)
        
        # if total >= n:
        #     print("[Warning] {} models loaded, even though the configured limit is {}.".format(total, n), flush=True)
            # print("Active Models:")
            # for k, v in Scheduler._instances.items():
            #     print("  ", k, "used by", v.users)

Scheduler._instances = {}

class TokenSession:
    """
    A LMTP token session, which is a single user generating tokens with a fixed model, 
    using several token streams in parallel and varying sampling configurations.
    """
    def __init__(self, transport, model_args, static=False, longrunning=False):
        self.transport = transport
        self.token_queue = Queue()
        self.queue_processor = asyncio.create_task(self.queue_loop())
        self.used_models = set()
        self.model_args = model_args
        self.static = static

        self.longrunning = longrunning

    async def handle(self, cmd, kwargs):
        stream_id = kwargs.get("stream_id")

        try:
            model = kwargs.pop("model")

            if cmd == "GENERATE":
                prompt = kwargs.pop("prompt")
                stream_id = kwargs.pop("stream_id")
                logit_bias = kwargs.pop("logit_bias", {})
                self.used_models.add(model)

                scheduler = Scheduler.instance(model, self.model_args, user=self, only_existing=self.static)
                scheduler.put(GenerateCall(prompt, logit_bias, kwargs, stream_id, self.token_queue))
            elif cmd == "SCORE":
                prompt = kwargs.pop("prompt")
                scored = kwargs.pop("scored")
                stream_id = kwargs.pop("stream_id")
                self.used_models.add(model)
                
                kwargs["score"] = True
                # full sequence to score
                full_ids = prompt + scored 
                # determines the offset from which on the scoring starts in full_ids
                kwargs["scoring_offset"] = len(prompt)

                scheduler = Scheduler.instance(model, self.model_args, user=self, only_existing=self.static)
                scheduler.put(GenerateCall(full_ids, {}, kwargs, stream_id, self.token_queue))
            else:
                raise Exception("Unknown command: {}".format(cmd))
        except LMTPCannotLoadModelByPolicy as e:
            print("Client requested model that is not loaded and server is not configured to load it on demand.", flush=True)
            self.token_queue.put({
                "stream_id": stream_id,
                "error": "The requested model is not loaded and the server is not configured to load it on demand."
            })
        except Exception as e:
            print("Error in lmtp_server.TokenSession.handle", e, flush=True)
            self.token_queue.put({
                "stream_id": stream_id,
                "error": str(e)
            })        

    async def queue_loop(self):
        try:
            while True:
                try:
                    token = self.token_queue.get_nowait()
                    await self.transport.send("TOKEN", token)
                except QueueEmpty:
                    await asyncio.sleep(0.01)
        except asyncio.CancelledError:
            self.close()
        except Exception as e:
            print("TokenSession.queue_loop error", e, flush=True)
            self.close()

    def close(self):
        self.queue_processor.cancel()
        
        for m in self.used_models:
            try:
                scheduler = Scheduler.instance(m, model_args=self.model_args, user=None, only_existing=self.static)
                scheduler.unregister(self)
                
                if self.longrunning:
                    scheduler.gc()
                else:
                    Scheduler.gc(0)
            except LMTPCannotLoadModelByPolicy:
                pass

class LMTPWebSocketTransport:
    """
    Exposes a LMTP TokenSession over a websocket.
    """
    def __init__(self, ws):
        self.ws = ws
        self.queue = asyncio.Queue()
        self._dumper = asyncio.create_task(self.dumper())

    async def dumper(self):
        while True:
            try:
                batch = [await self.queue.get()]
                # while len(batch) < 1:
                #     try:
                #         batch.append(await asyncio.wait_for(self.queue.get(), timeout=0.1))
                #     except asyncio.TimeoutError:
                #         break
                if len(batch) > 0:
                    await self.ws.send_str("TOKEN" + " " + json.dumps(batch))
            except asyncio.CancelledError:
                break
            except Exception as e:
                print("LMTPWebSocketTransport.dumper error", e, flush=True)

    async def send(self, type, payload):
        await self.queue.put(payload)

    @staticmethod
    async def listen(ws, model_args, static):
        transport = LMTPWebSocketTransport(ws)
        session = TokenSession(transport, model_args, static=static, longrunning=True)

        try:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    cmd, kwargs = msg.data.split(" ", 1)
                    
                    kwargs = json.loads(kwargs)
                    logit_bias = kwargs.pop("logit_bias", {})
                    logit_bias = {int(k): float(v) for k, v in logit_bias.items()}
                    kwargs["logit_bias"] = logit_bias
                    
                    await session.handle(cmd, kwargs)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
        finally:
            transport._dumper.cancel()
            session.close()
            await ws.close()

    async def close(self):
        await self.ws.close()
