from setuptools import setup
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='adua',  # Replace with your package name
    version='1.2.3',
    author='Abhay Bairagi',
    author_email='abhaynarayanbairagi@gmail.com',
    description='You can use this to create your own assistant',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['adua'],  # List all the packages you want to include
    install_requires=[
        'face_recognition',
        'opencv-python',
        'pyttsx3',
        'wikipedia',
        'wolframalpha',
        'SpeechRecognition',
        'openai',
        'numpy',
        'dlib'
    ],
)
