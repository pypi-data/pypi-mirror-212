from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import pandas as pd

class Wafpd:
    commands = set(["sort", "filter", "group", "rank", "data", "analyse", "save", "all", "clear",
                    "information", "fill", "split", "join", "add", "find", "average", "max", "min", "value",
                    "odd", "even", "or", "select", "create", "into", "database", "table", "relate", "in",
                    "between", "alter", "int", "varchar", "primary", "update", "from", "where", "on", "delete",
                    "commit", "plot", "ranked"])
    ignore_commands = set(["give", "me", "i", "want", "to", "it", "and"])

    def word_analyzer(self, interface_input):
        self.interface_input = interface_input
        picfi = word_tokenize(self.interface_input)
        common_elements = set(picfi) & self.commands - self.ignore_commands
    
        
        # sort data , max and min values, unique value
        # try:
        #     self.max_value_of_something = self.interface_input.find("max") + 1
        # except ValueError:
        #     self.max_value_of_something = ""
        # try:
        #     self.max_value_of_something = self.interface_input.find("max") + 1
        # except ValueError:
        #     self.max_value_of_something = ""
        try:
            self.unique_value_of_something = self.interface_input.find("unique") + 1
        except ValueError:
            self.unique_value_of_something = ""
        try:
            self.unique = self.interface_input.find("unique")
        except ValueError:
            self.unique = ""
        
        try:
            self.max_value_of_something = self.interface_input.find("max") + 1
        except ValueError:
            self.max_value_of_something = ""

        try:
            self.min_value_of_something = self.interface_input.find("min") + 1
        except ValueError:
            self.max_value_of_something = ""

        try:
            self.database_show = interface_input.find("show me database")
        except ValueError:
            self.database_show = ""
            print("error")
        
        try:
            act_word1 = picfi.index("average") + 1
            self.action_word = picfi[act_word1]
        except ValueError:
            self.action_word = ""

        try:
            act_word2 = picfi.index("first") + 1
            self.number_of_limit_from_head = int(picfi[act_word2])
        except ValueError:
            self.number_of_limit_from_head = 0

        try:
            act_word3 = picfi.index("last") + 1
            self.number_of_limit_from_tail = int(picfi[act_word3])
        except ValueError:
            self.number_of_limit_from_tail = 0

    def data_analyze(self, datatype):
        self.dt_type = datatype.split(".")

        # working on csv file
        if "csv" in self.dt_type:
            scale = pd.read_csv(datatype)
            if "describe" in self.interface_input:
                return scale.describe()
            elif "show me database" in self.interface_input: 
                return scale
            elif f"first {self.number_of_limit_from_head}" in self.interface_input:
                return scale.head(self.number_of_limit_from_head)
            elif f"last {self.number_of_limit_from_tail}" in self.interface_input:
                return scale.tail(self.number_of_limit_from_tail)
            elif "average" in self.interface_input:
               return scale[self.action_word].mean()
            elif "max" in self.interface_input:
                return scale.max(self.max_value_of_something)
            elif "min" in self.interface_input:
               return scale.min(self.min_value_of_something)
            elif "unique" in self.interface_input:
              return scale.unique(self.unique)
            elif "unique" in self.interface_input and self.unique in self.interface_input:
                return scale[self.unique].unique()

        # working on excel file
        elif "excel" in self.dt_type:
            scale = pd.read_excel(datatype)
            if "describe" in self.interface_input:
                return scale.describe()
            elif "show me database" in self.interface_input: 
                return scale
            elif f"first {self.number_of_limit_from_head}" in self.interface_input:
                return scale.head(self.number_of_limit_from_head)
            elif f"last {self.number_of_limit_from_tail}" in self.interface_input:
                return scale.tail(self.number_of_limit_from_tail)
            elif "average" in self.interface_input:
               return scale[self.action_word].mean()
            elif "max" in self.interface_input:
                return scale.max(self.max_value_of_something)
            elif "min" in self.interface_input:
               return scale.min(self.min_value_of_something)
            elif "unique" in self.interface_input:
              return scale.unique()
            elif "unique" in self.interface_input and self.unique in self.interface_input:
                return scale[self.unique].unique()
        
        # working on json file
        elif "json" in self.dt_type:
            scale = pd.read_json(datatype)
            if "describe" in self.interface_input:
                return scale.describe()
            elif "show me database" in self.interface_input: 
                return scale
            elif f"first {self.number_of_limit_from_head}" in self.interface_input:
                return scale.head(self.number_of_limit_from_head)
            elif f"last {self.number_of_limit_from_tail}" in self.interface_input:
                return scale.tail(self.number_of_limit_from_tail)
            elif "average" in self.interface_input:
               return scale[self.action_word].mean()
            elif "max" in self.interface_input:
                return scale.max(self.max_value_of_something)
            elif "min" in self.interface_input:
               return scale.min(self.min_value_of_something)
            elif "unique" in self.interface_input:
              return scale.unique()
            elif "unique" in self.interface_input and self.unique in self.interface_input:
                return scale[self.unique].unique()
            
        # working on txt file
        elif "txt" in self.dt_type:
            scale = pd.read_txt(datatype)
            if "describe" in self.interface_input:
                return scale.describe()
            elif "show me database" in self.interface_input: 
                return scale
            elif f"first {self.number_of_limit_from_head}" in self.interface_input:
                return scale.head(self.number_of_limit_from_head)
            elif f"last {self.number_of_limit_from_tail}" in self.interface_input:
                return scale.tail(self.number_of_limit_from_tail)
            elif "average" in self.interface_input:
               return scale[self.action_word].mean()
            elif "max" in self.interface_input:
                return scale.max(self.max_value_of_something)
            elif "min" in self.interface_input:
               return scale.min(self.min_value_of_something)
            elif "unique" in self.interface_input:
              return scale.unique()
            elif "unique" in self.interface_input and self.unique in self.interface_input:
                return scale[self.unique].unique()
            

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



caler = Wafpd()
generate_plot = caler.generate_plot
word_analyzer = caler.word_analyzer
data_analyze = caler.data_analyze
