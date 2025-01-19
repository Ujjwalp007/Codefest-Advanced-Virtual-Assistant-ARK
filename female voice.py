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

def listenToAudio():
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
    
def processText(prompt):
    """
    Sends the given prompt to the OpenAI API to generate a response, and returns the generated text.
    """
    # generate text using GPT3.5-turbo's API
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens= 150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # extract text from API response
    text = response.choices[0].text.strip()
    return text

# main loop for the program
while True:
    # get user's speech input
    prompt = listenToAudio()
    
    if prompt:
        # process user input using GPT-3 API
        output = processText(prompt)
        print("Output:", output)
        
        # speak the output with a female voice
        engine.say(output)
        engine.runAndWait()
        
        # display the output
        print(output)
