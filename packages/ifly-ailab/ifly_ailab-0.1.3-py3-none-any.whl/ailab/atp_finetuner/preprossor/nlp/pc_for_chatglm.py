import json
from tqdm import tqdm
import transformers
import datasets
from transformers import models
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.build import PreProcessorRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.atp_finetuner.preprossor import AILabPreprocessor

@PreProcessorRg.register((Task.question_answering, Model.chatglm_6b))
class ChatGlmPreProcessor(AILabPreprocessor):
    def __init__(self, dataset, preprocessor):
        super().__init__(dataset, preprocessor)

    @classmethod
    def build_preprocessor(cls, model_name:str, dataset: AILabDataset,**kwargs):
        preprocessor = models.auto.AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        return cls(dataset, preprocessor)

    def process_data(self) ->AILabDataset:
        return self._dataset
    
    def preprocess(tokenizer, config, example, max_seq_length):
        prompt = example["context"]
        target = example["target"]
        prompt_ids = tokenizer.encode(prompt, max_length=max_seq_length, truncation=True)
        target_ids = tokenizer.encode(
            target,
            max_length=max_seq_length,
            truncation=True,
            add_special_tokens=False)
        input_ids = prompt_ids + target_ids + [config.eos_token_id]
        return {"input_ids": input_ids, "seq_len": len(prompt_ids)}


    def read_jsonl(path, max_seq_length, skip_overlength=False):
        model_name = "THUDM/chatglm-6b"
        tokenizer = transformers.AutoTokenizer.from_pretrained(
            model_name, trust_remote_code=True)
        config = transformers.AutoConfig.from_pretrained(
            model_name, trust_remote_code=True, device_map='auto')
        with open(path, "r") as f:
            for line in tqdm(f.readlines()):
                example = json.loads(line)
                feature = preprocess(tokenizer, config, example, max_seq_length)
                if skip_overlength and len(feature["input_ids"]) > max_seq_length:
                    continue
                feature["input_ids"] = feature["input_ids"][:max_seq_length]
                yield feature


    def tokenize_dataset_rows():
        jsonl_path =  "chatglm/alpaca_data.jsonl"
        save_path = "chatglm/alpaca"
        max_seq_length = 384
        skip_overlength = False
        dataset = datasets.Dataset.from_generator(
            lambda: read_jsonl(jsonl_path, max_seq_length, skip_overlength)
        )
        dataset.save_to_disk(save_path)