import abc
from typing import *

import torch
from torch import nn
from transformers import AutoModel, DistilBertConfig, DistilBertModel

from .context import ContextHead, ContextTransformerAndWide
from .moe import MOELayer, Top2Gate, ExpertLayer, MoEFFLayer, MoEFFLayerTopK
from .transformer import (ParallelTransformerAEP, ParallelTransformerBlock, TransformerAEP, ParallelTransformerAEP2S,
                          TransformerHistory)
from .utils import MeanMaxPooling, LayerNorm, AutomaticWeightedLoss

    
class GRec(nn.Module):
    def __init__(self, deep_dims, page_dim, seq_dim, item_meta_dim, page_embed_dim, seq_embed_dim, item_embed_dim, item_meta_embed_dim, item_pre_embed_dim, deep_embed_dims, wad_embed_dim, nlp_embed_dim, seq_hidden_size, nlp_encoder_path, task_type_dims, task_type_embed_dim, task_out_dims, num_task,
                 num_wide=0, num_meta_wide=0, num_shared=0, nlp_dim=0, item_freeze=None, item_pre_freeze=None, nlp_freeze=None, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 page_embedding_weight=None, item_embedding_weight=None, item_meta_embedding_weight=None, item_pre_embedding_weight=None, shared_embeddings_weight=None, moe_kwargs=None):
        super().__init__()
        #self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        context_head_kwargs = context_head_kwargs if context_head_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        
        if page_embedding_weight is None:
            print("not use pretrained embedding")
            self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        else:
            print("use pretrained item embedding")
            self.page_embedding = nn.Embedding.from_pretrained(page_embedding_weight, freeze=False)
        if item_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_embedding = nn.Embedding(seq_dim, item_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_embedding = nn.Embedding.from_pretrained(item_embedding_weight, freeze=False)
        if item_meta_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_meta_embedding = nn.Embedding(item_meta_dim, item_meta_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_meta_embedding = nn.Embedding.from_pretrained(item_meta_embedding_weight, freeze=False)
        if item_pre_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_pre_embedding = nn.Embedding(seq_dim, item_pre_embed_dim)
        else:
            print("use pretrained item pre embedding")
            self.item_pre_embedding = nn.Embedding.from_pretrained(item_pre_embedding_weight, freeze=False)
            
        if item_freeze:
            self.item_embedding.weight.requires_grad = False
        if item_pre_freeze:
            self.item_pre_embedding.weight.requires_grad = False
            
        if nlp_freeze:
            for param in self.nlp_encoder.parameters():
                param.requires_grad = False
         
#         self.combined_dim = nlp_embed_dim + wad_embed_dim + seq_embed_dim + seq_embed_dim
        self.combined_dim = nlp_embed_dim + wad_embed_dim + seq_embed_dim + seq_embed_dim + seq_embed_dim
#         self.mm_pooling = MeanMaxPooling()
        self.task_embedding = nn.ModuleList([
            nn.Embedding(task_type_dim, task_type_embed_dim)
            for task_type_dim in task_type_dims
        ])
#         print(task_type_dims)
#         print(self.task_embedding)
#         self.task_embedding = nn.Embedding(task_type_dims, seq_embed_dim)
        self.context_head = ContextHead(
            deep_dims=deep_dims,
            num_wide=num_wide,
            item_embedding=self.item_embedding,
            shared_embeddings_weight=shared_embeddings_weight,
            wad_embed_dim=wad_embed_dim,
            deep_embed_dims=deep_embed_dims
        )
        self.sequence_transformer = ParallelTransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            item_meta_embedding=self.item_meta_embedding,
            item_pre_embedding=self.item_pre_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            moe_kwargs=moe_kwargs,
            **sequence_transformer_kwargs
        )
        self.att_pooling = ParallelTransformerBlock(
            dim=256, dim_head=256, heads=1
        )
        self.seq_dense = torch.nn.Linear(
            in_features=seq_embed_dim,
            out_features=seq_embed_dim
        )
        self.nlp_dense = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=nlp_embed_dim
        ) 
        self.moe = MoEFFLayer(dim=seq_embed_dim, num_experts=moe_kwargs.get("num_experts"), expert_capacity=moe_kwargs.get("expert_capacity"), router_jitter_noise=moe_kwargs.get("router_jitter_noise"), hidden_size=seq_embed_dim, expert_class=ExpertLayer)
#         self.moe = MoEFFLayerTopK(dim=seq_embed_dim, num_experts=moe_kwargs.get("num_experts"), expert_capacity=moe_kwargs.get("expert_capacity"), num_K=moe_kwargs.get("num_K"), router_jitter_noise=moe_kwargs.get("router_jitter_noise"), hidden_size=seq_embed_dim, expert_class=ExpertLayer)
        
#         self.moe = MoEFFLayer(dim=self.combined_dim, num_experts=moe_kwargs.get("num_experts"), expert_capacity=moe_kwargs.get("expert_capacity"), hidden_size=self.combined_dim, expert_class=ExpertLayer)
#         self.tasks_dense1 = nn.ModuleDict()
#         self.tasks_dense2 = nn.ModuleDict()
#         self.tasks_act1 = self.tasks_act2 = nn.ModuleDict()
#         for i in range(task_type_dim):
#             self.tasks_dense1[f"task{i}_dense1"] = nn.Linear(
#                 self.combined_dim, 
#                 self.combined_dim // 2
#             )
#             self.tasks_dense2[f"task{i}_dense2"] = nn.Linear(
#                 self.combined_dim // 2, 
#                 task_out_dims[i]
#             )
#             self.tasks_act1[f"task{i}_act1"] = self.tasks_act2[f"task{i}_act2"] = nn.LeakyReLU(0.2)

        self.tasks_dense1 = nn.Linear(
            self.combined_dim, 
            self.combined_dim // 2
        )
        self.tasks_dense2 = nn.Linear(
            self.combined_dim // 2, 
            task_out_dims[0]
        )
        self.tasks_act1 = self.tasks_act2 = nn.LeakyReLU(0.2)
        self.seq_dim = seq_dim
        self.task_type_dim = num_task
#         self.awl = AutomaticWeightedLoss(task_type_dim)

#     def split_task(self, task_type_dim, task_in, combined_out):
#         task_indices = []
#         task_outs = []
#         task_user_outs = []
#         for i in range(task_type_dim):
#             task_indice = task_in == i
#             task_indice = torch.nonzero(task_indice).flatten()
#             task_input = combined_out[task_indice]
#             task_out = self.tasks_dense1[f"task{i}_dense1"](task_input)
#             task_user_out = self.tasks_act1[f"task{i}_act1"](task_out)
#             task_out = self.tasks_dense2[f"task{i}_dense2"](task_user_out)
#             task_indices.append(task_indice)
#             task_user_outs.append(task_user_out)
#             task_outs.append(task_out)
#         return task_indices, task_outs, task_user_outs
    
    def split_task(self, task_type_dim, task_in, combined_out):
        task_indices = []
        task_outs = []
        task_user_outs = []
        for i in range(task_type_dim):
            task_indice = task_in == i
            task_indice = torch.nonzero(task_indice).flatten()
            task_input = combined_out[task_indice]
            task_out = self.tasks_dense1(task_input)
            task_user_out = self.tasks_act1(task_out)
            task_out = self.tasks_dense2(task_user_out)
            task_indices.append(task_indice)
            task_user_outs.append(task_user_out)
            task_outs.append(task_out)
        return task_indices, task_outs, task_user_outs
        
    def forward(self, deep_in, page_in, item_in, vl_in, tasks_in, current_in, current_meta_in, item_meta_in=None, page_meta_in=None, item_meta_wide_in=None, page_meta_wide_in=None, wide_in=None, input_ids=None, attention_mask=None, shared_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask).pooler_output.to(dtype=torch.float32)
#         search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state[:,0,:].to(dtype=torch.float32)
        search_out = self.nlp_dense(search_out)
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, item_meta_in=item_meta_in, page_meta_in=page_meta_in, item_meta_wide_in=item_meta_wide_in, page_meta_wide_in=page_meta_wide_in, vl_in=vl_in)
        seq_out = self.seq_dense(seq_out)
        current_item_out = self.item_embedding(current_in)
        current_meta_out = self.item_meta_embedding(current_meta_in)
        current_pre_out = self.item_pre_embedding(current_in)
        current_out = torch.cat((current_item_out, current_meta_out, current_pre_out), 1)

#         tasks_out_list = [self.task_embedding[i](task_in).unsqueeze(1)
#                            for i, task_in in enumerate(tasks_in)]
#         task_out = torch.cat(tasks_out_list, dim=2)
#         outs = torch.cat((seq_out[:, None, :], ctx_out[:, None, :], search_out[:, None, :], current_out[:, None, :]), dim=1)
#         outs = self.att_pooling(outs)
#         outs, aux_loss = self.moe(outs, task_out)
        
        
        tasks_out_list = [self.task_embedding[i](task_in).unsqueeze(1)
                           for i, task_in in enumerate(tasks_in)]
        task_out = torch.cat(tasks_out_list, dim=2).squeeze(1)
#         task_out = self.mm_pooling(tasks_out)
        outs = torch.cat((seq_out[:, None, :], ctx_out[:, None, :], search_out[:, None, :], current_out[:, None, :], task_out[:, None, :]), dim=1)
        outs = self.att_pooling(outs)
        outs, aux_loss = self.moe(outs)
        
        outs = outs.reshape(-1, self.combined_dim)
        task_indices, task_outs, task_user_outs = self.split_task(self.task_type_dim, tasks_in[0], outs)
        return (tuple(task_indices), tuple(task_outs), aux_loss)


class PaRSAudienceTT(nn.Module):
    def __init__(self, user_deep_dims, user_deep_embed_dims, user_num_wide, user_wad_embed_dim,
                 offer_deep_dims, offer_deep_embed_dims, offer_num_wide, offer_wad_embed_dim,
                 svc_dim, svc_embed_dim, new_svc_dim, new_svc_embed_dim, page_dim, item_dim,
                 seq_embed_dim, nlp_encoder_path, nlp_dim, sequence_transformer_kwargs,
                 user_moe_kwargs, offer_moe_kwargs, task_type_dim):
        super().__init__()
        self.task_type_dim = task_type_dim
        self.seq_embed_dim = seq_embed_dim

        # user layers
        self.svc_embedding = nn.Embedding(svc_dim, svc_embed_dim)
        self.new_svc_embedding = nn.Embedding(new_svc_dim, new_svc_embed_dim)
        self.mm_pooling = MeanMaxPooling()

        self.page_embedding = nn.Embedding(page_dim, seq_embed_dim)
        self.item_embedding = nn.Embedding(item_dim, seq_embed_dim)
        self.sequence_transformer = ParallelTransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            heads=sequence_transformer_kwargs.get("seq_num_heads"),
            num_layers=sequence_transformer_kwargs.get("seq_num_layers"),
        )

        self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        self.search_nlp_dense_0 = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=seq_embed_dim * 2
        )
        self.search_nlp_dense_1 = torch.nn.Linear(
            in_features=seq_embed_dim * 2,
            out_features=seq_embed_dim
        )
        self.nlp_act = nn.LeakyReLU(0.2)

        self.user_context_head = ContextTransformerAndWide(
            deep_dims=user_deep_dims,
            num_wide=user_num_wide,
            deep_embed_dims=user_deep_embed_dims,
            wad_embed_dim=user_wad_embed_dim,
        )
        self.user_att_pooling = ParallelTransformerBlock(
            dim=seq_embed_dim, dim_head=seq_embed_dim, heads=1
        )
        self.user_task_type_embedding = nn.Embedding(task_type_dim, seq_embed_dim)
        # nlp_out + aep_seq_out + svc_out + new_svc_out + user_ctx_out
        self.user_concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim \
                               + seq_embed_dim + seq_embed_dim + seq_embed_dim
        self.user_moe = MoEFFLayer(
            dim=seq_embed_dim,
            num_experts=user_moe_kwargs.get("num_experts"),
            expert_capacity=user_moe_kwargs.get("expert_capacity"),
            hidden_size=seq_embed_dim,
            expert_class=ExpertLayer,
            # num_K=user_moe_kwargs.get("num_K"),
        )

        self.user_dense_0 = nn.ModuleDict()
        self.user_dense_1 = nn.ModuleDict()
        self.user_act = nn.LeakyReLU(0.2)
        self.user_dropout = nn.Dropout(p=0.1)
        for i in range(task_type_dim):
            self.user_dense_0[f"task{i}_dense1"] = nn.Linear(
                in_features=self.user_concat_dim,
                out_features=seq_embed_dim * 3
            )
            self.user_dense_1[f"task{i}_dense2"] = nn.Linear(
                in_features=seq_embed_dim * 3,
                out_features=seq_embed_dim
            )

        # offer layers
        self.offer_context_head = ContextTransformerAndWide(
            deep_dims=offer_deep_dims,
            num_wide=offer_num_wide,
            deep_embed_dims=offer_deep_embed_dims,
            wad_embed_dim=offer_wad_embed_dim,
        )
        self.offer_task_type_embedding = nn.Embedding(task_type_dim, seq_embed_dim)
        self.offer_att_pooling = ParallelTransformerBlock(
            dim=seq_embed_dim, dim_head=seq_embed_dim, heads=1
        )
        # offer_context_out
        self.offer_concat_dim = seq_embed_dim + seq_embed_dim
        self.offer_moe = MoEFFLayer(
            dim=seq_embed_dim,
            num_experts=offer_moe_kwargs.get("num_experts"),
            expert_capacity=offer_moe_kwargs.get("expert_capacity"),
            hidden_size=seq_embed_dim,
            expert_class=ExpertLayer,
            # num_K=offer_moe_kwargs.get("num_K"),
        )

        self.offer_dense_0 = nn.ModuleDict()
        self.offer_dense_1 = nn.ModuleDict()
        self.offer_act = nn.LeakyReLU(0.2)
        self.offer_dropout = nn.Dropout(p=0.1)
        for i in range(task_type_dim):
            self.offer_dense_0[f"task{i}_dense1"] = nn.Linear(
                in_features=self.offer_concat_dim,
                out_features=self.offer_concat_dim + self.offer_concat_dim // 2
            )
            self.offer_dense_1[f"task{i}_dense2"] = nn.Linear(
                in_features=self.offer_concat_dim + self.offer_concat_dim // 2,
                out_features=seq_embed_dim
            )

        self.out_act = nn.Sigmoid()

    def user_split_task(self, task_in, combined_out):
        task_indices = []
        task_outs = []
        for i in range(self.task_type_dim):
            task_indice = task_in == i
            task_indice = torch.nonzero(task_indice).flatten()
            task_indices.append(task_indice)
            task_input = combined_out[task_indice]
            task_out = self.user_dense_0[f"task{i}_dense1"](task_input)
            task_out = self.user_act(task_out)
            task_out = self.user_dropout(task_out)
            task_out = self.user_dense_1[f"task{i}_dense2"](task_out)
            task_out = self.user_act(task_out)
            task_outs.append(task_out)
        return task_indices, task_outs

    def offer_split_task(self, task_in, combined_out):
        task_indices = []
        task_outs = []
        for i in range(self.task_type_dim):
            task_indice = task_in == i
            task_indice = torch.nonzero(task_indice).flatten()
            task_indices.append(task_indice)
            task_input = combined_out[task_indice]
            task_out = self.offer_dense_0[f"task{i}_dense1"](task_input)
            task_out = self.offer_act(task_out)
            task_out = self.offer_dropout(task_out)
            task_out = self.offer_dense_1[f"task{i}_dense2"](task_out)
            task_out = self.offer_act(task_out)
            task_outs.append(task_out)
        return task_indices, task_outs

    def forward(self, user_deep_in, offer_deep_in, svc_in, new_svc_in, page_in, item_in, vl_in,
                user_wide_in, offer_wide_in, search_in, task_type_in):
        device = vl_in.device

        svc_out = self.svc_embedding(svc_in.long())
        svc_out = self.mm_pooling(svc_out)
        new_svc_out = self.new_svc_embedding(new_svc_in.long())
        new_svc_out = self.mm_pooling(new_svc_out)

        aep_seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

        search_out = self.nlp_encoder(**search_in).last_hidden_state[:, 0, :].to(dtype=torch.float32)
        search_out = self.search_nlp_dense_0(search_out)
        search_out = self.nlp_act(search_out)
        search_out = self.search_nlp_dense_1(search_out)
        search_out = self.nlp_act(search_out)

        user_ctx_out = self.user_context_head(deep_in=user_deep_in, wide_in=user_wide_in)
        user_task_out = self.user_task_type_embedding(task_type_in.long())
        user_out = torch.stack([user_task_out, search_out, aep_seq_out, svc_out, new_svc_out, user_ctx_out], dim=1)
        user_out = self.user_att_pooling(user_out)
#         user_task_out_routing = user_task_out[:, None, :]
#         user_task_out_routing = torch.cat([user_task_out_routing] * user_out.shape[1], dim=1)
        user_out, user_aux_loss = self.user_moe(user_out)
        user_out = user_out.reshape(-1, self.user_concat_dim)
        user_task_indices, user_outs = self.user_split_task(task_type_in, user_out)
        user_out_res = torch.zeros(user_out.shape[0], self.seq_embed_dim).to(device)
        for i in range(self.task_type_dim):
            user_out_res[user_task_indices[i]] = user_outs[i]

        offer_ctx_out = self.offer_context_head(deep_in=offer_deep_in, wide_in=offer_wide_in)
        offer_task_out = self.offer_task_type_embedding(task_type_in.long())
        offer_out = torch.stack([offer_task_out, offer_ctx_out], dim=1)
        offer_out = self.offer_att_pooling(offer_out)
#         offer_task_out_routing = offer_task_out[:, None, :]
#         offer_task_out_routing = torch.cat([offer_task_out_routing] * offer_out.shape[1], dim=1)
        offer_out, offer_aux_loss = self.offer_moe(offer_out)
        offer_out = offer_out.reshape(-1, self.offer_concat_dim)
        offer_task_indices, offer_outs = self.offer_split_task(task_type_in, offer_out)
        offer_out_res = torch.zeros(offer_out.shape[0], self.seq_embed_dim).to(device)
        for i in range(self.task_type_dim):
            offer_out_res[offer_task_indices[i]] = offer_outs[i]

        out = torch.mul(user_out_res, offer_out_res)
        out = torch.sum(out, dim=1)
        out = self.out_act(out)

        return out, user_out_res, offer_out_res, (user_aux_loss, offer_aux_loss)


class PaRSAudienceLoyaltyTT(nn.Module):
    def __init__(self, user_deep_dims, user_deep_embed_dims, user_num_wide, user_wad_embed_dim,
                 offer_deep_dims, offer_deep_embed_dims, offer_num_wide, offer_wad_embed_dim,
                 svc_dim, svc_embed_dim, new_svc_dim, new_svc_embed_dim, page_dim, item_dim,
                 seq_embed_dim, nlp_encoder_path, nlp_dim, sequence_transformer_kwargs,
                 user_moe_kwargs, offer_moe_kwargs):
        super().__init__()
        self.seq_embed_dim = seq_embed_dim

        # user layers
        self.svc_embedding = nn.Embedding(svc_dim, svc_embed_dim)
        self.new_svc_embedding = nn.Embedding(new_svc_dim, new_svc_embed_dim)
        self.mm_pooling = MeanMaxPooling()

        self.page_embedding = nn.Embedding(page_dim, seq_embed_dim)
        self.item_embedding = nn.Embedding(item_dim, seq_embed_dim)
        self.sequence_transformer = ParallelTransformerAEP2S(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            heads=sequence_transformer_kwargs.get("seq_num_heads"),
            num_layers=sequence_transformer_kwargs.get("seq_num_layers"),
        )

        #self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        self.search_nlp_dense_0 = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=seq_embed_dim * 2
        )
        self.search_nlp_dense_1 = torch.nn.Linear(
            in_features=seq_embed_dim * 2,
            out_features=seq_embed_dim
        )
        self.nlp_act = nn.LeakyReLU(0.2)

        self.user_context_head = ContextTransformerAndWide(
            deep_dims=user_deep_dims,
            num_wide=user_num_wide,
            deep_embed_dims=user_deep_embed_dims,
            wad_embed_dim=user_wad_embed_dim,
        )
        self.user_att_pooling = ParallelTransformerBlock(
            dim=seq_embed_dim, dim_head=seq_embed_dim, heads=1
        )
        # nlp_out + aep_seq_out + svc_out + new_svc_out + user_ctx_out
        self.user_concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim \
                               + seq_embed_dim + seq_embed_dim
        self.user_moe = MoEFFLayer(
            dim=seq_embed_dim,
            num_experts=user_moe_kwargs.get("num_experts"),
            expert_capacity=user_moe_kwargs.get("expert_capacity"),
            hidden_size=seq_embed_dim,
            expert_class=ExpertLayer,
            # num_K=user_moe_kwargs.get("num_K"),
        )

        self.user_act = nn.LeakyReLU(0.2)
        self.user_dropout = nn.Dropout(p=0.1)
        self.user_dense_0 = nn.Linear(
            in_features=self.user_concat_dim,
            out_features=seq_embed_dim * 3
        )
        self.user_dense_1 = nn.Linear(
            in_features=seq_embed_dim * 3,
            out_features=seq_embed_dim
        )

        # offer layers
        self.offer_context_head = ContextTransformerAndWide(
            deep_dims=offer_deep_dims,
            num_wide=offer_num_wide,
            deep_embed_dims=offer_deep_embed_dims,
            wad_embed_dim=offer_wad_embed_dim,
        )
        # offer_context_out
        self.offer_concat_dim = seq_embed_dim
        self.offer_act = nn.LeakyReLU(0.2)
        self.offer_dropout = nn.Dropout(p=0.1)
        self.offer_dense_0 = nn.Linear(
            in_features=self.offer_concat_dim,
            out_features=self.offer_concat_dim + self.offer_concat_dim // 2
        )
        self.offer_dense_1 = nn.Linear(
            in_features=self.offer_concat_dim + self.offer_concat_dim // 2,
            out_features=seq_embed_dim
        )

        self.out_act = nn.Sigmoid()

    def forward(self, user_deep_in, offer_deep_in, svc_in, new_svc_in, page_in, item_in, vl_in,
                user_wide_in, offer_wide_in, search_in):
        svc_out = self.svc_embedding(svc_in.long())
        svc_out = self.mm_pooling(svc_out)
        new_svc_out = self.new_svc_embedding(new_svc_in.long())
        new_svc_out = self.mm_pooling(new_svc_out)

        aep_seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

#        search_out = self.nlp_encoder(**search_in).last_hidden_state[:, 0, :].to(dtype=torch.float32)
        search_out = self.nlp_encoder(**search_in).pooler_output.to(dtype=torch.float32)
        search_out = self.search_nlp_dense_0(search_out)
        search_out = self.nlp_act(search_out)
        search_out = self.search_nlp_dense_1(search_out)
        search_out = self.nlp_act(search_out)

        user_ctx_out = self.user_context_head(deep_in=user_deep_in, wide_in=user_wide_in)
        user_out = torch.stack([search_out, aep_seq_out, svc_out, new_svc_out, user_ctx_out], dim=1)
        user_out = self.user_att_pooling(user_out)
        user_out, user_aux_loss = self.user_moe(user_out)
        user_out = user_out.reshape(-1, self.user_concat_dim)
        user_out = self.user_dense_0(user_out)
        user_out = self.user_act(user_out)
        user_out = self.user_dropout(user_out)
        user_out = self.user_dense_1(user_out)
        user_out = self.user_act(user_out)

        offer_ctx_out = self.offer_context_head(deep_in=offer_deep_in, wide_in=offer_wide_in)
        offer_out = offer_ctx_out
        offer_out = self.offer_dense_0(offer_out)
        offer_out = self.offer_act(offer_out)
        offer_out = self.offer_dropout(offer_out)
        offer_out = self.offer_dense_1(offer_out)
        offer_out = self.offer_act(offer_out)

        out = torch.mul(user_out, offer_out)
        out = torch.sum(out, dim=1)
        out = self.out_act(out)

        return out, user_out, offer_out, user_aux_loss


class GRecUPG(nn.Module):
    def __init__(self, user_deep_dims, user_deep_embed_dims, user_num_wide, user_wad_embed_dim,
                 svc_dim, svc_embed_dim, new_svc_dim, new_svc_embed_dim, page_dim, item_dim,
                 seq_embed_dim, nlp_encoder_path, nlp_dim, sequence_transformer_kwargs,
                 user_moe_kwargs):
        super().__init__()
        self.seq_embed_dim = seq_embed_dim

        # user layers
        self.svc_embedding = nn.Embedding(svc_dim, svc_embed_dim)
        self.new_svc_embedding = nn.Embedding(new_svc_dim, new_svc_embed_dim)
        self.mm_pooling = MeanMaxPooling()

        self.page_embedding = nn.Embedding(page_dim, seq_embed_dim)
        self.item_embedding = nn.Embedding(item_dim, seq_embed_dim)
        self.sequence_transformer = ParallelTransformerAEP2S(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            heads=sequence_transformer_kwargs.get("seq_num_heads"),
            num_layers=sequence_transformer_kwargs.get("seq_num_layers"),
        )

        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        self.search_nlp_dense_0 = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=seq_embed_dim * 2
        )
        self.search_nlp_dense_1 = torch.nn.Linear(
            in_features=seq_embed_dim * 2,
            out_features=seq_embed_dim
        )
        self.nlp_act = nn.LeakyReLU(0.2)

        self.user_context_head = ContextTransformerAndWide(
            deep_dims=user_deep_dims,
            num_wide=user_num_wide,
            deep_embed_dims=user_deep_embed_dims,
            wad_embed_dim=user_wad_embed_dim,
        )
        self.user_att_pooling = ParallelTransformerBlock(
            dim=seq_embed_dim, dim_head=seq_embed_dim, heads=1
        )
        # nlp_out + aep_seq_out + svc_out + new_svc_out + user_ctx_out
        self.user_concat_dim = seq_embed_dim + seq_embed_dim + seq_embed_dim \
                               + seq_embed_dim + seq_embed_dim
        self.user_moe = MoEFFLayerTopK(
            dim=seq_embed_dim,
            num_experts=user_moe_kwargs.get("num_experts"),
            expert_capacity=user_moe_kwargs.get("expert_capacity"),
            hidden_size=seq_embed_dim,
            expert_class=ExpertLayer,
            num_K=user_moe_kwargs.get("num_K"),
        )

        self.user_act = nn.LeakyReLU(0.2)
        self.user_dropout = nn.Dropout(p=0.1)
        self.user_dense_0 = nn.Linear(
            in_features=self.user_concat_dim,
            out_features=seq_embed_dim * 3
        )
        self.user_dense_1 = nn.Linear(
            in_features=seq_embed_dim * 3,
            out_features=seq_embed_dim
        )

        self.out_dense = nn.Linear(
            in_features=seq_embed_dim,
            out_features=1
        )
        self.out_act = nn.Sigmoid()

    def forward(self, user_deep_in, svc_in, new_svc_in, page_in, item_in, vl_in,
                user_wide_in, search_in):
        svc_out = self.svc_embedding(svc_in.long())
        svc_out = self.mm_pooling(svc_out)
        new_svc_out = self.new_svc_embedding(new_svc_in.long())
        new_svc_out = self.mm_pooling(new_svc_out)

        aep_seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

        search_out = self.nlp_encoder(**search_in).pooler_output.to(dtype=torch.float32)
        search_out = self.search_nlp_dense_0(search_out)
        search_out = self.nlp_act(search_out)
        search_out = self.search_nlp_dense_1(search_out)
        search_out = self.nlp_act(search_out)

        user_ctx_out = self.user_context_head(deep_in=user_deep_in, wide_in=user_wide_in)
        user_out = torch.stack([search_out, aep_seq_out, svc_out, new_svc_out, user_ctx_out], dim=1)
        user_out = self.user_att_pooling(user_out)
        user_out, user_aux_loss = self.user_moe(user_out)
        user_out = user_out.reshape(-1, self.user_concat_dim)
        user_out = self.user_dense_0(user_out)
        user_out = self.user_act(user_out)
        user_out = self.user_dropout(user_out)
        user_out = self.user_dense_1(user_out)
        user_out = self.user_act(user_out)

        out = self.out_dense(user_out)
        out = self.out_act(out)

        return out, user_aux_loss

    
class PaRS2(nn.Module):
    def __init__(self, deep_dims, page_dim, seq_dim, page_embed_dim, seq_embed_dim, item_embed_dim, item_meta_dim, item_meta_embed_dim, item_pre_embed_dim, deep_embed_dims, wad_embed_dim, nlp_embed_dim, seq_hidden_size, nlp_encoder_path, task_type_dim, task_type_embed_dim, task_out_dims, num_wide=0, num_shared=0, nlp_dim=0, page_meta_dim=0, page_meta_embed_dim=0, num_page_meta_wide=0, page_meta_wide_embed_dim=0, num_item_meta_wide=0, item_meta_wide_embed_dim=0, page_freeze=None, item_freeze=None, item_pre_freeze=None, nlp_freeze=None, context_head_kwargs=None, sequence_transformer_kwargs=None, page_embedding_weight=None, page_meta_embedding_weight=None, item_embedding_weight=None, item_meta_embedding_weight=None, item_pre_embedding_weight=None, shared_embeddings_weight=None, moe_kwargs=None):
        super().__init__()
        self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        context_head_kwargs = context_head_kwargs if context_head_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        
        if page_embedding_weight is None:
            print("not use pretrained embedding")
            self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        else:
            print("use pretrained item embedding")
            self.page_embedding = nn.Embedding.from_pretrained(page_embedding_weight, freeze=False)
        if item_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_embedding = nn.Embedding(seq_dim, item_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_embedding = nn.Embedding.from_pretrained(item_embedding_weight, freeze=False)
        if page_meta_embedding_weight is None:
            print("not use pretrained embedding")
            self.page_meta_embedding = nn.Embedding(page_meta_dim, page_meta_embed_dim)
        else:
            print("use pretrained item embedding")
            self.page_meta_embedding = nn.Embedding.from_pretrained(page_meta_embedding_weight, freeze=False)
        if item_meta_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_meta_embedding = nn.Embedding(item_meta_dim, item_meta_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_meta_embedding = nn.Embedding.from_pretrained(item_meta_embedding_weight, freeze=False)
        if item_pre_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_pre_embedding = nn.Embedding(seq_dim, item_pre_embed_dim)
        else:
            print("use pretrained item pre embedding")
            self.item_pre_embedding = nn.Embedding.from_pretrained(item_pre_embedding_weight, freeze=False)
        if page_freeze:
            self.page_embedding.weight.requires_grad = False
        if item_freeze:
            self.item_embedding.weight.requires_grad = False
        if item_pre_freeze:
            self.item_pre_embedding.weight.requires_grad = False

        if nlp_freeze:
            for param in self.nlp_encoder.parameters():
                param.requires_grad = False
         
        self.combined_dim = nlp_embed_dim + wad_embed_dim + seq_embed_dim + seq_embed_dim + seq_embed_dim
        self.task_embedding = nn.Embedding(task_type_dim, seq_embed_dim)
        self.context_head = ContextHead(
            deep_dims=deep_dims,
            num_wide=num_wide,
            item_embedding=self.item_embedding,
            shared_embeddings_weight=shared_embeddings_weight,
            wad_embed_dim=wad_embed_dim,
            deep_embed_dims=deep_embed_dims
        )
        self.sequence_transformer = ParallelTransformerAEP3(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            item_meta_embedding=self.item_meta_embedding,
            item_pre_embedding=self.item_pre_embedding,
            dim=seq_embed_dim,
            dim_head=seq_embed_dim,
            heads=sequence_transformer_kwargs.get("seq_num_heads"),
            num_layers=sequence_transformer_kwargs.get("seq_num_layers"),
            num_page_meta_wide=num_page_meta_wide,
            num_item_meta_wide=num_item_meta_wide,
            page_meta_embedding=self.page_meta_embedding,
            page_meta_wide_embed_dim=page_meta_wide_embed_dim,
            item_meta_wide_embed_dim=item_meta_wide_embed_dim,
            moe_kwargs=moe_kwargs
        )
    
        self.att_pooling = ParallelTransformerBlock(
            dim=256, dim_head=256, heads=1
        )
        self.seq_dense = torch.nn.Linear(
            in_features=seq_embed_dim,
            out_features=seq_embed_dim
        )
        self.nlp_dense = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=nlp_embed_dim
        ) 
        self.moe = MoEFFLayer(dim=seq_embed_dim, num_experts=moe_kwargs.get("num_experts"), expert_capacity=moe_kwargs.get("expert_capacity"), router_jitter_noise=moe_kwargs.get("router_jitter_noise"), hidden_size=seq_embed_dim, expert_class=ExpertLayer)

        self.tasks_dense1 = nn.Linear(
            self.combined_dim, 
            self.combined_dim // 2
        )
        self.tasks_dense2 = nn.Linear(
            self.combined_dim // 2, 
            task_out_dims[0]
        )
        self.tasks_act1 = self.tasks_act2 = nn.LeakyReLU(0.2)
        self.seq_dim = seq_dim
        self.task_type_dim = task_type_dim

        if num_item_meta_wide > 0:
            self.wide_meta_batch_norm = nn.BatchNorm1d(num_item_meta_wide)
            if item_meta_wide_embed_dim > 0:
                self.wide_meta_dense = nn.Linear(num_item_meta_wide, item_meta_wide_embed_dim)
            else: 
                print("There are wide meta features but item_meta_wide_embed_dim is not given!")
            self.wide_meta_act = nn.LeakyReLU(0.2)

    def split_task(self, task_type_dim, task_in, combined_out):
        task_indices = []
        task_outs = []
        task_user_outs = []
        for i in range(task_type_dim):
            task_indice = task_in == i
            task_indice = torch.nonzero(task_indice).flatten()
            task_input = combined_out[task_indice]
            task_out = self.tasks_dense1(task_input)
            task_user_out = self.tasks_act1(task_out)
            task_out = self.tasks_dense2(task_user_out)
            task_indices.append(task_indice)
            task_user_outs.append(task_user_out)
            task_outs.append(task_out)
        return task_indices, task_outs, task_user_outs
        
    def forward(self, deep_in, page_in, item_in, item_meta_in, vl_in, task_in, current_in, current_meta_in, wide_in=None, input_ids=None, attention_mask=None, page_meta_in=None, page_meta_wide_in=None, current_meta_wide_in=None, item_meta_wide_in=None, shared_in=None):
        """
        Args:
            deep_in: list, a list of tensor of shape [batch_size, deep_dims]
            page_in: tensor, page input sequence [batch_size, seq_len]
            item_in: tensor, item input sequence [batch_size, seq_len]
            item_meta_in: tensor, item deep meta data input sequence [batch_size, seq_len]
            vl_in: tensor, valid length of input data [batch_size]
            taks_in: tensor, task type index [batch_size]
            current_in: tensor, current item input [batch_size]
            current_meta_in: tensor, current item deep meta data input [batch_size]
            wide_in: list, a list of tensor of shape [batch_size, num_wide]
            inputs_id: list, a list of tensor of shape [batch_size, num_shared] (default=None)
            att_mask: tensor, tensor of shape [batch_size, sentence_length] (default=None)
            page_meta_in: tensor, page deep meta data input sequence [batch_size, seq_len]
            page_meta_wide_in: tensor, page wide meta data input sequence [batch_size, num_page_meta_wide, seq_len]
            current_meta_wide_in: list, a list of tensor of shape [batch_size, num_item_meta_wide]
            item_meta_wide_in: tensor, item wide meta data input sequence [batch_size, num_item_meta_wide, seq_len]
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None)

        Return:
            out: tensor, shape [batch_size, seq_dim].
            user_out: tensor, shape [batch_size, seq_embed_dim].
        """
        search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state[:,0,:].to(dtype=torch.float32)
        search_out = self.nlp_dense(search_out)
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, item_meta_in=item_meta_in, vl_in=vl_in, page_meta_in=page_meta_in, page_meta_wide_in=page_meta_wide_in, item_meta_wide_in=item_meta_wide_in)
        seq_out = self.seq_dense(seq_out)
        current_item_out = self.item_embedding(current_in)
        current_meta_out = self.item_meta_embedding(current_meta_in)
        current_pre_out = self.item_pre_embedding(current_in)	        
        if current_meta_wide_in is not None:
            current_meta_wide_in_list = [wide_i.float() for wide_i in current_meta_wide_in]
            current_meta_wide_cat = torch.stack(current_meta_wide_in_list, dim=0)
            current_meta_wide_out = torch.transpose(current_meta_wide_cat, dim1=1, dim0=0)
            if len(current_meta_wide_in) > 1:
                current_meta_wide_out_norm = self.wide_meta_batch_norm(current_meta_wide_out)
            else:
                current_meta_wide_out_norm = current_meta_wide_out
            current_meta_wide_out_norm = self.wide_meta_dense(current_meta_wide_out_norm)
            current_meta_wide_out_norm = self.wide_meta_act(current_meta_wide_out_norm)
            current_out = torch.cat((current_item_out, current_meta_out, current_pre_out, current_meta_wide_out_norm), 1)
        else:
            current_out = torch.cat((current_item_out, current_meta_out, current_pre_out), 1)
        
        task_out = self.task_embedding(task_in)
        outs = torch.cat((seq_out[:, None, :], ctx_out[:, None, :], search_out[:, None, :], current_out[:, None, :], task_out[:, None, :]), dim=1)
        outs = self.att_pooling(outs)
        outs, aux_loss = self.moe(outs)
        
        outs = outs.reshape(-1, self.combined_dim)
        task_indices, task_outs, task_user_outs = self.split_task(self.task_type_dim, task_in, outs)
        return (tuple(task_indices), tuple(task_outs), aux_loss)
