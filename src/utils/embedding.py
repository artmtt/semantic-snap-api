import json
from transformers import CLIPProcessor, CLIPModel
import torch
from torch import Tensor
import torch.nn.functional as F

processor = CLIPProcessor.from_pretrained('openai/clip-vit-large-patch14')
model = CLIPModel.from_pretrained('openai/clip-vit-large-patch14')

# def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
#     last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
#     return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

def generate_embeddings(text: str, metadata = {}):
    if metadata:
        combined_text = ' '.join(
            [text] + [v for k, v in metadata.items() if isinstance(v, str)]
        )
    else:
        combined_text = text

    inputs = processor(text=combined_text, return_tensors='pt', padding=True, truncation=True, max_length=77)

    # CLIP Embedding Dims: 768
    with torch.no_grad():
        outputs = model.get_text_features(**inputs)

    # attention_mask = inputs['attention_mask']
    # embeddings = average_pool(outputs.last_hidden_state, attention_mask)

    embeddings = F.normalize(outputs, p=2, dim=1)
    return embeddings.numpy().tolist()[0]
