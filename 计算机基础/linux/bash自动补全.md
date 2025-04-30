## bash自动补全


1. 安装 补全工具 bash-completion
    ```sh
    yum install -y bash-completion
    ```
2. 加载
    ```sh
    [[ $PS1 && -f /usr/share/bash-completion/bash_completion ]] && \
        . /usr/share/bash-completion/bash_completion
    ```
3. 验证 bash_completion 的安装状态
   有输出则正常
    ```sh
    type _init_completion
    ```

4. 启用 bash 补全
   1. 针对当前用户
      ```sh
      # 例如 添加 kubectl 补全功能
      echo 'source <(kubectl completion bash)' >>~/.bashrc

      # 例如 添加 docker 补全功能
      echo 'source <(docker completion bash)' >>~/.bashrc

      # 例如 添加 helm 补全功能
      echo 'source <(helm completion bash)' >>~/.bashrc
      ```
   2. 针对所有用户 
      ```sh
      # kubectl 补全功能
      kubectl completion bash | sudo tee /etc/bash_completion.d/kubectl > /dev/null
      # docker 补全功能
      docker completion bash | sudo tee /etc/bash_completion.d/docker > /dev/null
      ```
