from transformers import AutoModelForQuestionAnswering
from torch.nn.utils import prune
import torch

class BertPruner:
    def __init__(self, model_name: str, saved_dir: str, sparsity: float):
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_name)
        self.saved_dir = saved_dir
        self.sparsity = sparsity
    def prune_and_save(self):
        for name, module in self.model.named_modules():
            if isinstance(module, torch.nn.Linear):
                # replace l1_unstructured pruning with l2structured for magnitude pruning
                # prune.l1_unstructured(module, name='weight', amount=self.sparsity)
                prune.ln_structured(module, name='weight', amount=self.sparsity, n=2, dim=0)

        # it fixed using previous code (2 potential changes: eval model/input_id)
        input_shape = (1, 512)
        input_ids = torch.zeros(input_shape, dtype=torch.long, device=self.model.device)
        attention_mask = torch.ones(input_shape, dtype=torch.long, device=self.model.device)
        token_type_ids = torch.zeros(input_shape, dtype=torch.long, device=self.model.device)

        torch.onnx.export(self.model, (input_ids, attention_mask, token_type_ids),
                          self.saved_dir,
                          opset_version=11,
                          input_names=['input_ids', 'input_mask', 'segment_ids'],
                          output_names=['output'],
                          dynamic_axes={'input_ids': {0: 'batch_size', 1: 'sequence_length'},
                                        'input_mask': {0: 'batch_size', 1: 'sequence_length'},
                                        'segment_ids': {0: 'batch_size', 1: 'sequence_length'},
                                        'output': {0: 'batch_size', 1: 'sequence_length'}})