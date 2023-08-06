import torch
import numpy as np
from torch.utils.data import DataLoader
from deepod.core.base_transformer_network import TokenEmbedding, LearnablePositionalEncoding, FixedPositionalEncoding, TransformerEncoderLayer, TransformerBatchNormEncoderLayer
from deepod.core.network_utility import _handle_n_hidden, _instantiate_class
from deepod.core.base_model import BaseDeepAD


class RoSAS(BaseDeepAD):
    def __init__(self, data_type='ts', epochs=100, batch_size=128, lr=0.005,
                 network='Transformer', seq_len=100, stride=1,
                 rep_dim=32, hidden_dims='32', act='LeakyReLU', bias=False,
                 n_heads=8, d_model=512, pos_encoding='fixed', norm='LayerNorm',
                 margin=5., alpha=0.5, T=2, k=2,
                 epoch_steps=-1, prt_steps=10, device='cuda',
                 verbose=2, random_state=42):
        super(BaseDeepAD, self).__init__(
            data_type=data_type, model_name='RoSAS', epochs=epochs, batch_size=batch_size, lr=lr,
            network=network, seq_len=seq_len, stride=stride,
            epoch_steps=epoch_steps, prt_steps=prt_steps, device=device,
            verbose=verbose, random_state=random_state
        )

        # network parameters
        self.hidden_dims = hidden_dims
        self.rep_dim = rep_dim
        self.act = act
        self.bias = bias

        # parameters for Transformer
        self.n_heads = n_heads
        self.d_model = d_model
        self.pos_encoding = pos_encoding
        self.norm = norm

        self.k = k
        self.margin = margin
        self.alpha = alpha
        self.T = T
        return

    def training_prepare(self, X, y):
        train_loader = RoSASLoader(X, y, batch_size=self.batch_size)

        network_params = {
            'n_features': self.n_features,
            'n_hidden': self.hidden_dims,
            'n_output': self.rep_dim,
            'activation': self.act,
            'bias': self.bias
        }
        if self.network == 'Transformer':
            network_params['n_heads'] = self.n_heads
            network_params['d_model'] = self.d_model
            network_params['pos_encoding'] = self.pos_encoding
            network_params['norm'] = self.norm
            network_params['seq_len'] = self.seq_len
        # if self.network == 'TCN':
        #     net = TcnEncoder(**network_params).to(self.device)
        if self.network == 'Transformer':
            net = TSTransformerEncoder(**network_params).to(self.device)
        else:
            raise NotImplementedError('')

        criterion = Loss(
            margin=self.margin, alpha=self.alpha,
            T=self.T, k=self.k,
            reduction='mean'
        )

        return train_loader, net, criterion

    def training_forward(self, batch_x, net, criterion):
        anchor, pos, neg = batch_x[:, 0], batch_x[:, 1], batch_x[:, 2]

        anchor = torch.from_numpy(anchor).float().to(self.device)
        pos = torch.from_numpy(pos).float().to(self.device)
        neg = torch.from_numpy(neg).float().to(self.device)

        anchor_emb, anchor_s = net(anchor)
        pos_emb, pos_s = net(pos)
        neg_emb, neg_s = net(neg)
        embs = [anchor_emb, pos_emb, neg_emb]

        x_i = torch.cat((anchor, pos, neg), 0)
        target_i = torch.cat((torch.ones_like(anchor_s)*-1,
                              torch.ones_like(pos_s)*-1,
                              torch.ones_like(neg_s)*1), 0)

        indices_j = torch.randperm(x_i.size(0)).to(self.device)
        x_j = x_i[indices_j]
        target_j = target_i[indices_j]

        Beta = torch.distributions.dirichlet.Dirichlet(torch.tensor([self.alpha, self.alpha]))
        lambdas = Beta.sample(target_i.flatten().shape).to(self.device)[:, 1]

        x_tilde = x_i * lambdas.view(lambdas.size(0), 1, 1) + x_j * (1 - lambdas.view(lambdas.size(0), 1, 1))
        _, score_tilde = net(x_tilde)
        _, score_xi = net(x_i)
        _, score_xj = net(x_j)

        score_mix = score_xi * lambdas.view(lambdas.size(0), 1) + score_xj * (1 - lambdas.view(lambdas.size(0), 1))
        y_tilde = target_i * lambdas.view(lambdas.size(0), 1) + target_j * (1 - lambdas.view(lambdas.size(0), 1))

        loss, loss1, loss2, loss_out, loss_consistency = self.criterion(
            embs, score_tilde, score_mix, y_tilde
        )
        return loss

    def inference_prepare(self, X):
        test_loader = DataLoader(X, batch_size=self.batch_size, drop_last=False, shuffle=False)
        return test_loader

    def inference_forward(self, batch_x, net, criterion):
        batch_x = batch_x.float().to(self.device)
        batch_z, batch_score = net(batch_x)
        return batch_z, batch_score



class RoSASLoader:
    def __init__(self, x, y, batch_size=256, steps_per_epoch=None):
        self.x = x
        self.y = y

        self.anom_idx = np.where(y==1)[0]
        self.norm_idx = np.where(y==0)[0]
        self.unlabeled_idx = np.where(y==0)[0]

        self.batch_size = batch_size

        self.counter = 0

        self.steps_per_epoch = steps_per_epoch if steps_per_epoch is not None \
            else int(len(x) / self.batch_size)

        return

    def __iter__(self):
        self.counter = 0
        return self

    def __next__(self):
        self.counter += 1

        batch_x = self.batch_generation()
        batch_x = torch.from_numpy(batch_x)

        if self.counter > self.steps_per_epoch:
            raise StopIteration
        return batch_x

    def batch_generation(self):
        this_anchor_idx = np.random.choice(self.norm_idx, self.batch_size, replace=False)
        this_pos_idx = np.random.choice(self.unlabeled_idx, self.batch_size, replace=False)
        this_anom_idx = np.random.choice(self.anom_idx, self.batch_size)

        batch_x = np.array([[self.x[a], self.x[p], self.x[n]]
                            for a, p, n in zip(this_anchor_idx, this_pos_idx, this_anom_idx)])
        # batch_y = np.array([[self.y[a], self.y[p], self.y[n]]
        #                     for a, p, n in zip(this_anchor_idx, this_pos_idx, this_anom_idx)])

        return batch_x


class Loss(torch.nn.Module):
    def __init__(self, l2_reg_weight=0., margin=1., alpha=1., T=2, k=2, reduction='mean'):
        super(Loss, self).__init__()
        self.loss_tri = torch.nn.TripletMarginLoss(margin=margin, reduction=reduction)
        self.loss_reg = torch.nn.SmoothL1Loss(reduction=reduction)

        self.T = T
        self.alpha = alpha
        self.k = k
        self.reduction = reduction
        return

    def forward(self, embs, score_tilde, score_mix, y_tilde, pre_emb_loss=None, pre_score_loss=None):
        anchor_emb, pos_emb, neg_emb = embs
        loss_emb = self.loss_tri(anchor_emb, pos_emb, neg_emb)
        # loss_emb_mean = torch.mean(loss_emb)

        loss_out = self.loss_reg(score_tilde, y_tilde)
        loss_consistency = self.loss_reg(score_tilde, score_mix)
        loss_score = loss_out + loss_consistency

        if self.reduction == 'mean' and pre_emb_loss is not None:
            # # adaptive weighting
            k1 = torch.exp((loss_emb / pre_emb_loss) / self.T) if pre_emb_loss != 0 else 0
            k2 = torch.exp((loss_score / pre_score_loss) / self.T) if pre_score_loss != 0 else 0
            loss = (k1 / (k1 + k2)) * loss_emb + (k2 / (k1 + k2)) * loss_score
        else:
            loss = 0.5 * loss_emb + 0.5 * loss_score

        # loss = (k1 / (k1 + k2)) * loss_emb + (k2 / (k1 + k2)) * loss_score + self.l2_reg_weight * l2_reg
        # print(basenet.l2.weight.shape)

        return loss, loss_emb, loss_score, loss_out, loss_consistency


class TSTransformerEncoder(torch.nn.Module):
    """
    Simplest classifier/regressor. Can be either regressor or classifier because the output does not include
    softmax. Concatenates final layer embeddings and uses 0s to ignore padding embeddings in final output layer.
    """

    def __init__(self, n_features, n_output=128, seq_len=100, d_model=512,
                 n_heads=8, n_hidden='512', dropout=0.1,
                 token_encoding='convolutional', pos_encoding='fixed', activation='GELU', bias=False,
                 norm='LayerNorm', freeze=False):
        super(TSTransformerEncoder, self).__init__()

        self.max_len = seq_len
        self.d_model = d_model
        n_hidden, n_layers = _handle_n_hidden(n_hidden)

        # parameter check
        assert  token_encoding in ['linear', 'convolutional'], \
            f"use 'linear' or 'convolutional', {token_encoding} is not supported in token_encoding"
        assert  pos_encoding in ['learnable', 'fixed'],\
            f"use 'learnable' or 'fixed', {pos_encoding} is not supported in pos_encoding"
        assert  norm in ['LayerNorm', 'BatchNorm'],\
            f"use 'learnable' or 'fixed', {norm} is not supported in norm"

        if token_encoding == 'linear':
            self.project_inp = torch.nn.Linear(n_features, d_model, bias=bias)
        elif token_encoding == 'convolutional':
            self.project_inp = TokenEmbedding(n_features, d_model, kernel_size=3, bias=bias)

        if pos_encoding == "learnable":
            self.pos_enc = LearnablePositionalEncoding(d_model, dropout=dropout*(1.0 - freeze), max_len=seq_len)
        elif pos_encoding == "fixed":
            self.pos_enc =  FixedPositionalEncoding(d_model, dropout=dropout*(1.0 - freeze), max_len=seq_len)

        if norm == 'LayerNorm':
            # d_model -> n_hidden -> d_model
            encoder_layer = TransformerEncoderLayer(d_model, n_heads,
                                                    n_hidden, dropout*(1.0 - freeze),
                                                    activation=activation)
        elif norm == 'BatchNorm':
            encoder_layer = TransformerBatchNormEncoderLayer(d_model, n_heads,
                                                             n_hidden, dropout*(1.0 - freeze),
                                                             activation=activation)

        self.transformer_encoder = torch.nn.TransformerEncoder(encoder_layer, num_layers=n_layers)

        assert activation in ['ReLU', 'GELU'], \
            f"activation should be ReLU/GELU, not {activation}"
        self.act = _instantiate_class("torch.nn.modules.activation", activation)

        self.dropout = torch.nn.Dropout(dropout)
        self.dropout1 = torch.nn.Dropout(dropout)
        # self.output_layer = torch.nn.Linear(d_model * seq_len, n_output, bias=bias)
        self.output_layer = torch.nn.Linear(d_model, n_output, bias=bias)
        self.output_layer21 = torch.nn.Linear(n_output, int(n_output/2), bias=bias)
        self.output_layer22 = torch.nn.Linear(int(n_output/2), 1, bias=bias)
        self.act2 = torch.nn.Tanh()

    def forward(self, X, padding_masks=None):
        """
        Args:
            X: (batch_size, seq_length, feat_dim) torch tensor of masked features (input)
            padding_masks: (batch_size, seq_length) boolean tensor, 1 means keep vector at this position, 0 means padding
        Returns:
            output: (batch_size, num_classes)
        """

        # permute because pytorch convention for transformers is [seq_length, batch_size, feat_dim]. padding_masks [batch_size, feat_dim]

        # inp = X.permute(1, 0, 2)
        # inp = self.project_inp(inp) * math.sqrt(self.d_model)  # [seq_length, batch_size, d_model] project input vectors to d_model dimensional space
        # inp = self.pos_enc(inp)  # add positional encoding

        # data embedding
        inp = self.project_inp(X) + self.pos_enc(X)
        # inp = self.dropout(inp)
        inp = inp.permute(1, 0, 2)

        # NOTE: logic for padding masks is reversed to comply with definition in MultiHeadAttention, TransformerEncoderLayer
        output = self.transformer_encoder(inp, src_key_padding_mask=~padding_masks if padding_masks is not None else None)  # (seq_length, batch_size, d_model)
        output = self.act(output)  # the output transformer encoder/decoder embeddings don't include non-linearity
        output = output.permute(1, 0, 2)  # (batch_size, seq_length, d_model)
        output = self.dropout1(output)

        if padding_masks is None:
            padding_masks = torch.ones(X.shape[0], X.shape[1], dtype=torch.uint8).to(X.device)

        # Output
        output = output * padding_masks.unsqueeze(-1)  # (batch_size, seq_len, 1) zero-out padding embeddings
        output = output[:, -1] # (batch_size, d_model)
        # output = output.reshape(output.shape[0], -1)  # (batch_size, seq_length * d_model)
        representation = self.output_layer(output)  # (batch_size, n_output)

        score = self.output_layer21(representation)
        score = self.act(score)
        score = self.output_layer22(score)
        score = self.act2(score)

        return representation, score




if __name__ == '__main__':
    data = np.random.randn(1000, 10)
    model = RoSAS()
    model.fit(data)