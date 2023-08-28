https://gist.github.com/hanifa2102/e038ffa86b807a874998d0bd01b7da4b

#https://k0nze.dev/posts/install-pyenv-venv-vscode/
Set up pyenv and venv 

# Set up bamboolib using python 3.8.13
python -m venv llmenv
source llmenv/bin/activate
pip install --upgrade pip
pip install notebook==6.5.5
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
pip install --upgrade bamboolib
pip install jupyterlab

ssh-keygen -t rsa -b 4096 -C "hanifa.email@gmail.com"
eval "$(ssh-agent -s)"    start-ssh-agent.cmd
Private_key : ssh-add ~/.ssh/id_rsa
Public_key : Copypasta id_rsa.pub >> https://github.com/settings/keys
ssh -T git@github.com

config
Host github.com
Hostname ssh.github.com
IdentityFile ~/.ssh/id_rsa
Port 443

pip install datasets evaluate transformers[sentencepiece] torch accelerate xformers
