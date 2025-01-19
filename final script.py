# import necessary libraries
import openai  # for accessing the OpenAI API
import pyttsx3  # for text-to-speech conversion
import speech_recognition as sr  # for speech recognition

# initialize text-to-speech engine with a female voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use the ID of the desired female voice
engine.say('Hello, how are you?')
engine.runAndWait()

# set up OpenAI API credentials
openai.api_key = "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"

# initialize speech recognizer
listener = sr.Recognizer()

def listen_to_audio():
    """
    Uses the microphone to listen for audio input and returns the recognized text.
    """
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            result = listener.recognize_google(voice)
            print(f"You said: {result}\n")
            return result
    except sr.UnknownValueError:
        print("Sorry, I did not understand what you said.")
        return None
    except sr.RequestError as e:
        print("Sorry, my speech service is not available at the moment.")
        return None


def process_text(prompt):
    """
    Sends the given prompt to the OpenAI API to generate a response, and returns the generated text.
    """
    # generate text using GPT3.5-turbo's API
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=400,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # extract text from API response
    text = response.choices[0].text.strip()

    # check if output is Python code
    if 'def' in text or 'class' in text or 'import' in text:
        # print code with indentation
        code_lines = text.split('\n')
        indented_code = '\n'.join(['    ' + line for line in code_lines])
        print(indented_code)
        return process_text(indented_code)

    return text


def main():
    """
    Main loop for the program.
    """
    while True:
        # get user's speech input
        prompt = listen_to_audio()

        if prompt:
            # process user input using GPT-3 API
            output = process_text(prompt)

            if output is not None:
                # display the output and speak it at the same time
                print(output)
                engine.say(output)
                engine.runAndWait()


if __name__ == '__main__':
    main()

