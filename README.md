完整ctglm-6b模型下载：

git lfs install
git clone https://huggingface.co/THUDM/chatglm-6b

上传的ctglm-6b的checkpoint已转为mindspore版本

微调ctglm模型使用mindformers的run_glm_6b_lora.yaml

训练微调ctglm使用的datasets在advertisegen文件夹中，AD数据集来自清华云，family数据集来自kaggle。
