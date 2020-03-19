from Hotel import settings
import sys
import torch
import os

sys.path.append(os.path.join(settings.BASE_DIR, "extral_apps", "m_facemask", "load_model"))


# model_path = str(Path(__file__).parents[1] / r'load_model') + "\\"
# print(model_path)


def load_pytorch_model(model_path):
    print(model_path)
    model = torch.load(model_path)
    return model


def pytorch_inference(model, img_arr):
    y_bboxes, y_scores, = model.forward(torch.tensor(img_arr).float())
    return y_bboxes.detach().numpy(), y_scores.detach().numpy()
