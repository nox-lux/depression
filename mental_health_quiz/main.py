import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from mysql.connector import Error
import random
import os
import sys
import subprocess
import csv
import platform

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

MYSQL_CONFIG = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'database': 'mental_health_app',
    'auth_plugin': 'mysql_native_password'
}

QUESTIONS_BANK = {
    "Sleep": [
        {"question": "How would you rate the quality of your sleep recently?", "options": [("Excellent", 10), ("Good", 5), ("Average", 0), ("Poor", -5), ("Very Poor", -10)]},
        {"question": "On average, how many hours of sleep do you get per night?", "options": [("8+ hours", 10), ("7-8 hours", 5), ("6-7 hours", -2), ("5-6 hours", -5), ("Less than 5 hours", -10)]},
        {"question": "How often do you wake up feeling refreshed?", "options": [("Almost always", 10), ("Often", 5), ("Sometimes", 0), ("Rarely", -5), ("Never", -10)]},
        {"question": "Do you have a consistent sleep schedule, even on weekends?", "options": [("Yes, very consistent", 10), ("Mostly consistent", 5), ("Somewhat", -2), ("Not really", -5), ("No, it's chaotic", -10)]},
        {"question": "How long does it typically take you to fall asleep?", "options": [("Under 15 minutes", 10), ("15-30 minutes", 5), ("30-60 minutes", -2), ("Over an hour", -5), ("It varies greatly", -10)]},
        {"question": "Is your sleep often disturbed by noise or other factors?", "options": [("Never", 10), ("Rarely", 5), ("Sometimes", 0), ("Often", -5), ("Almost always", -10)]},
        {"question": "How much does lack of sleep affect your mood the next day?", "options": [("Not at all", 10), ("A little", 5), ("Moderately", -2), ("Significantly", -5), ("It ruins my day", -10)]},
        {"question": "Do you feel sleepy or groggy during the day?", "options": [("Never", 10), ("Rarely", 5), ("Sometimes", 0), ("Often", -5), ("Constantly", -10)]},
        {"question": "Have you found effective ways to wind down before bed?", "options": [("Yes, very effective", 10), ("Somewhat effective", 5), ("I try, but it's hit or miss", 0), ("Not really", -5), ("I don't have a routine", -10)]},
        {"question": "How is your dreaming experience? (e.g., pleasant, stressful)", "options": [("Mostly pleasant", 10), ("Neutral / Don't remember", 5), ("Mixed", 0), ("Often stressful or nightmares", -5), ("Very distressing nightmares", -10)]},
        {"question": "Do you rely on medication or aids to help you sleep?", "options": [("Never", 10), ("Rarely", 5), ("Sometimes", 0), ("Often", -5), ("Every night", -10)]}
    ],
    "Social": [
        {"question": "How often do you connect with friends or family?", "options": [("Daily", 8), ("A few times a week", 4), ("Once a week", 0), ("A few times a month", -4), ("Rarely or never", -8)]},
        {"question": "How comfortable do you feel in social gatherings?", "options": [("Very comfortable", 8), ("Comfortable", 4), ("Neutral", 0), ("Uncomfortable", -4), ("Very uncomfortable", -8)]},
        {"question": "Do you feel you have a strong support system?", "options": [("Yes, very strong", 8), ("Yes, it's good", 4), ("It's okay", 0), ("It's weak", -4), ("I feel isolated", -8)]},
        {"question": "How easy is it for you to meet new people?", "options": [("Very easy", 8), ("Fairly easy", 4), ("Neutral", 0), ("Difficult", -4), ("Extremely difficult", -8)]},
        {"question": "Do you feel understood by the people you are close to?", "options": [("Completely", 8), ("Mostly", 4), ("Sometimes", 0), ("Rarely", -4), ("Not at all", -8)]},
        {"question": "How often do you initiate social plans?", "options": [("Often", 8), ("Sometimes", 4), ("Rarely", 0), ("Almost never", -4), ("Never", -8)]},
        {"question": "Are you satisfied with the depth of your friendships?", "options": [("Very satisfied", 8), ("Satisfied", 4), ("Neutral", 0), ("Unsatisfied", -4), ("Very unsatisfied", -8)]},
        {"question": "Do you feel lonely, even when you are with people?", "options": [("Never", 8), ("Rarely", 4), ("Sometimes", 0), ("Often", -4), ("Almost always", -8)]},
        {"question": "How do you handle disagreements with loved ones?", "options": [("Constructively", 8), ("Okay, but could be better", 4), ("I avoid them", 0), ("Poorly", -4), ("It's always a big fight", -8)]},
        {"question": "Do you prefer spending time alone or with others?", "options": [("I enjoy a healthy balance", 8), ("Mostly with others", 4), ("Mostly alone", 0), ("Almost exclusively alone by choice", -4), ("Almost exclusively alone due to anxiety", -8)]},
        {"question": "How much energy does socializing take from you?", "options": [("It energizes me!", 8), ("It's neutral", 4), ("It's a bit draining", 0), ("It's very draining", -4), ("It's completely exhausting", -8)]}
    ],
    "Activity": [
        {"question": "How many days a week do you engage in at least 30 minutes of physical activity?", "options": [("5-7 days", 9), ("3-4 days", 5), ("1-2 days", 0), ("Less than 1 day", -4), ("Never", -9)]},
        {"question": "Do you enjoy the types of physical activity you do?", "options": [("Love it!", 9), ("It's enjoyable", 5), ("It's okay, just a chore", 0), ("I dislike it", -4), ("I hate it", -9)]},
        {"question": "How does exercise impact your mental clarity?", "options": [("Greatly improves it", 9), ("Improves it", 5), ("No noticeable effect", 0), ("Makes me feel tired/foggy", -4), ("I don't exercise enough to know", -9)]},
        {"question": "Do you spend much time outdoors?", "options": [("Daily", 9), ("A few times a week", 5), ("Once a week", 0), ("Rarely", -4), ("Almost never", -9)]},
        {"question": "How would you describe your current fitness level?", "options": [("Excellent", 9), ("Good", 5), ("Average", 0), ("Below average", -4), ("Poor", -9)]},
        {"question": "What is your main barrier to exercising more?", "options": [("I have no barriers", 9), ("Lack of time", 5), ("Lack of motivation", 0), ("Lack of energy", -4), ("Health issues or cost", -9)]},
        {"question": "Do you incorporate stretching or flexibility work into your routine?", "options": [("Yes, regularly", 9), ("Sometimes", 5), ("Rarely", 0), ("Never", -4), ("What's stretching?", -9)]},
        {"question": "How consistent is your exercise routine?", "options": [("Very consistent", 9), ("Fairly consistent", 5), ("On and off", 0), ("Inconsistent", -4), ("Non-existent", -9)]},
        {"question": "Do you listen to your body and rest when needed?", "options": [("Always", 9), ("Usually", 5), ("Sometimes", 0), ("Rarely, I push through pain", -4), ("I don't have a routine to rest from", -9)]},
        {"question": "Does your daily routine involve a lot of sitting?", "options": [("Very little", 9), ("A moderate amount", 5), ("A lot", 0), ("Most of the day", -4), ("Almost the entire day", -9)]},
        {"question": "Have you seen positive changes from your physical activity?", "options": [("Yes, significant changes", 9), ("Yes, some positive changes", 5), ("Not really", 0), ("No, I feel the same or worse", -4), ("I don't do any", -9)]}
    ],
    "Mood": [
        {"question": "How would you describe your general mood over the past week?", "options": [("Very positive", 10), ("Mostly positive", 5), ("Neutral", 0), ("Mostly negative", -5), ("Very negative", -10)]},
        {"question": "How often do you experience mood swings?", "options": [("Rarely or never", 10), ("Occasionally", 5), ("Sometimes", 0), ("Frequently", -5), ("Constantly", -10)]},
        {"question": "Are you able to find joy in small, everyday things?", "options": [("Yes, often", 10), ("Sometimes", 5), ("Rarely", 0), ("Almost never", -5), ("Not at all", -10)]},
        {"question": "How often do you feel irritable or easily annoyed?", "options": [("Rarely", 10), ("Sometimes", 5), ("About half the time", 0), ("Often", -5), ("Almost always", -10)]},
        {"question": "Do you feel a sense of hopelessness?", "options": [("Never", 10), ("Rarely", 5), ("Sometimes", 0), ("Often", -5), ("Pervasively", -10)]},
        {"question": "How often do you laugh out loud?", "options": [("Several times a day", 10), ("Daily", 5), ("A few times a week", 0), ("Rarely", -5), ("I can't remember the last time", -10)]},
        {"question": "Do you feel emotionally numb or detached?", "options": [("Never", 10), ("Rarely", 5), ("Sometimes", 0), ("Often", -5), ("Most of the time", -10)]},
        {"question": "How quickly do you bounce back from disappointments?", "options": [("Very quickly", 10), ("Fairly quickly", 5), ("Slowly", 0), ("Very slowly", -5), ("I don't bounce back", -10)]},
        {"question": "Do you feel that your emotional responses are appropriate to situations?", "options": [("Yes, always", 10), ("Usually", 5), ("Sometimes", 0), ("Often not", -5), ("Rarely", -10)]},
        {"question": "How much do you worry about things you can't control?", "options": [("Very little", 10), ("A moderate amount", 5), ("A lot", 0), ("A great deal", -5), ("It's all-consuming", -10)]},
        {"question": "When you feel down, do you know how to lift your spirits?", "options": [("Yes, I have effective strategies", 10), ("I have some ideas", 5), ("It's a struggle", 0), ("I feel helpless", -5), ("I tend to spiral downwards", -10)]}
    ],
    "Stress": [
        {"question": "How well are you able to manage stress?", "options": [("Very well", 9), ("Well", 5), ("Okay", 0), ("Poorly", -5), ("Not at all", -9)]},
        {"question": "Do you have healthy coping mechanisms for stress (e.g., exercise, hobbies)?", "options": [("Yes, several", 9), ("Yes, one or two", 5), ("I'm trying to develop them", 0), ("I tend to use unhealthy ones", -5), ("I have no coping mechanisms", -9)]},
        {"question": "How often do you feel overwhelmed by your responsibilities?", "options": [("Rarely", 9), ("Sometimes", 5), ("Frequently", 0), ("Most of the time", -5), ("Constantly", -9)]},
        {"question": "Are you able to relax and 'switch off' your mind?", "options": [("Easily", 9), ("With some effort", 5), ("It's difficult", 0), ("It's very difficult", -5), ("It's impossible", -9)]},
        {"question": "Do you practice mindfulness or meditation?", "options": [("Regularly", 9), ("Occasionally", 5), ("I've tried it", 0), ("Not for me", -5), ("What's mindfulness?", -9)]},
        {"question": "How does stress physically manifest in your body (e.g., headaches, tension)?", "options": [("It doesn't", 9), ("Rarely", 5), ("Sometimes", 0), ("Often", -5), ("I have constant physical symptoms", -9)]},
        {"question": "Are you able to say 'no' to additional commitments when you're busy?", "options": [("Yes, easily", 9), ("Yes, but I feel guilty", 5), ("I struggle with it", 0), ("Rarely", -5), ("Never, I always say yes", -9)]},
        {"question": "Do you feel in control of your life?", "options": [("Completely", 9), ("Mostly", 5), ("Sometimes", 0), ("Rarely", -5), ("Not at all", -9)]},
        {"question": "How much time do you dedicate to pure relaxation each week?", "options": [("Several hours", 9), ("A couple of hours", 5), ("Maybe an hour", 0), ("Very little", -5), ("None", -9)]},
        {"question": "Do you feel you are proactive or reactive when it comes to stress?", "options": [("Proactive, I prevent it", 9), ("Mostly proactive", 5), ("A mix of both", 0), ("Mostly reactive", -5), ("Completely reactive", -9)]},
        {"question": "How much does work/school stress bleed into your personal life?", "options": [("Not at all", 9), ("A little bit", 5), ("A moderate amount", 0), ("A lot", -5), ("It consumes my personal life", -9)]}
    ],
    "Hobbies": [
        {"question": "How often do you make time for hobbies and activities you enjoy?", "options": [("Daily", 5), ("A few times a week", 3), ("Once a week", 0), ("Rarely", -2), ("Never", -5)]},
        {"question": "Do you feel passionate or excited about your hobbies?", "options": [("Yes, very passionate", 5), ("Yes, they are enjoyable", 3), ("They're just okay", 0), ("I've lost interest", -2), ("I don't have any hobbies", -5)]},
        {"question": "Have you learned a new skill or hobby in the last year?", "options": [("Yes, and I love it", 5), ("Yes, I'm trying something", 3), ("I thought about it", 0), ("No, not interested", -2), ("No, I don't have time/energy", -5)]},
        {"question": "Do your hobbies help you de-stress?", "options": [("Yes, immensely", 5), ("Yes, they help a bit", 3), ("Not really", 0), ("They sometimes add stress", -2), ("I don't have any", -5)]},
        {"question": "Are your hobbies creative, active, or passive?", "options": [("A good mix of all three", 5), ("Mostly one type", 3), ("I don't really know", 0), ("I only watch TV/scroll social media", -2), ("I have no hobbies", -5)]},
        {"question": "Do you share your interests with others?", "options": [("Yes, I'm part of a group/community", 5), ("Yes, with friends", 3), ("Not really, it's a solo thing", 0), ("No, I'm embarrassed by them", -2), ("I don't have any", -5)]},
        {"question": "Do you feel a sense of accomplishment from your hobbies?", "options": [("Yes, often", 5), ("Sometimes", 3), ("Rarely", 0), ("No", -2), ("N/A", -5)]},
        {"question": "Is 'fun' a regular part of your weekly schedule?", "options": [("Absolutely!", 5), ("I try to make it so", 3), ("Not as much as I'd like", 0), ("Rarely", -2), ("Never", -5)]},
        {"question": "How much have your interests changed over the years?", "options": [("They evolve, it's exciting!", 5), ("They've changed a bit", 3), ("They're the same", 0), ("I've lost interest in everything", -2), ("I never had strong interests", -5)]},
        {"question": "Does lack of money or resources stop you from pursuing interests?", "options": [("Not at all", 5), ("Sometimes it's a factor", 3), ("Often, yes", 0), ("Yes, it's a major barrier", -2), ("N/A", -5)]},
        {"question": "Do you feel 'bored' often?", "options": [("Never, I always find something to do", 5), ("Rarely", 3), ("Sometimes", 0), ("Often", -2), ("Constantly", -5)]}
    ],
    "Balance": [
        {"question": "How balanced do you feel your work/school life and personal life are?", "options": [("Very balanced", 7), ("Balanced", 4), ("Slightly unbalanced", -1), ("Unbalanced", -4), ("Very unbalanced", -7)]},
        {"question": "Are you able to 'switch off' from work/school thoughts in your personal time?", "options": [("Yes, completely", 7), ("Mostly", 4), ("With difficulty", -1), ("Rarely", -4), ("Never", -7)]},
        {"question": "Do you take your full lunch break away from your desk/work area?", "options": [("Yes, always", 7), ("Most of the time", 4), ("Sometimes", -1), ("Rarely", -4), ("Never", -7)]},
        {"question": "How often do you work overtime or outside of your scheduled hours?", "options": [("Never", 7), ("Rarely", 4), ("Sometimes", -1), ("Often", -4), ("Constantly", -7)]},
        {"question": "Do you feel your workload is manageable?", "options": [("Yes, very manageable", 7), ("Yes, it's okay", 4), ("It's a struggle sometimes", -1), ("It's often overwhelming", -4), ("It's impossible", -7)]},
        {"question": "Do you have enough time for personal appointments and errands?", "options": [("Yes, plenty", 7), ("Usually", 4), ("It's a squeeze", -1), ("Rarely", -4), ("No, I have to sacrifice sleep/weekends", -7)]},
        {"question": "Do you feel supported by your manager/teachers?", "options": [("Very supported", 7), ("Supported", 4), ("Neutral", -1), ("Unsupported", -4), ("Actively undermined", -7)]},
        {"question": "Do you feel guilty when you take time off?", "options": [("Not at all", 7), ("A little bit", 4), ("Yes, moderately", -1), ("Yes, a lot", -4), ("I never take time off", -7)]},
        {"question": "Is your work/school environment positive or toxic?", "options": [("Very positive and collaborative", 7), ("Mostly positive", 4), ("Neutral / Mixed", -1), ("Mostly toxic", -4), ("Extremely toxic", -7)]},
        {"question": "Do you feel your work has meaning or purpose?", "options": [("Yes, a great deal", 7), ("Yes, some", 4), ("Not really", -1), ("No, it's just a job", -4), ("I feel it's meaningless", -7)]},
        {"question": "Do you dread Mondays (or the start of your work week)?", "options": [("No, I look forward to it", 7), ("Not really", 4), ("Sometimes", -1), ("Yes, often", -4), ("Yes, with intense anxiety", -7)]}
    ],
    "Self-Esteem": [
        {"question": "How would you rate your current level of self-esteem?", "options": [("Very high", 9), ("High", 5), ("Moderate", 0), ("Low", -5), ("Very low", -9)]},
        {"question": "How often do you engage in negative self-talk?", "options": [("Rarely or never", 9), ("Sometimes", 5), ("Frequently", 0), ("Most of the time", -5), ("My inner critic is constant", -9)]},
        {"question": "Are you able to accept compliments gracefully?", "options": [("Yes, easily", 9), ("Yes, with a little awkwardness", 5), ("I struggle with it", 0), ("I usually deflect or deny them", -5), ("I think they are lying", -9)]},
        {"question": "How do you handle making a mistake?", "options": [("I learn from it and move on", 9), ("I feel bad for a bit, then move on", 5), ("I beat myself up over it", 0), ("It ruins my day", -5), ("I dwell on it for days or weeks", -9)]},
        {"question": "Do you compare yourself to others on social media?", "options": [("Never", 9), ("Rarely", 5), ("Sometimes, but I know it's a highlight reel", 0), ("Often, and it makes me feel bad", -5), ("Constantly, and it's destructive", -9)]},
        {"question": "Do you feel worthy of love and happiness?", "options": [("Yes, absolutely", 9), ("I think so", 5), ("I'm not sure", 0), ("I often feel I'm not", -5), ("No, I don't believe I am", -9)]},
        {"question": "Can you list three things you like about yourself?", "options": [("Yes, easily", 9), ("With some thought", 5), ("It's a struggle", 0), ("I can't think of any", -5), ("I can only think of things I dislike", -9)]},
        {"question": "Do you advocate for your own needs in relationships?", "options": [("Yes, effectively", 9), ("I try to", 5), ("I find it difficult", 0), ("I tend to be a people-pleaser", -5), ("I never put my needs first", -9)]},
        {"question": "How comfortable are you with your own appearance?", "options": [("Very comfortable", 9), ("Comfortable enough", 5), ("Neutral", 0), ("Uncomfortable", -5), ("Very uncomfortable", -9)]},
        {"question": "Do you celebrate your own achievements, big or small?", "options": [("Yes, always", 9), ("Sometimes", 5), ("Rarely", 0), ("I tend to downplay them", -5), ("I feel I haven't achieved anything", -9)]},
        {"question": "Do you believe you can handle future challenges?", "options": [("Yes, I'm confident", 9), ("I'm hopeful", 5), ("I'm worried", 0), ("I doubt my ability", -5), ("I feel doomed to fail", -9)]}
    ],
    "Energy": [
        {"question": "How would you describe your typical energy levels throughout the day?", "options": [("Very high", 8), ("High", 4), ("Moderate", 0), ("Low", -4), ("Very low", -8)]},
        {"question": "Do you wake up with energy for the day ahead?", "options": [("Yes, ready to go!", 8), ("Usually", 4), ("It takes a while to get going", 0), ("I wake up tired", -4), ("I wake up exhausted", -8)]},
        {"question": "Do you experience a significant 'afternoon slump'?", "options": [("No, my energy is stable", 8), ("Sometimes", 4), ("Yes, most days", 0), ("Yes, it's a major struggle", -4), ("I feel slumped all day", -8)]},
        {"question": "How is your mental energy and focus?", "options": [("Sharp and focused", 8), ("Pretty good", 4), ("It comes and goes", 0), ("Often foggy and unfocused", -4), ("I can't concentrate at all", -8)]},
        {"question": "What is your reliance on caffeine or sugar for energy?", "options": [("None, I have natural energy", 8), ("I have one or two a day", 4), ("I need it to function", 0), ("I consume a lot", -4), ("I'm constantly using it", -8)]},
        {"question": "Do you have enough energy for both your obligations and your hobbies?", "options": [("Yes, plenty", 8), ("Usually", 4), ("Only enough for obligations", 0), ("Barely enough for obligations", -4), ("Not enough for either", -8)]},
        {"question": "How does your diet affect your energy?", "options": [("It fuels me well", 8), ("It's okay", 4), ("I notice I crash after certain foods", 0), ("My diet likely makes me tired", -4), ("I don't pay attention to my diet", -8)]},
        {"question": "How does your emotional state affect your physical energy?", "options": [("Not much", 8), ("Sometimes it does", 4), ("Stress or sadness drains me", 0), ("My emotions completely dictate my energy", -4), ("I feel emotionally and physically drained", -8)]},
        {"question": "How much 'get up and go' do you have for spontaneous activities?", "options": [("A lot!", 8), ("A fair amount", 4), ("Not much", 0), ("Very little", -4), ("None at all", -8)]},
        {"question": "Do you feel you are getting enough rest (aside from sleep)?", "options": [("Yes, I make time for downtime", 8), ("I try to", 4), ("Not really", 0), ("I feel constantly 'on'", -4), ("I'm burnt out", -8)]},
        {"question": "How has your energy been compared to six months ago?", "options": [("It's much better", 8), ("It's about the same", 4), ("It's a little worse", 0), ("It's much worse", -4), ("It has plummeted", -8)]}
    ],
    "Outlook": [
        {"question": "How optimistic are you about your future?", "options": [("Very optimistic", 10), ("Optimistic", 5), ("Neutral", 0), ("Pessimistic", -5), ("Very pessimistic", -10)]},
        {"question": "Do you feel you have clear goals you are working towards?", "options": [("Yes, very clear goals", 10), ("I have some general goals", 5), ("My goals are a bit fuzzy", 0), ("I don't have any goals", -5), ("I feel aimless", -10)]},
        {"question": "Do you believe that good things will happen to you?", "options": [("Yes, I expect them to", 10), ("I'm hopeful", 5), ("I'm not sure", 0), ("I tend to expect the worst", -5), ("I feel nothing good will ever happen", -10)]},
        {"question": "How much do you look forward to the coming weeks and months?", "options": [("A great deal", 10), ("A fair amount", 5), ("I'm neutral about it", 0), ("I'm not looking forward to it", -5), ("I'm dreading it", -10)]},
        {"question": "Do you see challenges as opportunities for growth?", "options": [("Yes, always", 10), ("Sometimes", 5), ("Rarely", 0), ("No, I see them as threats", -5), ("Challenges just confirm my failures", -10)]},
        {"question": "Do you feel a sense of purpose in your life?", "options": [("Yes, a strong sense", 10), ("I think so", 5), ("I'm searching for it", 0), ("I don't feel I have one", -5), ("I feel my life is without purpose", -10)]},
        {"question": "How much do you dwell on past mistakes or regrets?", "options": [("Very little, I've moved on", 10), ("I reflect, but don't dwell", 5), ("I dwell on them sometimes", 0), ("I dwell on them a lot", -5), ("I am haunted by them", -10)]},
        {"question": "Do you feel excited about the possibilities the future holds?", "options": [("Very excited!", 10), ("Somewhat excited", 5), ("Neutral", 0), ("Apprehensive", -5), ("Fearful", -10)]},
        {"question": "Do you believe you have the ability to change your life for the better?", "options": [("Yes, absolutely", 10), ("I think so", 5), ("I'm not sure", 0), ("I doubt it", -5), ("No, I feel powerless", -10)]},
        {"question": "How often do you think 'what if' in a negative way?", "options": [("Rarely", 10), ("Sometimes", 5), ("Often", 0), ("Very often", -5), ("It's a constant thought pattern", -10)]},
        {"question": "Do you feel that your best days are ahead of you or behind you?", "options": [("Ahead of me!", 10), ("Hopefully ahead", 5), ("I'm not sure", 0), ("Probably behind me", -5), ("Definitely behind me", -10)]}
    ]
}

PASTEL_COLORS = [
    '#FFADAD', '#FFD6A5', '#FDFFB6', '#CAFFBF', '#9BF6FF', 
    '#A0C4FF', '#BDB2FF', '#FFC6FF'
]

def get_script_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

class MentalHealthQuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mental Health Quiz")
        self.geometry("600x700")

        self.font_family = ("Segoe UI", "Calibri", "Arial")
        self.font_normal = (self.font_family[0], 11)
        self.font_bold = (self.font_family[0], 11, "bold")
        self.font_title = (self.font_family[0], 26, "bold")
        self.font_button = (self.font_family[0], 12, "bold")
        self.font_question = (self.font_family[0], 14, "bold")
        self.font_results_score = (self.font_family[0], 16, "bold")
        self.font_results_assessment = (self.font_family[0], 14)
        self.font_history_entry = (self.font_family[0], 10)

        self.username = tk.StringVar()

        self._container = tk.Frame(self)
        self._container.pack(expand=True, fill="both")

        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.style.configure("TFrame", background="#F0F0F0")
        self.style.configure("TLabel", background="#F0F0F0", font=self.font_normal)
        self.style.configure("Title.TLabel", font=self.font_title)
        self.style.configure("TRadiobutton", background="#F0F0F0", font=self.font_normal)

        self.style.configure("Modern.TButton", 
            font=self.font_button, padding=10, background='#FFFFFF',
            foreground='#333333', borderwidth=1, relief='solid', bordercolor='#CCCCCC'
        )
        self.style.map("Modern.TButton",
            background=[('active', '#F0F0F0')], relief=[('pressed', 'sunken')]
        )

        self.quiz_questions = []
        self.current_question_index = 0
        self.score = 0
        self.category_scores = {}
        self.selected_answer = tk.IntVar(value=-1)
        self.current_frame_name = None
        self.active_color = "#F0F0F0"

        self.frames = {}
        for F in (StartPage, QuizPage, ResultsPage, HistoryPage):
            page_name = F.__name__
            frame = F(parent=self._container, controller=self)
            self.frames[page_name] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame("StartPage", initial=True)

    def show_instructions(self):
        filepath = os.path.join(get_script_dir(), 'instructions.txt')
        try:
            if not os.path.exists(filepath):
                messagebox.showerror("Error", "Could not find instructions.txt.")
                return
            if platform.system() == 'Darwin':
                subprocess.call(('open', filepath))
            elif platform.system() == 'Windows':
                os.startfile(filepath)
            else:
                subprocess.call(('xdg-open', filepath))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_frame(self, page_name, initial=False):
        if self.current_frame_name == page_name:
            return
        new_color = random.choice(PASTEL_COLORS)
        self.update_colors(new_color)
        new_frame = self.frames[page_name]
        if page_name == "HistoryPage":
            new_frame.load_history()
        if initial or self.current_frame_name is None:
            self.current_frame_name = page_name
            new_frame.tkraise()
            return
        old_frame = self.frames[self.current_frame_name]
        self.current_frame_name = page_name
        self.animate_page_transition(old_frame, new_frame)

    def animate_page_transition(self, old_frame, new_frame):
        width = self.winfo_width()
        duration = 700
        steps = 100
        new_frame.place(x=width, y=0, relwidth=1, relheight=1)
        new_frame.tkraise()

        def ease_out_quad(n): return 1 - (1 - n) ** 2
        def animate_step(step):
            progress = step / steps
            eased = ease_out_quad(progress)
            old_x, new_x = -int(width * eased), width - int(width * eased)
            old_frame.place(x=old_x, y=0, relwidth=1, relheight=1)
            new_frame.place(x=new_x, y=0, relwidth=1, relheight=1)
            if step < steps:
                self.after(duration // steps, animate_step, step + 1)
            else:
                new_frame.place(x=0, y=0, relwidth=1, relheight=1)
        animate_step(1)

    def update_colors(self, new_color):
        self.active_color = new_color
        self.configure(bg=new_color)
        self.style.configure("TFrame", background=new_color)
        self.style.configure("TLabel", background=new_color)
        self.style.configure("Title.TLabel", background=new_color)
        self.style.configure("TRadiobutton", background=new_color)
        results_page = self.frames.get("ResultsPage")
        if results_page and results_page.canvas_widget:
            results_page.create_bar_graph(self.category_scores)
        history_page = self.frames.get("HistoryPage")
        if history_page:
            history_page.canvas.configure(bg=new_color)

    def start_quiz(self):
        user_name = self.username.get().strip()
        if not user_name:
            messagebox.showerror("Name Required", "Please enter your name to start.")
            return
        self.current_question_index = 0
        self.score = 0
        self.category_scores = {}
        self.quiz_questions = self._generate_quiz()
        self.frames["QuizPage"].display_question()
        self.show_frame("QuizPage")

    def _generate_quiz(self):
        quiz = []
        for category, questions in QUESTIONS_BANK.items():
            chosen = random.choice(questions)
            chosen['category'] = category
            quiz.append(chosen)
        random.shuffle(quiz)
        return quiz

    def show_results(self):
        assessment, recommendations = self.get_assessment()
        self.frames["ResultsPage"].update_results(self.score, assessment, recommendations, self.category_scores)
        self.show_frame("ResultsPage")
        self.save_results_to_db(self.score, assessment, recommendations)

    def get_assessment(self):
        if self.score > 50:
            return ("Excellent Mental Well-being", "You're doing great! Keep it up.")
        elif self.score > 20:
            return ("Good Mental Well-being", "Solid foundation, consider new habits.")
        elif self.score > -10:
            return ("Average Mental Well-being", "Focus on consistency in habits.")
        elif self.score > -40:
            return ("Needs Improvement", "You might be struggling, talk to someone.")
        else:
            return ("Consider Seeking Support", "It’s strongly recommended to see a professional.")

    def save_results_to_db(self, score, assessment, recommendations):
        cnx, cursor = None, None
        try:
            cnx = mysql.connector.connect(**MYSQL_CONFIG)
            cursor = cnx.cursor()
            query = ("INSERT INTO quiz_history (username, score, assessment, recommendations) "
                     "VALUES (%s, %s, %s, %s)")
            data_tuple = (self.username.get().strip(), score, assessment, recommendations)
            cursor.execute(query, data_tuple)
            cnx.commit()
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to save results: {err}")
        finally:
            if cursor: cursor.close()
            if cnx and cnx.is_connected(): cnx.close()

class BasePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="TFrame")
        self.controller = controller
        self.content_frame = ttk.Frame(self, style="TFrame")
        self.content_frame.pack(expand=True, fill='both')

class StartPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        main_content = ttk.Frame(self.content_frame, style="TFrame")
        main_content.pack(expand=True)

        title_label = ttk.Label(main_content, text="Mental Health Quiz", style="Title.TLabel")
        title_label.pack(pady=(20, 20), padx=20)
        
        name_label = ttk.Label(main_content, text="Enter Your Name:", font=controller.font_bold)
        name_label.pack()
        
        name_entry = ttk.Entry(main_content, textvariable=controller.username, font=controller.font_normal, width=30, justify='center')
        name_entry.pack(pady=(5, 25))

        button_frame = ttk.Frame(main_content, style="TFrame")
        button_frame.pack(padx=100, fill='x')

        start_button = ttk.Button(button_frame, text="Start Quiz", style="Modern.TButton", command=self.controller.start_quiz)
        start_button.pack(pady=5, fill='x')

        history_button = ttk.Button(button_frame, text="Health History", style="Modern.TButton", command=lambda: controller.show_frame("HistoryPage"))
        history_button.pack(pady=5, fill='x')
        
        instructions_button = ttk.Button(button_frame, text="How to Use", style="Modern.TButton", command=controller.show_instructions)
        instructions_button.pack(pady=5, fill='x')
        
        exit_button = ttk.Button(button_frame, text="Exit", style="Modern.TButton", command=self.controller.destroy)
        exit_button.pack(pady=(5, 20), fill='x')


class QuizPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.question_container = ttk.Frame(self.content_frame, style="TFrame")
        
        self.question_label = ttk.Label(self.question_container, text="", font=controller.font_question, wraplength=500, justify="center")
        self.question_label.pack(pady=(40, 20), padx=20)

        self.options_frame = ttk.Frame(self.question_container, style="TFrame")
        self.options_frame.pack(pady=20, padx=40, anchor='w')
        
        button_container = ttk.Frame(self.question_container, style="TFrame")
        button_container.pack(pady=20, padx=60, fill='x')

        self.next_button = ttk.Button(button_container, text="Next", style="Modern.TButton", command=self.process_and_transition)
        self.next_button.pack(side='left', expand=True, padx=(0, 5), fill='x')
        
        self.skip_button = ttk.Button(button_container, text="Skip", style="Modern.TButton", command=self.skip_question)
        self.skip_button.pack(side='left', expand=True, padx=(5, 0), fill='x')

    def skip_question(self):
        self._next_step(0)

    def _next_step(self, score_to_add):
        q_data = self.controller.quiz_questions[self.controller.current_question_index]
        category = q_data['category']
        
        self.controller.score += score_to_add
        self.controller.category_scores[category] = {'score': score_to_add, 'options': q_data['options']}
        
        self.controller.current_question_index += 1
        
        if self.controller.current_question_index < len(self.controller.quiz_questions):
            self.animate_question_transition()
        else:
            self.controller.show_results()

    def process_and_transition(self):
        try:
            if self.controller.selected_answer.get() == -1:
                messagebox.showerror("Error", "Please select an answer before proceeding.")
                return
            
            q_data = self.controller.quiz_questions[self.controller.current_question_index]
            score_to_add = q_data['options'][self.controller.selected_answer.get()][1]
            self._next_step(score_to_add)

        except (IndexError, tk.TclError):
            messagebox.showerror("Error", "An unexpected error occurred while processing your answer.")
            return

    def animate_question_transition(self):
        width = self.winfo_width()
        duration = 500
        steps = 70

        def ease_out_quad(n):
            return 1 - (1 - n) ** 2

        def animate_out_step(step):
            progress = step / steps
            eased_progress = ease_out_quad(progress)
            
            new_relx = 0.5 - (1.0 * eased_progress)
            self.question_container.place(relx=new_relx, rely=0.5, anchor='center')

            if step < steps:
                self.after(duration // steps, animate_out_step, step + 1)
            else:
                self.display_question(is_animating=True)
                self.question_container.place(relx=1.5, rely=0.5, anchor='center')
                animate_in_step(1)
        
        def animate_in_step(step):
            progress = step / steps
            eased_progress = ease_out_quad(progress)

            new_relx = 1.5 - (1.0 * eased_progress)
            self.question_container.place(relx=new_relx, rely=0.5, anchor='center')

            if step < steps:
                self.after(duration // steps, animate_in_step, step + 1)
            else:
                self.question_container.place(relx=0.5, rely=0.5, anchor='center')

        animate_out_step(1)

    def display_question(self, is_animating=False):
        if not is_animating:
            self.question_container.place(relx=0.5, rely=0.5, anchor='center')

        for widget in self.options_frame.winfo_children():
            widget.destroy()

        self.controller.selected_answer.set(-1) 
        
        questionData = self.controller.quiz_questions[self.controller.current_question_index]
        self.question_label.config(text=questionData["question"])

        for i, option in enumerate(questionData["options"]):
            rb = ttk.Radiobutton(self.options_frame, text=option[0], variable=self.controller.selected_answer, value=i)
            rb.pack(anchor="w", pady=5)

        if self.controller.current_question_index == len(self.controller.quiz_questions) - 1:
            self.next_button.config(text="Finish & See Results")
            self.skip_button.config(state="disabled")
        else:
            self.next_button.config(text="Next")
            self.skip_button.config(state="normal")


class ResultsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.title_label = ttk.Label(self.content_frame, text="Your Results", style="Title.TLabel")
        self.title_label.pack(pady=10)
        
        self.score_label = ttk.Label(self.content_frame, text="", font=controller.font_results_score)
        self.score_label.pack(pady=5)

        self.assessment_label = ttk.Label(self.content_frame, text="", font=controller.font_results_assessment)
        self.assessment_label.pack(pady=5)
        
        self.graph_frame = ttk.Frame(self.content_frame, style="TFrame")
        self.graph_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.canvas_widget = None

        self.recs_title_label = ttk.Label(self.content_frame, text="Recommendations:", font=controller.font_bold)
        self.recs_title_label.pack(pady=5)

        self.recs_label = ttk.Label(self.content_frame, text="", wraplength=500, justify="center")
        self.recs_label.pack(pady=5, padx=20)

        home_button = ttk.Button(self.content_frame, text="Back to Home", style="Modern.TButton", command=lambda: controller.show_frame("StartPage"))
        home_button.pack(pady=(10,20), padx=100, fill='x')

    def update_results(self, score, assessment, recommendations, category_scores):
        self.score_label.config(text=f"Final Score: {score}")
        self.assessment_label.config(text=assessment)
        self.recs_label.config(text=recommendations)
        self.create_bar_graph(category_scores)

    def create_bar_graph(self, category_scores):
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()

        categories, normalized_scores = list(category_scores.keys()), []
        for cat in categories:
            data, actual_score = category_scores[cat], category_scores[cat]['score']
            score_values = [opt[1] for opt in data['options']]
            min_score, max_score = min(score_values), max(score_values)
            
            if (max_score - min_score) == 0:
                norm_score = 100 if actual_score >= 0 else 0
            else:
                norm_score = ((actual_score - min_score) / (max_score - min_score)) * 100
            normalized_scores.append(norm_score)

        fig = Figure(figsize=(5, 3), dpi=100)
        fig.patch.set_alpha(0)
        ax = fig.add_subplot(111)
        ax.patch.set_alpha(0)
        
        bar_colors = [random.choice(PASTEL_COLORS) for _ in categories]
        ax.bar(categories, normalized_scores, color=bar_colors)
        
        ax.set_ylabel('Score (0-100)', fontname=self.controller.font_family[0])
        ax.set_title('Category Breakdown', fontname=self.controller.font_family[0])
        ax.set_ylim(0, 100)
        
        for spine in ax.spines.values(): spine.set_edgecolor('#555555')
        ax.tick_params(axis='x', colors='#333333', labelrotation=30)
        ax.tick_params(axis='y', colors='#333333')
        ax.yaxis.label.set_color('#333333')
        ax.title.set_color('#333333')
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas_widget = canvas
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class HistoryPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        title_label = ttk.Label(self.content_frame, text="Quiz History", style="Title.TLabel")
        title_label.pack(pady=(20, 10))
        container = ttk.Frame(self.content_frame)
        container.pack(fill="both", expand=True, padx=20, pady=10)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style="TFrame")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        button_frame = ttk.Frame(self.content_frame, style="TFrame")
        button_frame.pack(pady=(10, 20), padx=100, fill='x')
        home_button = ttk.Button(button_frame, text="Back to Home", style="Modern.TButton", command=lambda: controller.show_frame("StartPage"))
        home_button.pack(pady=5, fill='x')
        export_button = ttk.Button(button_frame, text="Export to CSV", style="Modern.TButton", command=self.export_to_csv)
        export_button.pack(pady=5, fill='x')
        clear_button = ttk.Button(button_frame, text="Clear History", style="Modern.TButton", command=self.clear_history)
        clear_button.pack(pady=5, fill='x')

    def export_to_csv(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not filepath:
            return
        cnx, cursor = None, None
        try:
            cnx = mysql.connector.connect(**MYSQL_CONFIG)
            cursor = cnx.cursor()
            cursor.execute("""
                SELECT username,
                       DATE_FORMAT(test_date, '%Y-%m-%d %H:%i:%s') AS test_date,
                       score, assessment, recommendations
                FROM quiz_history
                ORDER BY test_date DESC
            """)
            rows = cursor.fetchall()
            headers = [desc[0].capitalize() for desc in cursor.description]
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)
            messagebox.showinfo("Success", f"History exported to:\n{filepath}")
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to export: {err}")
        finally:
            if cursor: cursor.close()
            if cnx and cnx.is_connected(): cnx.close()

    def clear_history(self):
        if not messagebox.askyesno("Confirm", "Are you sure you want to permanently delete all quiz history?"):
            return
        cnx, cursor = None, None
        try:
            cnx = mysql.connector.connect(**MYSQL_CONFIG)
            cursor = cnx.cursor()
            cursor.execute("TRUNCATE TABLE quiz_history")
            cnx.commit()
            self.load_history()
        except Error as err:
            messagebox.showerror("Database Error", f"Failed to clear history: {err}")
        finally:
            if cursor: cursor.close()
            if cnx and cnx.is_connected(): cnx.close()

    def load_history(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.canvas.configure(bg=self.controller.active_color)
        self.scrollable_frame.configure(style="TFrame")
        cnx, cursor = None, None
        try:
            cnx = mysql.connector.connect(**MYSQL_CONFIG)
            cursor = cnx.cursor()
            cursor.execute("""
                SELECT username,
                       DATE_FORMAT(test_date, '%Y-%m-%d %H:%i:%s') AS test_date,
                       score, assessment
                FROM quiz_history
                ORDER BY test_date DESC
            """)
            results = cursor.fetchall()
            if not results:
                ttk.Label(self.scrollable_frame, text="No history found.").pack(pady=20)
                return
            for username, test_date, score, assessment in results:
                entry_text = f"User: {username}\nDate: {test_date}  |  Score: {score}  |  Result: {assessment}"
                ttk.Label(self.scrollable_frame, text=entry_text, justify="left", wraplength=450, font=self.controller.font_history_entry).pack(pady=8, padx=10, anchor='w')
                ttk.Separator(self.scrollable_frame, orient='horizontal').pack(fill='x', padx=10)
        except Error as err:
            ttk.Label(self.scrollable_frame, text=f"Database Error: {err}").pack(pady=20, padx=10)
        finally:
            if cursor: cursor.close()
            if cnx and cnx.is_connected(): cnx.close()

if __name__ == "__main__":
    app = MentalHealthQuizApp()
    app.mainloop()
