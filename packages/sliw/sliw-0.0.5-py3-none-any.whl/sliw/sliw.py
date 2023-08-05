from nltk.tokenize import word_tokenize
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

caler = Wafpd()
word_analyzer = caler.word_analyzer
data_analyze = caler.data_analyze
