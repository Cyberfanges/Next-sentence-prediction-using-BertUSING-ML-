import runway
import torch
from transformers import BertTokenizer
from transformers import BertForNextSentencePrediction
from runway.data_types import array, text, number, boolean


# Setup block copy-pasted from Cris's tutorial
@runway.setup(options={"checkpoint": runway.category(
   description="Pretrained checkpoints to use.",
	choices=['celebAHQ-512', 'celebAHQ-256', 'celeba'],
	default='celebAHQ-512'
)})
def setup(opts):
	model = BertForNextSentencePrediction.from_pretrained('bert-base-uncased')
	tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
	return model, tokenizer


@runway.command(name='sequence_score',
	inputs={ 'line1': text(), 'next_line_candidates': text()},
	outputs={ 'scores': array(item_type=number)}
)
def sequence_score(setup_tuple, inputs):
	model, tokenizer = setup_tuple
	line1 = inputs['line1']
	outpath = line1[:5] + '.txt'
	outfile = open(outpath, 'w')
	next_line_candidates = inputs['next_line_candidates']
	candidates = [line.strip() for line in next_line_candidates.split('\n')]
	loss_scores = []
	for candidate in candidates:
		combined = inputs['line1'] + ' ' + candidate      # may be better to concatenate *after* tokenization using special [SEP] token
		input_tokens = tokenizer.encode(combined, add_special_tokens=True)
		input_ids = torch.tensor(input_tokens).unsqueeze(0)
		outputs = model(input_ids)
		sequence_loss = outputs[0][0][0]     # outputs is an array with losses as the first value and logits as the second (I *think*)
		sequence_loss = float(sequence_loss.cpu().detach().numpy())
		loss_scores.append(sequence_loss)
		outfile.write(str(candidate) + '\t' + str(sequence_loss) + '\n')
		print(candidate, sequence_loss)
	return loss_scores