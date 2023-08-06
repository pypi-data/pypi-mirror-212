from ailab.atp_finetuner.model.model import AILabModel
from transformers import ViltConfig, ViltForQuestionAnswering
from ailab.atp_finetuner.build import ModelRg
from ailab.atp_finetuner.constant import Task, Model

@ModelRg.register((Task.visual_question_answering, Model.vilt))
class ViltForVQAModel(AILabModel):
    def __init__(self, model: any) -> None:
        super().__init__(model)

    def forward(self):
        pass
    
    @classmethod
    def build_model(cls, device_name:str, model_name:str, **kwargs):
        config = ViltConfig.from_pretrained(model_name)
        model = ViltForQuestionAnswering.from_pretrained(model_name,
                                                    num_labels=len(config.id2label),
                                                    id2label=config.id2label,
                                                    label2id=config.label2id)
        import torch
        device = torch.device(device_name)
        model.to(device)
        return cls(model)
    
    def get_inside_models(self, model_type:str):
        pass
