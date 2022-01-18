from re import search
from requests.models import ReadTimeoutError
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import callbackcontext
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.dispatcher import Dispatcher
import finance_def
import telegram
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

############################### status #########################################
my_token = '사용자토큰'
updater = Updater(my_token, use_context=True)
bot = telegram.Bot(token=my_token)

def error(update, context):
    print(f'Update {update} caused error {context.error}')
############################ Keyboards #########################################
def main_menu_keyboard():
  keyboard = [
      [InlineKeyboardButton('시작하기', callback_data='m1'),
      InlineKeyboardButton('설명듣기', callback_data='ab_1')]]
  return InlineKeyboardMarkup(keyboard)

def about_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("뒤로가기", callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)

def first_menu_keyboard():
  keyboard = [[
      InlineKeyboardButton('상승종목', callback_data='k1_1'),
      InlineKeyboardButton('하락종목', callback_data='k1_2')],
      [
      InlineKeyboardButton('시총상위', callback_data='k1_3'),
      InlineKeyboardButton('거래상위', callback_data='k1_4')],
      [
      InlineKeyboardButton('코스피', callback_data='k1_5'),
      InlineKeyboardButton('코스닥', callback_data='k1_6')],
      [
      InlineKeyboardButton('종목검색', callback_data='k1_7'),
      InlineKeyboardButton('뉴스', callback_data='k1_8')],
      [
      InlineKeyboardButton('메인메뉴', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def first_submenu_keyboard():
    keyboard = [[
        InlineKeyboardButton('메인메뉴', callback_data='main'),
        InlineKeyboardButton('뒤로가기', callback_data='m1')]]
    return InlineKeyboardMarkup(keyboard)

def kospi_submenu_keyboard():
    keyboard = [[
        InlineKeyboardButton('코스피 지수', callback_data = 'kp_1'),
        InlineKeyboardButton('시황뉴스', callback_data='kp_2')
    ],[
        InlineKeyboardButton('메인메뉴', callback_data='main'),
        InlineKeyboardButton('뒤로가기', callback_data='m1')
    ]]
    return InlineKeyboardMarkup(keyboard)

def kospi_menu_keyboard():
    keyboard = [[
        InlineKeyboardButton('메인메뉴', callback_data='main'),
        InlineKeyboardButton('뒤로가기', callback_data='k1_5')]]
    return InlineKeyboardMarkup(keyboard)

def kosdaq_submenu_keyboard():
    keyboard = [[
        InlineKeyboardButton('코스닥 지수', callback_data = 'kd_1'),
        InlineKeyboardButton('시황뉴스', callback_data='kd_2')
    ],[
        InlineKeyboardButton('메인메뉴', callback_data='main'),
        InlineKeyboardButton('뒤로가기', callback_data='m1')
    ]]
    return InlineKeyboardMarkup(keyboard)

def kosdaq_menu_keyboard():
    keyboard = [[
        InlineKeyboardButton('메인메뉴', callback_data='main'),
        InlineKeyboardButton('뒤로가기', callback_data='k1_6')]]
    return InlineKeyboardMarkup(keyboard)

def news_menu_keyboard():
    keyboard = [[
        InlineKeyboardButton('Today News', callback_data='new_1')
    ],[
        InlineKeyboardButton('시황·전망', callback_data='new_2'),
        InlineKeyboardButton('기업·종목분석', callback_data='new_3')
    ],[
        InlineKeyboardButton('해외증시', callback_data='new_4'),
        InlineKeyboardButton('채권·선물', callback_data='new_5')
    ],[
        InlineKeyboardButton('공시·메모', callback_data='new_6'),
        InlineKeyboardButton('환율', callback_data='new_7')
    ],[
        InlineKeyboardButton('메인메뉴', callback_data='main'),
        InlineKeyboardButton('뒤로가기', callback_data='m1')
    ]]
    return InlineKeyboardMarkup(keyboard)

def news_submenu_keyboard():
    keyboard = [[
        InlineKeyboardButton('메인메뉴', callback_data = 'main'),
        InlineKeyboardButton('뒤로가기', callback_data='k1_8')
    ]]
    return InlineKeyboardMarkup(keyboard)

def search_company_keyboard():
    keyboard = [[
        InlineKeyboardButton('검색하기', callback_data = 's1_1'),
        InlineKeyboardButton('뒤로가기', callback_data = 'm1')
    ]]
    return InlineKeyboardMarkup(keyboard)

def back_keyboard():
    keyboard = [[
        InlineKeyboardButton('뒤로가기', callback_data='m1')
    ]]
    return InlineKeyboardMarkup(keyboard)
############################# MainMenu Messages #########################################
def main_menu_message():
  return 'Choose the option in main menu:'

def first_menu_message():
  return 'Choose the submenu in first menu:'

def about_menu_message():
    text = f"국내주식 봇에 오신것을 환영합니다.\n"
    text += f"현재 국내주식봇은 버튼형 챗봇으로 구현되어 있으며,\n"
    text += f"언제든지 종목검색을 하실 수 있도록 설계되어 있습니다.\n"
    text += f"단, ETF / 선물 부분은 추후 업데이트 예정입니다.\n"
    text += f"해당 챗봇에 대한 문의사항은 아래 연락처로 부탁드립니다.\n"
    text += f"이메일(wocl123@gmail.com), 텔레그램()"
    return text
############################# SubMenu Messages ########################################
def first_submenu_1_message():
    high_price = finance_def.Top_Price
    text = f"상승 종목 메뉴로 들어오셨습니다.\n\n"
    text += high_price.today_high()
    return text

def first_submenu_2_message():
    low_price = finance_def.Top_Price
    text = f"하락 종목 메뉴로 들어오셨습니다.\n\n"
    text += low_price.today_low()
    return text

def first_submenu_3_message():
    money_rank = finance_def.Top_Price
    text = f"시총 상위 메뉴로 들어오셨습니다.\n\n"
    text += money_rank.today_money()
    return text

def first_submenu_4_message():
    trade_rank = finance_def.Top_Price
    text = f"거래 상위 메뉴로 들어오셨습니다\n\n"
    text += trade_rank.today_trade()
    return text

def first_submenu_5_message():
    return '코스피 메뉴로 들어오셨습니다.'

def first_submenu_6_message():
    return '코스닥 메뉴로 들어오셨습니다.'

def first_submenu_7_message():
    return '종목검색 메뉴로 들어오셨습니다.'

def first_submenu_8_message():
    return '뉴스 메뉴로 들어오셨습니다.'

def kospi_point_message():
    kospi = finance_def.Kos
    text = f"코스피 지수 메뉴로 오셨습니다.\n\n"
    text += kospi.kospi_main()
    return text

def kospi_news_message():
    news = finance_def.Kos
    text = f"코스피 시황뉴스 메뉴로 오셨습니다.\n\n"
    text += news.kospi_news()
    return text

def kosdaq_point_message():
    kosdaq = finance_def.Kos
    text = f"코스닥 지수 메뉴로 오셨습니다.\n\n"
    text += kosdaq.kosdaq_main()
    return text

def kosdaq_news_message():
    news = finance_def.Kos
    text = f"코스닥 시황뉴스 메뉴로 오셨습니다.\n\n"
    text += news.kosdaq_news()
    return text

def today_news_message():
    t_news = finance_def.Get_News
    text = f"Today News 메뉴로 오셨습니다.\n\n"
    text += t_news.main_news()
    return text

def condition_news_message():
    c_news = finance_def.Get_News
    text = f"시황·전망 뉴스 메뉴입니다.\n\n"
    text += c_news.condition_news()
    return text

def analyze_news_message():
    a_news = finance_def.Get_News
    text = f"기업·종목분석 뉴스 메뉴입니다.\n\n"
    text += a_news.analyze_news()
    return text

def overseas_news_message():
    o_news = finance_def.Get_News
    text = f"해외 증시 뉴스 메뉴입니다.\n\n"
    text += o_news.overseas_news()
    return text

def bond_news_message():
    b_news = finance_def.Get_News
    text = f"채권·선물 뉴스 메뉴입니다.\n\n"
    text += b_news.bond_news()
    return text

def memo_news_message():
    m_news = finance_def.Get_News
    text = f"공시·메모 뉴스 메뉴입니다.\n\n"
    text += m_news.memo_news()
    return text

def rate_news_message():
    r_news = finance_def.Get_News
    text = f"환율 뉴스 메뉴입니다.\n\n"
    text += r_news.rate_news()
    return text

def search_news_message():
    text = f"종목검색을 시작합니다.\n주식 종목을 정확하게 입력해주세요.Ex)LG전자"
    return text

if __name__ == '__main__':
############################### Main Menu ############################################
    def start(bot, update):
        bot.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard())

    def main_menu(bot, update):
        bot.callback_query.message.edit_text(main_menu_message(), reply_markup=main_menu_keyboard())

    def first_menu(bot, update):
        bot.callback_query.message.edit_text(first_menu_message(), reply_markup=first_menu_keyboard())

    def about_menu(bot, update):
        bot.callback_query.message.edit_text(about_menu_message(), reply_markup=about_menu_keyboard())
############################### First Sub Menu ############################################
    def first_submenu_1(bot, update):
        bot.callback_query.message.edit_text(first_submenu_1_message(), reply_markup=first_submenu_keyboard())

    def first_submenu_2(bot, update):
        bot.callback_query.message.edit_text(first_submenu_2_message(), reply_markup=first_submenu_keyboard())

    def first_submenu_3(bot, update):
        bot.callback_query.message.edit_text(first_submenu_3_message(), reply_markup=first_submenu_keyboard())

    def first_submenu_4(bot, update):
        bot.callback_query.message.edit_text(first_submenu_4_message(), reply_markup=first_submenu_keyboard())

    def first_submenu_5(bot, update):
        bot.callback_query.message.edit_text(first_submenu_5_message(), reply_markup=kospi_submenu_keyboard())

    def first_submenu_6(bot, update):
        bot.callback_query.message.edit_text(first_submenu_6_message(), reply_markup=kosdaq_submenu_keyboard())

    def first_submenu_7(bot, update):
        bot.callback_query.message.edit_text(first_submenu_7_message(), reply_markup=search_company_keyboard())

    def first_submenu_8(bot, update):
        bot.callback_query.message.edit_text(first_submenu_8_message(), reply_markup=news_menu_keyboard())
############################### First Sub-Sub Menu ############################################
    def kospi_point(bot, update):
        bot.callback_query.message.edit_text(kospi_point_message(), reply_markup= kospi_menu_keyboard())

    def kospi_news(bot, update):
        bot.callback_query.message.edit_text(kospi_news_message(),  reply_markup= kospi_menu_keyboard())

    def kosdaq_point(bot, update):
        bot.callback_query.message.edit_text(kosdaq_point_message(), reply_markup= kosdaq_menu_keyboard())

    def kosdaq_news(bot, update):
        bot.callback_query.message.edit_text(kosdaq_news_message(), reply_markup= kosdaq_menu_keyboard())

    def today_news(bot, update):
        bot.callback_query.message.edit_text(today_news_message(), reply_markup= news_submenu_keyboard())

    def condition_news(bot, update):
        bot.callback_query.message.edit_text(condition_news_message(), reply_markup= news_submenu_keyboard())

    def analyze_news(bot, update):
        bot.callback_query.message.edit_text(analyze_news_message(), reply_markup= news_submenu_keyboard())

    def overseas_news(bot, update):
        bot.callback_query.message.edit_text(overseas_news_message(), reply_markup= news_submenu_keyboard())

    def bond_news(bot, update):
        bot.callback_query.message.edit_text(bond_news_message(), reply_markup= news_submenu_keyboard())

    def memo_news(bot, update):
        bot.callback_query.message.edit_text(memo_news_message(), reply_markup= news_submenu_keyboard())

    def rate_news(bot, update):
        bot.callback_query.message.edit_text(rate_news_message(), reply_markup= news_submenu_keyboard())

    def on(bot, update):
        bot.callback_query.message.edit_text("/v 검색할 종목명 으로 입력하시면 검색결과가 화면에 나타납니다.")
        def v(update, context):
            user_text = update.message.text[3:]
            code = finance_def.Get_CompanyCode.stock_list(user_text)
            today = finance_def.Get_Price.get_price_company(code, 0)
            yester = finance_def.Get_Price.get_price_company(code, 1)
            high = finance_def.Get_Price.get_price_company(code, 2)
            low = finance_def.Get_Price.get_price_company(code, 3)
            volume = finance_def.Get_Price.get_price_company(code, 4)
            money = finance_def.Get_Price.get_price_company(code, 5)
            updown = finance_def.Get_Price.get_price_company(code, 6)
            bot.callback_query.message.edit_text("검색하신 종목명 : " + user_text + "\n현재가격 : " + today + "\n전일종가 : " + yester + "\n당일고가 : " + high + "\n당일저가 : " + low + "\n거래량 : " + volume + "\n거래대금(백만) : " + money + "\n"+updown,
                          reply_markup =back_keyboard())
        updater.dispatcher.add_handler(CommandHandler('v', v))

############################# MainMenu Handlers #########################################
    updater = Updater(token=my_token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(about_menu, pattern="ab_1"))
############################# SubMenu Handlers #########################################
    updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu_1, pattern='k1_1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu_2, pattern='k1_2'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu_3, pattern='k1_3'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu_4, pattern='k1_4'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu_5, pattern='k1_5'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu_6, pattern='k1_6'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu_7, pattern='k1_7'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu_8, pattern='k1_8'))
    updater.dispatcher.add_handler(CallbackQueryHandler(kospi_point, pattern='kp_1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(kospi_news, pattern='kp_2'))
    updater.dispatcher.add_handler(CallbackQueryHandler(kosdaq_point, pattern='kd_1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(kosdaq_news, pattern='kd_2'))
    updater.dispatcher.add_handler(CallbackQueryHandler(today_news, pattern='new_1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(condition_news, pattern='new_2'))
    updater.dispatcher.add_handler(CallbackQueryHandler(analyze_news, pattern='new_3'))
    updater.dispatcher.add_handler(CallbackQueryHandler(overseas_news, pattern='new_4'))
    updater.dispatcher.add_handler(CallbackQueryHandler(bond_news, pattern='new_5'))
    updater.dispatcher.add_handler(CallbackQueryHandler(memo_news, pattern='new_6'))
    updater.dispatcher.add_handler(CallbackQueryHandler(rate_news, pattern='new_7'))
    updater.dispatcher.add_handler(CallbackQueryHandler(on, 's1_1'))

    updater.dispatcher.add_error_handler(error)
    updater.start_polling()
################################################################################