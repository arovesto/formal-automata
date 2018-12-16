from telegram.ext import Updater, CommandHandler

from regular_parser import parse_regular_expression
from min_dfa import MinDFA
from dfa import DFA
from no_epsilon_nfa import NoEpsilonNFA



def automata(bot, update):
    command = update.message.text.split()
    if len(command) != 2:
        update.message.reply_text("Прости( по-моему не хватает регулярного выражения мб попробуешь ещё раз?")
        return
    regular = update.message.text.split()[1]
    print(update.message.from_user.username if update.message.from_user.username else update.message.from_user.id,
          regular, end=" ")
    try:
        regular = parse_regular_expression(regular)
    except IndexError:
        update.message.reply_text('Прости( я как-то не очень поняла, когда ты написала: "' + regular
                                  + '" мб попробуешь ещё раз?')
        print("BAD REGULAR")
        return
    if len(regular) == 0:
        update.message.reply_text("Ну ты конечно приколист, это ж пустая регулярка")
        print("EMPTY REGULAR")
        return
    try:
        nfa = NoEpsilonNFA(regular)
        dfa = DFA(regular)
        full_dfa = DFA(regular, True)
        min_dfa = MinDFA(regular)
    except IndexError:
        update.message.reply_text('Прости( я как-то не очень поняла, когда ты написала: "' + regular
                                  + '" мб попробуешь ещё раз?')
        print("BAD REGULAR")
        return
    update.message.reply_text("Вот, держи, для тебя я построила автоматы, всех видов. Если что, они всегда начинаются"
                              "в нуле, а где они заканчиваются, я написала)")
    update.message.reply_text("Это твой НКА без эпсилон переходов\n" + str(nfa))
    update.message.reply_text("А это твой ДКА\n" + str(dfa))
    update.message.reply_text("Держи теперь ПДКА\n" + str(full_dfa))
    update.message.reply_text("Ну и МПДКА конечно тоже))\n" + str(min_dfa))
    print("OK")
    return


def start(bot, update):
    update.message.reply_text("Привет, я Ира. Готова помочь вам с вашей регуляркой, можете ввести команду"
                              " /automata <regular> где <regular> это регулярное выражение, в обычной нотации"
                              "без плюсов Клини только)). Если что, епсилон это E")
    return


def main():
    # TODO implement buttons to chose variant "enter regular" or anything
    # TODO go to server, mb www.pythonanywhere.com will do
    # TODO maybe it's time to go to contest grammars and Erly algorithm?
    # TODO it should have it's own button then
    # TODO sounds like context free grammar to push down automata
    updater = Updater("654073755:AAF3FnUsnrkchA9VYrxkl3kTbpAQ9wL1dxI")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("automata", automata))
    updater.start_polling()
    print("Bot is started")
    updater.idle()


if __name__ == "__main__":
    main()
