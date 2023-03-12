# try-chatgpt
ChatGPTを試す場所

## 確認動作環境

- OS: Ubuntu 20.04 on WSL2
- GPU: NVIDIA GeForce RTX 2070 SUPER

## HOW TO

```shell
pipenv run start
```

## 事前準備

VOICEVOXはDockerで起動する。
デフォルトポート 50021 で動かすと、 Windows 側の VOICEBOX が動かなくなるため、ポートをずらして起動している。

```shell
docker pull voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
docker run --rm --gpus all -p '127.0.0.1:50121:50021' voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
```

## クレジット

VOICEVOX:四国めたん を利用して読み上げをしています。
