# Langchain rdmp 配置

- 新增虚拟环境

```
conda create langchain_rdmp python=3.11
```

- 查看虚拟环境
```
conda info --envs
```

- 启动虚拟环境
```
conda activate langchain_rdmp
```

- 安装依赖包
```
pip install -r requirements.txt 
```
- 使用 Poetry 管理打包三方库



- 启动服务
```
 streamlit run chat.py
```