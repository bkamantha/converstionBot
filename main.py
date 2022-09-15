import json

logics = json.load(open('logics.json'))

user_input = True
logic_unit = 0
phrase = ""
prompt = logics[0][1]['hello']


# navigate relavent response in next logic unit
def logic_finder(navigate):
    global user_input, logic_unit

    for logic in range(0, len(logics)):
        user_input = False
        try:
            logics[logic][1][navigate]
            logic_unit = logic
            return navigate
        except:
            pass


# convert user str input to in for update recommondation score
def value_converter(phrase):
    global score
    try:
        score = int(phrase)
        if 0 <= score <= 10:
            if score < 8:
                strphrase = "0-8"
            else:
                strphrase = "9-10"
        return strphrase
    except:
        # print("error")
        return phrase


# update system values(value /tag) according to user action
def value_updater(phrase):
    try:
        key = list(logics[logic_unit][3][phrase].keys())[0]
        value = list(logics[logic_unit][3][phrase].values())[0]

        if key == "recommendation_score":
            value = score
        else:
            value = list(logics[logic_unit][3][phrase].values())[0]

        logics[logic_unit][2][key] = value

    except:
        # print("error")
        pass


# capture null input and redirect user
def null_finder(phrase):
    if logics[logic_unit][2]["repeat"] == False:

        logics[logic_unit][2]["repeat"] = 'True'
        navigate = logics[logic_unit][0]['NULL']['True']
        prompt = logics[logic_unit][1][navigate]
        return prompt

    else:
        navigate = logics[logic_unit][0]['NULL']['False']
        nextnavigate = logic_finder(navigate)
        logics[logic_unit][2]["wrong_time"] = 'True'
        return nextnavigate


# handel hello logic actions
def hello_logic(phrase):
    global logic_unit, prompt, nextnavigate

    value_updater(phrase)

    if not phrase:
        prompt = null_finder(phrase)
        return prompt

    try:
        navigate = logics[0][0][phrase]
        prompt = logics[0][1][navigate]
        return prompt

    except:
        navigate = logics[0][0][phrase]
        nextnavigate = logic_finder(navigate)
        return nextnavigate


# handel main logic actions
def main_logic(phrase):
    global logic_unit, prompt, user_input

    if not user_input:
        user_input = True
        prompt = logics[1][1][phrase]
        return prompt

    if not phrase:
        prompt = null_finder(phrase)
        return prompt

    phrase = value_converter(phrase)

    value_updater(phrase)

    if phrase == "DEFAULT":
        if logics[1][2]["repeat"] == False:
            navigate = logics[1][0]['DEFAULT']['True']
            prompt = logics[1][1][navigate]
            return prompt

        else:
            navigate = logics[1][0]['DEFAULT']['False']
            logic_finder(navigate)
            return prompt
    else:
        try:
            navigate = logics[1][0][phrase]
            prompt = logics[1][1][navigate]
            return prompt

        except:
            navigate = logics[1][0][phrase]
            nextnavigate = logic_finder(navigate)
            return nextnavigate


# handel hangup logic actions
def hangup_logic(phrase):
    print(phrase)
    value_updater(phrase)
    prompt = logics[2][1][phrase]
    print("Anne= > "+prompt)


# handel forward logic actions
def forward_logic(phrase):
    value_updater(phrase)
    prompt = logics[3][1][phrase]
    print("Anne= > "+prompt)


# main converstional loop trgger only user start converstion
while phrase != "End":
    try:
        if user_input:
            phrase = input(str(f"Anne => {prompt}: "))

        if logic_unit == 0:
            prompt = hello_logic(phrase)

        elif logic_unit == 1:
            if user_input:
                prompt = main_logic(phrase)
            else:
                prompt = main_logic(prompt)

        elif logic_unit == 2:
            prompt = hangup_logic(prompt)
            phrase = "End"

        elif logic_unit == 3:
            forward_logic(prompt)
            phrase = "End"

    except:

        print("Anne => Invalid Response Enter Valid Response or type 'End' to Quit")
        # end converstion if invaild response user enterd once remove following varible system wait until user enter valid response.
        # phrase = "End"


print("\n ..............Result.................... \n")

print(logics[0][2])
print(logics[1][2])
print(logics[2][2])
print(logics[3][2])


print("\n ..............Ended.................... \n")
