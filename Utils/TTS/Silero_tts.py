import os
import torch


def tts(text,):
    device = torch.device('cpu')
    torch.set_num_threads(4)
    local_file = 'model.pt'
    print('got here!')
    if not os.path.isfile(local_file):
        torch.hub.download_url_to_file(f'https://models.silero.ai/models/tts/en/v3_en.pt',
                                    local_file)  
    print('got here!!')
    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    model.to(device)
    print('got here!!!')
    example_text = str(text).strip().lower()
    sample_rate = 48000
    speaker='en_67'
    print('got here!!!!')

    audio_paths = model.save_wav(text=example_text,
                                speaker=speaker,
                                sample_rate=sample_rate)
    #with open("reply.wav", "wb") as outfile:
        #outfile.write(audio_paths.content)
    print('got here!!!!!!')
    return 'test.wav'

if __name__ == "__main__":
    print(tts('Goodbye!'))
