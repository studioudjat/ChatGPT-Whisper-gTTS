import whisper
import gradio as gr
import openai
from gtts import gTTS
from IPython.display import Audio

openai.api_key = "your-openai-api-key"

class ChatGPTAPI:
    def __init__(self, system_setting):
        self.system = {"role": "system", "content": system_setting}
        self.input_list = [self.system]
        self.logs = []

    def input_message(self, input_text):
        self.input_list.append({"role": "user", "content": input_text})
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=self.input_list
        )
        self.logs.append(result)
        self.input_list.append(
            {"role": "assistant", "content": result.choices[0].message.content}
        )
        return self.input_list[-2]["content"], self.input_list[-1]["content"]
        
def whisperTranscribe(audio):

    model = whisper.load_model("base")

    # Simple code
    #result = model.transcribe(audio)
    #return result["text"]
    
    # Access lower-level model

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    #print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions(fp16 = False)
    result = whisper.decode(model, mel, options)

    # post text to OpenAI API
    text_user, text_chatgpt = api.input_message(result.text)

    # convert transcript to audio file
    tts = gTTS(text=text_chatgpt, lang="ja", tld="co.jp", slow=False)
    tts.save("result.mp3")

    # output the recognized text
    return "result.mp3"
  
api = ChatGPTAPI(
    system_setting="あなたはいつもポジティブな人です。返答は30文字以内にしてください。では、会話を始めましょう。"
)

audio_input = gr.Audio(source="microphone", type="filepath")
interface = gr.Interface(
    fn=whisperTranscribe, inputs=audio_input, outputs=[gr.Audio()]
)
interface.launch(debug="False")
  
  
