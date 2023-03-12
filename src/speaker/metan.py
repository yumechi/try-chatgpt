import http
import json
import httpx
from playsound import playsound
from pathlib import Path


class Metan:
    SPEAKER_STYLE = {
        0: "あまあま",
        2: "ノーマル",
        4: "セクシー",
        6: "ツンツン",
        36: "ささやき",
        37: "ひそひそ",
    }
    STORE_PATH = Path("storage/audio")

    def __init__(self, style: int = 0):
        if style not in self.SPEAKER_STYLE:
            raise ValueError(
                f"{style} is not for metan style: accepted={self.SPEAKER_STYLE.keys()}"
            )
        self.style = style

        # TODO: separate HOST_URL data to speaker base model
        # TODO: allowing connections from other than local
        self.host_url = "http://localhost:50121"

    def play_sound(self, message, filename="temp.wav"):
        if len(message) == 0:
            raise ValueError("empty message")
        store_path = self.STORE_PATH / filename
        print(f"debug: {message=} {store_path=}")

        audio_query = self.__get_audio_query(message)
        synthesis_data = self.__get_synthesis(audio_query)
        self.__save_wavefile(synthesis_data, store_path)
        self.__play_sound(store_path)
        self.__remove_file(store_path)

    def __get_audio_query(self, message: str) -> dict[any, any]:
        url = self.host_url + "/audio_query"
        params = {
            "text": message,
            "speaker": self.style,
        }
        res = httpx.post(url, params=params, timeout=10.0)
        if res.status_code != http.HTTPStatus.OK:
            raise Exception(
                f"request audio query error: {res.status_code=}, {res.text}"
            )
        return res.json()

    def __get_synthesis(self, audio_query: dict[any, any]) -> bytes:
        url = self.host_url + "/synthesis"
        params = {
            "speaker": self.style,
        }
        res = httpx.post(
            url, params=params, content=json.dumps(audio_query), timeout=10.0
        )
        if res.status_code != http.HTTPStatus.OK:
            raise Exception(f"request synthesis error: {res.status_code=}, {res.text}")
        return res.content

    def __save_wavefile(self, synthesis_data: bytes, filename: Path):
        with open(filename, "wb") as f:
            f.write(synthesis_data)
        return filename

    def __play_sound(self, filename: Path) -> None:
        playsound(filename)

    def __remove_file(self, filename: Path) -> None:
        filename.unlink()


if __name__ == "__main__":
    # TODO: テスト
    t = input("めたんちゃんにしゃべらせたい言葉: ")
    metan = Metan(style=0)
    metan.play_sound(t)
