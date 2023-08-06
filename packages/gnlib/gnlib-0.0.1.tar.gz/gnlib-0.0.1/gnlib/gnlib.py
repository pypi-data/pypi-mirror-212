from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import pandas as pd
import speech_recognition as sr
import pyttsx3

# def text_to_speech(text):
    #     engine = pyttsx3.init()
    #     engine.say(text)
    #     engine.runAndWait()

#  text_to_speech()

class Wafpd:
    commands = set(["sort", "filter", "group", "rank", "data", "analyse", "save", "all", "clear",
                    "information", "fill", "split", "join", "add", "find", "average", "max", "min", "value",
                    "odd", "even", "or", "select", "create", "into", "database", "table", "relate", "in",
                    "between", "alter", "int", "varchar", "primary", "update", "from", "where", "on", "delete",
                    "commit", "plot", "ranked"])
    ignore_commands = set(["give", "me", "i", "want", "to", "it", "and"])
    # Create a recognizer object
    def word_analyzer(self):
        def text_to_speech(text):
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()

        text_to_speech("hello my name is jarvis how can i asist you today?")
        # import speech_recognition as sr

        r = sr.Recognizer()

        # Capture audio from the microphone
        with sr.Microphone() as source:
            print("Say something...")
            audio = r.listen(source)

        # Perform speech recognition
        try:
            text_from_user = r.recognize_google(audio)
            print("You said:", text_from_user)
        except sr.UnknownValueError:
            print("Unable to recognize speech")
        except sr.RequestError as e:
            print("Error:", e)

        self.interface_input = text_from_user
        picfi = word_tokenize(text_from_user)
        common_elements = set(picfi) & self.commands - self.ignore_commands

        try:
            self.multyply_value_of_something = self.interface_input.find("multiplie") + 1
            self.multyply_value = self.interface_input.find("multiplie") + 2
        except ValueError:
            self.max_value_of_something = ""
        # try:
        #     self.max_value_of_something = self.interface_input.find("max") + 1
        # except ValueError:
        #     self.max_value_of_something = ""
     
        try:
            self.unique_value_of_something = self.interface_input.find("unique") + 1
        except ValueError:
            self.unique_value_of_something = ""
            # print(f"""ERROR! sintax error
            #         word_analyzer({self.interface_input}) something went wrong 
            #         try like this : word_analyzer("unique ~ column name")""")
            
        try:
            self.unique = self.interface_input.find("unique")
        except ValueError:
            self.unique = ""
            # print(f"""ERROR! sintax error
            #         word_analyzer({self.interface_input}) something went wrong 
            #         try like this : word_analyzer("~text~ unique")""") 
        
        try:
            self.max_value_of_something = self.interface_input.find("max") + 1
        except ValueError:
            self.max_value_of_something = ""
            # print(f"""ERROR! sintax error
            #         word_analyzer({self.interface_input}) something went wrong 
            #         try like this : word_analyzer("~text~ max ~ column name")""") 

        try:
            self.min_value_of_something = self.interface_input.find("min") + 1
        except ValueError:
            self.max_value_of_something = ""
            # print(f"""ERROR! sintax error
            #         word_analyzer({self.interface_input}) something went wrong 
            #         try like this : word_analyzer("~text~ min ~ column name")""")

        try:
            self.database_show = self.interface_input.find("show me database")
        except ValueError:
            self.database_show = ""
            # print(f"""ERROR! sintax error
            #         word_analyzer({self.interface_input}) something went wrong 
            #         try like this : word_analyzer("~text~ show database")""") 
        
        try:
            act_word1 = picfi.index("average") + 1
            self.action_word = picfi[act_word1]
        except ValueError:
            self.action_word = ""
            # print(f"""ERROR! sintax error
            #         word_analyzer({self.interface_input}) something went wrong 
            #         try like this : word_analyzer("~text~ average age")""") 
    

        try:
            act_word2 = picfi.index("first") + 1
            self.number_of_limit_from_head = int(picfi[act_word2])
        except ValueError:
            self.number_of_limit_from_head = 0
            # print(f"""ERROR! sintax error
            #         word_analyzer({self.interface_input}) something went wrong 
            #         try like this : word_analyzer("~text~ first 100")""") 

        try:
            act_word3 = picfi.index("last") + 1
            self.number_of_limit_from_tail = int(picfi[act_word3])
        except ValueError:
            self.number_of_limit_from_tail = 0
            # print(f"""ERROR! sintax error
            #         word_analyzer({self.interface_input}) something went wrong 
            #         try like this : word_analyzer("~text~ last 100")""")


    def data_analyze(self, datatype):
        self.dt_type = datatype.split(".")

        # working on csv file
        if "csv" in self.dt_type:
            
            scale = pd.read_csv(datatype)
            if "describe" in self.interface_input:
                def text_to_speech(text):
                    engine = pyttsx3.init()
                    engine.say(text)
                    engine.runAndWait()

                text_to_speech("this is the description of this database")
                return scale.describe()
            elif "show me database" in self.interface_input: 
                text_to_speech("this is the representation of database")
                return scale
            elif f"first {self.number_of_limit_from_head}" in self.interface_input:
                text_to_speech(f"now you are seeing fitsr {self.number_of_limit_from_head} rows")
                return scale.head(self.number_of_limit_from_head)
            elif f"last {self.number_of_limit_from_tail}" in self.interface_input:
                text_to_speech(f"now you are seeing last {self.number_of_limit_from_tail} rows")
                return scale.tail(self.number_of_limit_from_tail)
            elif "average" in self.interface_input:
                text_to_speech("this is the average value")
                return scale[self.action_word].mean()
            elif "max" in self.interface_input:
                text_to_speech("this is max value")
                return scale.max(self.max_value_of_something)
            elif "min" in self.interface_input:
                text_to_speech("this is min value")
                return scale.min(self.min_value_of_something)
            elif "unique" in self.interface_input:
                text_to_speech("there is represented all unique values")
                return scale.unique(self.unique)
            elif "unique" in self.interface_input and self.unique in self.interface_input:
                text_to_speech("there is represented all unique values")
                return scale[self.unique].unique()
            elif "multiplie" in self.interface_input and self.unique in self.interface_input:
                text_to_speech("this is the product of your operation")
                return scale[f'{self.multyply_value_of_something}'] * self.multyply_value


        # working on excel file
        elif "excel" in self.dt_type:
            scale = pd.read_excel(datatype)
            if "describe" in self.interface_input:
                def text_to_speech(text):
                    engine = pyttsx3.init()
                    engine.say(text)
                    engine.runAndWait()

                text_to_speech("this is the description of this database")
                return scale.describe()
            elif "show me database" in self.interface_input: 
                text_to_speech("this is the representation of database")
                return scale
            elif f"first {self.number_of_limit_from_head}" in self.interface_input:
                text_to_speech(f"now you are seeing fitsr {self.number_of_limit_from_head} rows")
                return scale.head(self.number_of_limit_from_head)
            elif f"last {self.number_of_limit_from_tail}" in self.interface_input:
                text_to_speech(f"now you are seeing last {self.number_of_limit_from_tail} rows")
                return scale.tail(self.number_of_limit_from_tail)
            elif "average" in self.interface_input:
                text_to_speech("this is the average value")
                return scale[self.action_word].mean()
            elif "max" in self.interface_input:
                text_to_speech("this is max value")
                return scale.max(self.max_value_of_something)
            elif "min" in self.interface_input:
                text_to_speech("this is min value")
                return scale.min(self.min_value_of_something)
            elif "unique" in self.interface_input:
                text_to_speech("there is represented all unique values")
                return scale.unique(self.unique)
            elif "unique" in self.interface_input and self.unique in self.interface_input:
                text_to_speech("there is represented all unique values")
                return scale[self.unique].unique()
            elif "multiplie" in self.interface_input and self.unique in self.interface_input:
                text_to_speech("this is the product of your operation")
                return scale[f'{self.multyply_value_of_something}'] * self.multyply_value
            
        # working on json file
        elif "json" in self.dt_type:
            scale = pd.read_json(datatype)
            if "describe" in self.interface_input:
                def text_to_speech(text):
                    engine = pyttsx3.init()
                    engine.say(text)
                    engine.runAndWait()

                text_to_speech("this is the description of this database")
                return scale.describe()
            elif "show me database" in self.interface_input: 
                text_to_speech("this is the representation of database")
                return scale
            elif f"first {self.number_of_limit_from_head}" in self.interface_input:
                text_to_speech(f"now you are seeing fitsr {self.number_of_limit_from_head} rows")
                return scale.head(self.number_of_limit_from_head)
            elif f"last {self.number_of_limit_from_tail}" in self.interface_input:
                text_to_speech(f"now you are seeing last {self.number_of_limit_from_tail} rows")
                return scale.tail(self.number_of_limit_from_tail)
            elif "average" in self.interface_input:
                text_to_speech("this is the average value")
                return scale[self.action_word].mean()
            elif "max" in self.interface_input:
                text_to_speech("this is max value")
                return scale.max(self.max_value_of_something)
            elif "min" in self.interface_input:
                text_to_speech("this is min value")
                return scale.min(self.min_value_of_something)
            elif "unique" in self.interface_input:
                text_to_speech("there is represented all unique values")
                return scale.unique(self.unique)
            elif "unique" in self.interface_input and self.unique in self.interface_input:
                text_to_speech("there is represented all unique values")
                return scale[self.unique].unique()
            elif "multiplie" in self.interface_input and self.unique in self.interface_input:
                text_to_speech("this is the product of your operation")
                return scale[f'{self.multyply_value_of_something}'] * self.multyply_value
        # working on txt file
        elif "txt" in self.dt_type:
            scale = pd.read_txt(datatype)
            if "describe" in self.interface_input:
                def text_to_speech(text):
                    engine = pyttsx3.init()
                    engine.say(text)
                    engine.runAndWait()

                text_to_speech("this is the description of this database")
                return scale.describe()
            elif "show me database" in self.interface_input: 
                text_to_speech("this is the representation of database")
                return scale
            elif f"first {self.number_of_limit_from_head}" in self.interface_input:
                text_to_speech(f"now you are seeing fitsr {self.number_of_limit_from_head} rows")
                return scale.head(self.number_of_limit_from_head)
            elif f"last {self.number_of_limit_from_tail}" in self.interface_input:
                text_to_speech(f"now you are seeing last {self.number_of_limit_from_tail} rows")
                return scale.tail(self.number_of_limit_from_tail)
            elif "average" in self.interface_input:
                text_to_speech("this is the average value")
                return scale[self.action_word].mean()
            elif "max" in self.interface_input:
                text_to_speech("this is max value")
                return scale.max(self.max_value_of_something)
            elif "min" in self.interface_input:
                text_to_speech("this is min value")
                return scale.min(self.min_value_of_something)
            elif "unique" in self.interface_input:
                text_to_speech("there is represented all unique values")
                return scale.unique(self.unique)
            elif "unique" in self.interface_input and self.unique in self.interface_input:
                text_to_speech("there is represented all unique values")
                return scale[self.unique].unique()
            elif "multiplie" in self.interface_input and self.unique in self.interface_input:
                text_to_speech("this is the product of your operation")
                return scale[f'{self.multyply_value_of_something}'] * self.multyply_value

    def generate_plot(self,datatype, plot_type):
        if plot_type == "bar":
            datatype.plot(kind="bar")
        elif plot_type == "line":
            datatype.plot(kind="line")
        elif plot_type == "hist":
            datatype.plot(kind="hist")
        else:
            print("Invalid plot type. Supported plot types: bar, line, hist")

        plt.show()

    def help_sliw(self):
        print("""this library is provided my sliw team and helps you to work with data more easyer
                 
        we have one main functions data_analyze() also there is word_analthor() finction  
        ###########################################################################################
        word_analthor() finction gets command and analyzes text and turns it into heandy for main finction
        which is data_analize this is function which is usinf well knws "pandas" library but with just 
        calling one finction and giveing command to it is better and easyer to analyse the data.

        """)

        
        

caler = Wafpd()
help = caler.help_sliw
generate_plot = caler.generate_plot
word_analyzer = caler.word_analyzer
data_analyze = caler.data_analyze
# text_to_speech = caler.text_to_speech


